import sys
from datasets import Dataset
from ragas import evaluate
from ragas.metrics import (
    faithfulness,
    answer_correctness,
    answer_relevancy,
    answer_similarity,
    context_entity_recall,
    context_precision,
    context_recall,
    context_relevancy,
)
from .base import Metric
from ..utils import local_constructor

METRICS_DICT = {
    "faithfulness": faithfulness,
    "answer_correctness": answer_correctness,
    "answer_relevancy": answer_relevancy,
    "answer_similarity": answer_similarity,
    "context_entity_recall": context_entity_recall,
    "context_precision": context_precision,
    "context_recall": context_recall,
    "context_relevancy": context_relevancy,
}


class RagasMetric(Metric):
    def __init__(self):
        self.metrics_dict = METRICS_DICT

    def score(self, data, metrics=None):
        if metrics is not None:
            metrics_modules = [
                self.metrics_dict[metric]
                for metric in metrics
                if metric in self.metrics_dict
            ]
        else:
            metrics_modules = list(self.metrics_dict.values())

        dataset = Dataset.from_pandas(data)
        score = evaluate(dataset, metrics=metrics_modules)
        return score.to_pandas()[metrics]


def local_score(self, data):
    ret = super(self.__class__, self).score(data, metrics=[self.metric])
    self.scores = list(ret[self.metric])


# dynamically create all ragas metrics
this = sys.modules[__name__]

for metric in METRICS_DICT.keys():
    metric_formatted = metric.replace("_", " ").title().replace(" ", "")
    setattr(
        this,
        metric_formatted,
        type(
            metric_formatted,
            (RagasMetric,),
            {
                "__init__": local_constructor,
                "name": f"ragas.{metric_formatted}",
                "metric": metric,
                "evaluate": local_score,
                "tags": ["vijil:Hallucination"]
                if metric == "faithfulness"
                else ["vijil:Performance"],
            },
        ),
    )
