from abc import ABC, abstractmethod
from tqdm.autonotebook import tqdm
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from garak import _config
import json


class Metric(ABC):
    name = "base.Metric"
    threshold = None
    tokenizer = None
    model = None

    def __init__(self, yaml_path=None, tokenizer=None, model=None):
        self.yaml_path = yaml_path
        if tokenizer:
            self.tokenizer = AutoTokenizer.from_pretrained(tokenizer)
        if model:
            self.model = AutoModelForSequenceClassification.from_pretrained(model)

    @abstractmethod
    def score(self, sentence1, sentence2):
        return NotImplemented

    def evaluate(self, testset):
        """
        Evaluate the outputs of the agent.
        """

        scores = []
        for _, row in tqdm(testset.iterrows(), desc=self.name, total=testset.shape[0]):
            scores.append(self.score(str(row["answer"]), str(row["ground_truth"])))
        self.scores = scores

    def summarize(self, threshold=None, logged: bool = False):
        """
        Summarizes the results of the test

        Attributes:
            threshold (float): the threshold for a detector to pass. Defaults to None.
        """
        eval_summary = {
            "passed": sum([1 for x in self.scores if x < threshold])
            if threshold
            else sum(self.scores),
            "total": len(self.scores),
        }
        eval_summary["pass_rate"] = round(
            eval_summary["passed"] / eval_summary["total"] * 100, 2
        )
        self.eval_summary = eval_summary

        if logged:
            _config.transient.reportfile.write(
                json.dumps(
                    {
                        "entry_type": "eval",
                        "test": self.name,
                        "metric": self.name,
                        "passed": self.eval_summary["passed"],
                        "total": self.eval_summary["total"],
                    }
                )
                + "\n"
            )

        print(
            f"{self.name:<50} score: {round(self.eval_summary['passed'],2):>4}/{self.eval_summary['total']:>4} ({self.eval_summary['pass_rate']:>6}%)"
        )

        # # record the hits if logging is enabled
        # if logged:
        #     for d in self.detectors:
        #         detname = ".".join(d.detectorname.split(".")[-2:])
        #         for attempt in self.attempt_results:
        #             for idx, score in enumerate(attempt.detector_results[detname]):
        #                 if score > threshold:  # if we don't pass
        #                     if not _config.transient.hitlogfile:
        #                         hitlog_filename = f"{_config.reporting.report_dir}/autoredteam.{_config.transient.run_id}.hitlog.jsonl"
        #                         logging.info("hit log in %s", hitlog_filename)
        #                         _config.transient.hitlogfile = open(
        #                             hitlog_filename,
        #                             "w",
        #                             buffering=1,
        #                             encoding="utf-8",
        #                         )

        #                     trigger = None
        #                     if "trigger" in attempt.notes:
        #                         trigger = attempt.notes["trigger"]
        #                     _config.transient.hitlogfile.write(
        #                         json.dumps(
        #                             {
        #                                 "goal": attempt.goal,
        #                                 "prompt": attempt.prompt,
        #                                 "output": attempt.outputs[idx],
        #                                 "trigger": trigger,
        #                                 "score": score,
        #                                 "run_id": str(_config.transient.run_id),
        #                                 "attempt_id": str(attempt.uuid),
        #                                 "attempt_seq": attempt.seq,
        #                                 "attempt_idx": idx,
        #                                 "test": self.name,
        #                                 "detector": detname,
        #                                 "generations_per_prompt": len(
        #                                     attempt.detector_results[detname]
        #                                 ),
        #                             }
        #                         )
        #                         + "\n"
        #                     )
