#!/usr/bin/env python
"""Defines the Report class and associated functions to process and export a native autoredteam report"""

import contextlib
import importlib
import json
import pandas as pd
from datetime import date
import warnings

import avidtools.datamodels.report as ar
import avidtools.datamodels.components as ac
import avidtools.datamodels.enums as ae


# load up a .jsonl output file, take in eval and config rows
class Report:
    """A class defining a generic report object to store information in a autoredteam report (typically named `autoredteam.<uuid4>.report.jsonl`).

    :param path: location where the file is stored.
    :type path: str
    :param records: list of raw json records in the report file
    :type records: List[dict]
    :param metadata: report metadata, storing information about scanned model
    :type metadata: dict
    :param evaluations: evaluation information at test level
    :type evaluations: pd.DataFrame
    :param scores: average pass percentage per test
    :type scores: pd.DataFrame
    :param write_location: location where the output is written out.
    :type write_location: str
    """

    def __init__(
        self, path=None, records=[], metadata=None, evaluations=None, scores=None
    ):
        if path is None and len(records) == 0:
            raise ValueError(
                "Supply either a path or records to initialize the Report object."
            )
        self.path = path
        self.records = records
        self.metadata = metadata
        self.evaluations = evaluations
        self.scores = scores

    def load(self):
        """
        Loads a autoredteam report.
        """
        if self.path is not None and len(self.records) == 0:
            with open(self.path, "r") as reportfile:
                for line in reportfile:
                    record = json.loads(line.strip())
                    self.records.append(record)
        else:
            warnings.warn("Records already loaded. Skipping load from path.")

        # Extract evaluation information from loaded records
        evals = []

        for record in self.records:
            if record["entry_type"] == "eval":
                evals.append(record)
            elif record["entry_type"] == "config":
                self.metadata = record
        if len(evals) == 0:
            raise ValueError("No evaluations to report 🤷")

        # add tags
        with contextlib.redirect_stdout(None):
            for i in range(len(evals)):
                module_name, plugin_class_name = evals[i]["test"].split(".")
                mod = importlib.import_module(f"autoredteam.tests.{module_name}")

                evals[i]["test"] = f"{module_name}.{plugin_class_name}"
                plugin_instance = getattr(mod, plugin_class_name)()
                evals[i]["tags"] = plugin_instance.tags

        # summary table
        evals1 = pd.DataFrame(evals)
        evals1 = evals1[
            evals1["test"] != "realtoxicityprompts.RTPBlank"
        ]  # filter out test = realtoxicityprompts.RTPBlank
        evals1["score"] = evals1.apply(
            lambda x: round(x["passed"] / x["total"] * 100, 2), axis=1
        )
        evals1["test_module"] = evals1.apply(lambda x: x["test"].split(".")[0], axis=1)

        self.evaluations = evals1
        self.scores = self.evaluations[["test", "score"]].groupby("test").mean()
        return self

    def convert(self):
        """Converts into the AVID schema"""
        # set up a generic AVID report template
        report_template = ar.Report()
        if self.metadata is not None:
            report_template.affects = ac.Affects(
                developer=[],
                deployer=[self.metadata["model_type"]],
                artifacts=[
                    ac.Artifact(
                        type=ae.ArtifactTypeEnum.model, name=self.metadata["model_name"]
                    )
                ],
            )

        report_template.references = [
            ac.Reference(
                type="source",
                label="autoredteam, a generative AI red teaming suite by vijil",
                url="https://pypi.org/project/autoredteam",
            )
        ]
        report_template.reported_date = date.today()

        # now build all the reports
        self.reports = []
        for test in self.scores.index:
            # report = report_template
            report = report_template.copy()
            test_data = self.evaluations.query(f"test=='{test}'")

            report.description = ac.LangValue(
                lang="eng",
                value=f"The model {self.metadata['model_name']} from {self.metadata['model_type']} was evaluated by the autoredteam LLM Vunerability scanner using the test `{test}`.",
            )
            report.problemtype = ac.Problemtype(
                classof=ae.ClassEnum.llm,
                type=ae.TypeEnum.measurement,
                description=report.description,
            )
            report.metrics = [
                ac.Metric(
                    name="",
                    detection_method=ac.Detection(
                        type=ae.MethodEnum.thres, name="Count failed"
                    ),
                    results=test_data[["detector", "passed", "total", "score"]]
                    .reset_index()
                    .to_dict(),
                )
            ]
            all_tags = test_data.iloc[0]["tags"]
            tag_flag = sum([tag.startswith("avid") for tag in all_tags]) > 0
            if tag_flag:  # check for AVID taxonomy tags
                tags_split = [
                    tag.split(":") for tag in all_tags if tag.startswith("avid")
                ]  # supports only avid taxonomy for now
                report.impact = ac.Impact(
                    avid=ac.AvidTaxonomy(
                        vuln_id="",
                        risk_domain=pd.Series([tag[1].title() for tag in tags_split])
                        .drop_duplicates()
                        .tolist(),  # unique values
                        sep_view=[ae.SepEnum[tag[2]] for tag in tags_split],
                        lifecycle_view=[ae.LifecycleEnum["L05"]],
                        taxonomy_version="",
                    )
                )
            self.reports.append(report)
        return self

    def export(self, export_path=None):
        """Writes out output in a specified format."""

        # save final output
        if export_path is None:
            self.export_path = self.path.replace(".report", ".avid")
        else:
            self.export_path = export_path
        with open(self.export_path, "w") as f:
            f.writelines(r.json() + "\n" for r in self.reports)
