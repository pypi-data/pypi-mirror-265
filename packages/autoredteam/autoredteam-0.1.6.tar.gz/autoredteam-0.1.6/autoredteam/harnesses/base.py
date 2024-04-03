"""
The base `Harness` class provides a generic outline of an end to end structure of running a number of tests.

All other harnesses in `autoredteam` inherit from this class.
"""
from datetime import datetime
from garak.detectors.mitigation import MitigationBypass
from ..analyze.avid import Report


class Harness:
    tests = None
    # detectors = Optional[List[Dict[str, str]]]

    def __init__(self, agent, tests=None):
        """
        Initialize a harness.

        Args:
            agent (Agent): An `Agent` object.
        """
        self.agent = agent
        if tests is not None:
            self.tests = tests
        if self.tests is not None:
            self.test_instances = [getattr(self, test)() for test in self.tests]

    def run(self, logged: bool = False):
        """
        Run all tests in the harness.
        """
        out_string = f"Containing tests: "
        for test in self.test_instances:
            out_string += f"{test.name}, "
        print(out_string[:-2])
        # print(f"Containing tests: {[test.name for test in self.test_instances]}")
        for test in self.test_instances:
            test.run(self.agent, logged=logged)
        # return self

    def summarize(self):
        """
        Summarize the results of all tests in the harness.
        """
        for test in self.test_instances:
            test.summarize()

        # compile all results into a single dict
        self.eval_summary = {}
        for test in self.test_instances:
            self.eval_summary[test.__class__.__name__] = dict(test.eval_summary)

        # return self

    def export(self, path: str = None, subset=None, threshold=0.5):
        """
        Export the results of all tests in the harness.

        Args:
            path (str): Path to export results to. Defaults to None.
        """

        if path is None:
            if subset == "hits":
                level = "hitlog"
            else:
                level = "report"
            path = f"{type(self).__name__}_{int(datetime.utcnow().timestamp())}.{level}.jsonl"

        for test in self.test_instances:
            test.export(path=path, subset=subset, threshold=threshold, mode="a")

    def to_report(self):
        records = [
            {
                "entry_type": "config",
                "model_type": self.agent.family.lower(),
                "model_name": self.agent.name,
                "generations": self.agent.generations,
            }
        ]
        for t in self.test_instances:
            records += [attempt.as_dict() for attempt in t.attempt_results] + [
                {
                    "entry_type": "eval",
                    "test": t.name,
                    "detector": det,
                    "passed": t.eval_summary[det]["passed"],
                    "total": t.eval_summary[det]["total"],
                }
                for det in t.eval_summary.keys()
            ]

        return Report(records=records)

    def force_abstain(self):
        """
        Swap out all detectors for a dummy detector that checks for abstainment.

        This is useful for testing RAG-like systems or domain-specific LLMs where
        the desirable output for irrelevant prompts is to abstain.
        """
        for test in self.test_instances:
            test.detectors = [MitigationBypass()]
        return self
