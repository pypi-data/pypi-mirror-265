import importlib

from .base import MetricTest
from ..agents.testgen import ChaosAgent
from ..agents.openai import OpenaiAgent
from garak.probes.base import Probe

# create and populate the probe instance
probe_instance = Probe()
probe_instance.__doc__ = "This test checks if the LLM/agent displays hallucination."
probe_instance.uri = ""
probe_instance.description = probe_instance.__doc__
probe_instance.recommended_detector = ["paraphrase.SameAnswer"]
probe_instance.goal = "try to make the agent hallucinate"
probe_instance.active = False

# import detector and instantiate
det_module_name, detector_name = probe_instance.recommended_detector[0].split(".")
detector_module = importlib.import_module(f"autoredteam.detectors.{det_module_name}")
det_instance = getattr(detector_module, detector_name)(
    agent=OpenaiAgent("gpt-4", generations=1)
)


class ParaphraseTest(MetricTest):
    __doc__ = probe_instance.__doc__
    probe = probe_instance
    detectors = [det_instance]
    uri = probe_instance.uri
    description = probe_instance.description
    tags = ["vijil:Hallucination", "vijil:Robustness"] + probe_instance.tags
    goal = probe_instance.goal
    active = probe_instance.active

    def __init__(self, data):
        print("Initializing prompts using seed data")
        self.data = data
        self.agent = ChaosAgent(testset=self.data)


class Adversarial(ParaphraseTest):
    name = "paraphrase.Adversarial"
    description = probe_instance.description

    def __init__(self, persona, data):
        super().__init__(data)
        self.newdata = self.agent.generate(
            perturbation="adversarial-paraphrases", agent_persona=persona
        )
        self.prompts = self.newdata["question"]
        self.ground_truth = self.newdata["ground_truth"]
        self.probe.prompts = self.prompts

    def evaluate(self, logged: bool = False):
        # append triggers
        for i, attempt in enumerate(self.attempt_results):
            attempt.notes["ground_truth"] = self.ground_truth[i]

        super().evaluate(logged=logged)


benign_detectors = [
    "ParaphraseDetector",
    "Entailment",
    "Contradiction",
    "BLEU",
    "BERTScore",
    "AgreementNER",
]


class Benign(ParaphraseTest):
    name = "paraphrase.Benign"

    def __init__(self, data):
        super().__init__(data)
        self.detectors = [
            getattr(detector_module, detector_name)()
            for detector_name in benign_detectors
        ] + [det_instance]
        self.newdata = self.agent.generate(perturbation="benign-paraphrases")
        self.prompts = self.newdata["question"]
        self.ground_truth = self.newdata["ground_truth"]
        self.probe.prompts = self.prompts
        self.probe.recommended_detector += [
            "paraphrase." + det for det in benign_detectors
        ]

    def evaluate(self, logged: bool = False):
        # append triggers
        for i, attempt in enumerate(self.attempt_results):
            attempt.notes["ground_truth"] = self.ground_truth[i]

        super().evaluate(logged=logged)
