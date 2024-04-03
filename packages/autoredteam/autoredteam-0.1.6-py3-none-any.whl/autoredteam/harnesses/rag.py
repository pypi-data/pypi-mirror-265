import importlib
import pandas as pd
from tqdm.autonotebook import tqdm
from uuid import uuid4
import json
from datetime import datetime
from garak import _config

from .base import Harness
from ..agents.testgen import TestsetAgent, ChaosAgent


class RAGHarness(Harness):
    metrics = []
    metric_instances = []
    eval_summary = None

    def __init__(self, agent, documents, metrics=None):
        """
        Initialize a harness.

        Args:
            agent (Agent): An `Agent` object.
        """
        self.agent = agent
        self.documents = documents

        if metrics is not None:
            self.add_metrics(metrics)

    def add_metrics(self, metrics):
        """
        Add metrics to the harness.

        Args:
            metrics (list): A list of metric names.
        """
        for metric in metrics:
            if metric not in self.metrics:
                module_name, class_name = metric.rsplit(".", 1)
                print(f"Initializing metric {class_name} from module {module_name}")
                metric_class = getattr(
                    importlib.import_module(f"autoredteam.metrics.{module_name}"),
                    class_name,
                )
                self.metric_instances.append(metric_class())
                self.metrics.append(metric)
            else:
                print(f"Metric {metric} already added to harness, skipping.")

    def generate_testset(self, n=5, distribution=None):
    # def generate_testset(self, n=10, distribution=None): # temporary
        # generate initial testset
        gen_agent = TestsetAgent(documents=self.documents)
        self.testset = gen_agent.generate(n=n, distribution=distribution)
        return self

    def perturb_testset(self, perturbation=None, persona=None):
        """
        generated perturbed testset
        """
        chaos_agent = ChaosAgent(self.testset)
        self.perturbed_testsets = chaos_agent.generate(
            perturbation=perturbation, agent_persona=persona
        )
        self.testset["original_question"] = self.testset["question"]
        self.testset["perturbation"] = ["original" for _ in range(len(self.testset))]
        self.testset = pd.concat([self.testset, self.perturbed_testsets])
        return self

    def generate_answers(self):
        """
        Generate outputs from agent and score as a column in the test dataset.
        """
        test_records = self.testset.to_dict(orient="records")
        self.outputs = []
        for record in tqdm(test_records, desc="Generating answers"):
            rec_results = self.agent.generate(record["question"])
            for i in range(len(rec_results)):
                out_dict = record.copy()
                out_dict["answer"] = rec_results[i]
                out_dict["uuid"] = str(uuid4())
                self.outputs.append(out_dict)

        self.outputs = pd.DataFrame(self.outputs)

    def evaluate(self, metrics=None):
        """
        Evaluate the outputs of the agent.
        """

        # choose metrics instances to evaluate on
        if metrics is not None:
            metrics_to_evaluate = [
                metric for metric in self.metric_instances if metric.name in metrics
            ]
        else:
            metrics_to_evaluate = self.metric_instances

        for metric in metrics_to_evaluate:
            metric.evaluate(self.outputs)
            if metric.threshold is not None:
                self.outputs[metric.name] = [
                    1 if score < metric.threshold else 0 for score in metric.scores
                ]
            else:
                self.outputs[metric.name] = metric.scores

    def summarize(self, verbose=False):
        """
        Summarize the results of the evaluation.
        """
        # for metric in self.metric_instances:
        #     metric.summarize()
        self.eval_summary = []
        for pert in self.outputs["perturbation"].unique():
            for metric in self.metrics:
                self.eval_summary.append(
                    {
                        "perturbation": pert,
                        "metric": metric,
                        "passed": float(
                            self.outputs[self.outputs["perturbation"] == pert][
                                metric
                            ].sum()
                        ),
                        "total": len(
                            self.outputs[self.outputs["perturbation"] == pert]
                        ),
                    }
                )

        if verbose:
            for row in self.eval_summary:
                print(
                    f"{row['perturbation']:<50} {row['metric']:>50}: {row['passed']:.2f}/{row['total']:>4} ({100*row['passed']/row['total']:.2f}%)"
                )

    def export(self, logged: bool = False, path: str = None):
        """create custom export function for harness"""
        if logged:
            f = _config.transient.reportfile
        else:
            if path is None:
                path = f"{type(self).__name__}_{int(datetime.utcnow().timestamp())}.report.jsonl"
            f = open(path, "a")

        for i, row in self.outputs.iterrows():
            attempt_dict = {
                "entry_type": "attempt",
                "uuid": row["uuid"],
                "seq": i,
                "status": 2,
                "prompt": row["question"],
                "outputs": [row["answer"]],
                "detector_results": {},
                "notes": {
                    "original_question": row["original_question"],
                    "ground_truth": row["ground_truth"],
                    "perturbation": row["perturbation"],
                },
            }
            for metric in self.metrics:
                attempt_dict["detector_results"][metric] = [row[metric]]

            f.write(json.dumps(attempt_dict) + "\n")

        # summarize the results of the evaluation
        if self.eval_summary is None:
            self.summarize()
        for eval_row in self.eval_summary:
            f.write(
                json.dumps(
                    {
                        "entry_type": "eval",
                        "perturbation": eval_row["perturbation"],
                        "metric": eval_row["metric"],
                        "passed": eval_row["passed"],
                        "total": eval_row["total"],
                    },
                    default=str,
                )
                + "\n"
            )

    def run(self, logged: bool = False):
        """
        Run all metrics in the harness.
        """
        out_string = f"Containing metrics: "
        for metric in self.metric_instances:
            out_string += f"{metric.name}, "
        print(out_string[:-2])
        
        # generate test data
        self.generate_testset()
        self.perturb_testset()

        # generate and evaluate the outputs
        self.generate_answers()
        self.evaluate()
        self.summarize(verbose=True)
        self.export(logged=logged)
