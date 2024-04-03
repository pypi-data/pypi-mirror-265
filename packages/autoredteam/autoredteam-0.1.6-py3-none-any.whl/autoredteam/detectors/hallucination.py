from .base import Detector
from autoredteam.metrics.hhem import HHEM


class Hallucination(Detector):
    """
    Checks for hallucinations in the outputs.
    """

    def __init__(self, threshold, *args, **kwargs):
        self.model = HHEM()
        self.threshold = threshold
        super().__init__(*args, **kwargs)

    def detect(self, attempt):
        outputs = []
        for out in attempt.outputs:
            score = self.model.score(attempt.prompt, out)
            outputs.append(1 if score > self.threshold else 0)
        return outputs
