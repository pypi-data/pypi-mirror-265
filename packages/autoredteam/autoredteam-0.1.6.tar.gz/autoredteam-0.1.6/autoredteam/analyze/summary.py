"""
Produces a summary of the results of the red teaming exercise.
"""

import json
import pandas as pd
import numpy as np

from ..utils import (
    TRUST_DICT,
    TRUST_DICT_METRICS,
    TRUST_DICT_PERTURBATIONS,
    simulate_group_ci,
)


def compile_summary(
    path: str, dimensions: str = None, confint: bool = False, print_output: bool = True
):
    """ "
    Compile a digest from a report JSONL file

    Args:
        path (str): path to a report JSONL file
        dimensions (str): Trust dimensions to summarize by, comma separated. Default is all dimensions.
        confint (bool): Whether to include confidence intervals. Default is False.
        print_output (bool): Whether to print the summary. Default is True.

    Returns:
        dict: A dictionary containing summary tables at multiple levels and overall trust score.
        contains the following keys: "test", "test_module", "trust_dimension", "overall".
    """
    evals = []
    with open(path, "r", encoding="utf-8") as reportfile:
        for line in reportfile:
            record = json.loads(line.strip())
            if record["entry_type"] == "eval":
                evals.append(record)

    dimensions = dimensions.split(",") if dimensions else list(TRUST_DICT.keys())

    # incorporate RAG evals
    for idx, eval in enumerate(evals):
        if "metric" in eval.keys():
            eval["test"] = eval["metric"]
        if "perturbation" in eval.keys():
            eval["test"] += "." + eval["perturbation"]
        evals[idx] = eval

    # summary table
    evals1 = pd.DataFrame(evals)
    evals1 = evals1[
        evals1["test"] != "realtoxicityprompts.RTPBlank"
    ]  # filter out blank tests
    evals1 = evals1.groupby("test")[["passed", "total"]].min().reset_index()
    evals1["score"] = evals1.apply(
        lambda x: round(x["passed"] / x["total"] * 100, 2), axis=1
    )

    # map to test module
    def map_module(eval):
        test_split = eval["test"].split(".")
        if len(test_split) > 2:
            return eval["test"]
        return test_split[0]

    evals1["test_module"] = evals1.apply(lambda x: map_module(x), axis=1)

    # add dimension to each row
    evals1["dimension"] = evals1.apply(lambda x: [], axis=1)
    for _, row in evals1.iterrows():
        for dim, module in TRUST_DICT.items():
            if row["test_module"] in module:
                row["dimension"].append(dim)

        for dim, metrics in TRUST_DICT_METRICS.items():
            for metric in metrics:
                if metric in row["test_module"]:
                    row["dimension"].append(dim)

        for dim, perts in TRUST_DICT_PERTURBATIONS.items():
            for pert in perts:
                if pert in row["test_module"]:
                    row["dimension"].append(dim)

    # filter out rows with empty dimension
    evals1 = evals1[evals1["dimension"].apply(lambda x: len(x) > 0)]
    
    # make dimensions unique
    evals1["dimension"] = evals1["dimension"].apply(lambda x: list(set(x)))

    # summarize by each key of trust_dict
    evals2 = []
    unique_dims = list(
        set([item for sublist in evals1["dimension"].to_list() for item in sublist])
    )
    for dim in unique_dims:
        evals2.append(
            {
                "Dimension": dim,
                "Tests": evals1[evals1["dimension"].apply(lambda x: dim in x)][
                    "passed"
                ].count(),
                "Prompts": evals1[evals1["dimension"].apply(lambda x: dim in x)][
                    "total"
                ].sum(),
                "Passed": evals1[evals1["dimension"].apply(lambda x: dim in x)][
                    "passed"
                ].sum(),
                "Score": round(
                    evals1[evals1["dimension"].apply(lambda x: dim in x)][
                        "score"
                    ].mean(),
                    2,
                ),
            }
        )
    evals2 = pd.DataFrame(evals2)

    # summarize by test module
    evals3 = evals1.groupby("test_module")[["passed", "total"]].sum().reset_index()
    evals3["score"] = (
        evals1.groupby("test_module")[["score"]].mean().reset_index()["score"]
    )
    evals3["score"] = evals3["score"].apply(lambda x: round(x, 2))

    # overall trust score
    trust_score = "{:.2f}".format(sum(evals2["Score"]) / len(evals2))

    # optionally add confidence intervals
    if confint:
        # for evals1
        evals1["score_confint"] = evals1.apply(
            lambda x: simulate_group_ci([x["passed"]], [x["total"]]), axis=1
        )
        # round confint to 2 decimal places
        evals1["score_confint"] = evals1.apply(
            lambda x: (
                round(x["score_confint"][0] * 100, 2),
                round(x["score_confint"][1] * 100, 2),
            ),
            axis=1,
        )

        # for evals2
        ci_data = evals2.apply(
            lambda x: simulate_group_ci(
                evals1[evals1["dimension"].apply(lambda y: x["Dimension"] in y)][
                    "passed"
                ].to_list(),
                evals1[evals1["dimension"].apply(lambda y: x["Dimension"] in y)][
                    "total"
                ].to_list(),
                return_boot=True,
            ),
            axis=1,
        )
        evals2["Score CI"] = [
            (round(x[0] * 100, 2), round(x[1] * 100, 2)) for x in ci_data
        ]

        # for evals3
        evals3["score_confint"] = evals3.apply(
            lambda x: simulate_group_ci([x["passed"]], [x["total"]]), axis=1
        )
        # round confint to 2 decimal places
        evals3["score_confint"] = evals3.apply(
            lambda x: (
                round(x["score_confint"][0] * 100, 2),
                round(x["score_confint"][1] * 100, 2),
            ),
            axis=1,
        )

        # for trust score
        trust_score_dist = np.mean(np.array([x[2] for x in ci_data]), axis=0)
        trust_score = trust_score + " ({:.2f}, {:.2f})".format(
            np.percentile(trust_score_dist, 2.5) * 100,
            np.percentile(trust_score_dist, 97.5) * 100,
        )

    # optionally print the outputs
    if print_output:
        print("\nSummary by test\n-----")
        print(evals1)

        print("\nSummary by test module\n-----")
        print(evals3)

        print("\nSummary by trust dimension\n-----")
        print(evals2)

        print(f"""Overall trust score: {trust_score}""")

    return {
        "test": evals1,
        "test_module": evals3,
        "trust_dimension": evals2,
        "overall": trust_score,
    }
