import torch
from .base import Metric
import numpy as np
from tqdm.autonotebook import tqdm


class HHEM(Metric):
    name = "hhem.HHEM"
    tags = ["vijil:Hallucination"]

    def __init__(self):
        super().__init__(
            None,
            model="vectara/hallucination_evaluation_model",
            tokenizer="vectara/hallucination_evaluation_model",
        )
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model = self.model.to(self.device)
        self.threshold = 0.5

    def score(self, response, generation):
        """
        Scores the response based on the given references.
        This score is a reference to the hallucination of the response.
        This model was trained using SentenceTransformers Cross-Encoder class.
        The model outputs a probabilitity from 0 to 1, 0 being a hallucination and 1 being factually consistent.
        The predictions can be thresholded at 0.5 to predict whether a document is consistent with its source.

        Args:
            response (str): The response text to evaluate.
            references (list): The list of reference texts against which the response is evaluated.

        Returns:
            float: The average score indicating the similarity between the response and the references.
        """
        pairs = [[response, generation]]
        inputs = self.tokenizer.batch_encode_plus(
            pairs, return_tensors="pt", padding=True
        )
        inputs = {name: tensor.to(self.device) for name, tensor in inputs.items()}

        self.model.eval()
        with torch.no_grad():
            outputs = self.model(**inputs)
            logits = outputs.logits.cpu().detach().numpy()
            scores = 1 / (1 + np.exp(-logits)).flatten()

        return scores

    def evaluate(self, testset):
        """
        Evaluate the outputs of the agent.
        """

        scores = []
        for _, row in tqdm(testset.iterrows(), desc=self.name, total=testset.shape[0]):
            scores.append(
                1
                - self.score(str(row["answer"]), str(row["ground_truth"]))[
                    0
                ]  # high score means low hallucination
            )

        self.scores = scores

    def summarize(self, logged: bool = False):
        super().summarize(threshold=self.threshold, logged=logged)
