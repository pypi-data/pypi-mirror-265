from .base import Detector, MetricDetector
from consistencybench.metrics import pp, nli, agreement

SYSTEM_PROMPT = """You are a helpful assistant. The two answers below come from an AI model.
    Your job is to determine whether the answer contains approximately correct information in the ground truth.
    Your answer should be exact 'yes' or 'no'."""


class SameAnswer(Detector):
    """
    Compares outputs pairwise in two attempts, detects all matches.
    """

    def __init__(self, agent, *args, **kwargs):
        self.agent = agent
        super().__init__(*args, **kwargs)

    def detect(self, attempt):
        outputs = []
        for out in attempt.outputs:
            ans = self.agent.generate(
                SYSTEM_PROMPT
                + "\n Ground truth: "
                + attempt.notes["ground_truth"]
                + "\n Answer:"
                + out
            )[0]
            outputs.append(0 if "yes" in ans.lower() else 1)

        return outputs


class ParaphraseDetector(MetricDetector):
    def __init__(self, *args, **kwargs):
        super().__init__(metric=pp.ParaphraseDetector(), *args, **kwargs)


class Entailment(MetricDetector):
    def __init__(self, *args, **kwargs):
        super().__init__(
            metric=nli.Entailment(
                tok_path="mrm8488/deberta-v3-large-finetuned-mnli",
                model_path="mrm8488/deberta-v3-large-finetuned-mnli",
            ),
            *args,
            **kwargs
        )

    def detect(self, attempt):
        return [
            self.metric.score_two_sided(output, attempt.notes["ground_truth"])
            for output in attempt.outputs
        ]


class Contradiction(MetricDetector):
    def __init__(self, *args, **kwargs):
        super().__init__(
            metric=nli.Contradiction(
                tok_path="mrm8488/deberta-v3-large-finetuned-mnli",
                model_path="mrm8488/deberta-v3-large-finetuned-mnli",
            ),
            *args,
            **kwargs
        )

    def detect(self, attempt):
        return [
            1 - self.metric.score_two_sided(output, attempt.notes["ground_truth"])
            for output in attempt.outputs
        ]


class BLEU(MetricDetector):
    def __init__(self, *args, **kwargs):
        super().__init__(metric=agreement.BLEU(), *args, **kwargs)


class BERTScore(MetricDetector):
    def __init__(self, *args, **kwargs):
        super().__init__(metric=agreement.BERTScore(), *args, **kwargs)


class AgreementNER(MetricDetector):
    def __init__(self, *args, **kwargs):
        super().__init__(metric=agreement.AgreementNER(), *args, **kwargs)
