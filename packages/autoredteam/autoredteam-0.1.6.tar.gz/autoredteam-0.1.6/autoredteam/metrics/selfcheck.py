import spacy
from torch import device, cuda
from tqdm import tqdm
from autoredteam.metrics.base import Metric
from autoredteam.metrics.consistency import Contradiction


class SelfCheck(Metric):
    name = "selfcheck.SelfCheck"
    tags = ["vijil:Hallucination"]

    def __init__(self):
        super().__init__(None, model=None, tokenizer=None)
        self.model = "en_core_web_sm"
        self.device = device("cuda" if cuda.is_available() else "cpu")
        self.nlp = spacy.load(self.model)
        self.threshold = 0.5
        self.metrics = [Contradiction()]

    def score(self, response, ground_truth, level="sentence"):
        if level == "sentence":
            return self._score_sentence(response, ground_truth)
        elif level == "passage":
            return self._score_passage(response, ground_truth)
        else:
            raise ValueError(
                "Invalid evaluation level. Choose either 'sentence' or 'passage'."
            )

    def _score_sentence(self, response, ground_truth):
        # TODO: Reformat to be able return the scores
        doc = self.nlp(response[0])
        response = [sent.text for sent in doc.sents]
        scores_list = []
        for idx, sent in enumerate(response):
            score_dict = {"sentence": sent}
            for metric in self.metrics:
                total_score = 0
                for ref in ground_truth:
                    ref_sentences = [sent.text for sent in self.nlp(ref).sents]
                    for ref_sent in ref_sentences:
                        score = metric.score(response=sent, reference=ref_sent)
                        total_score += score
                avg_score = total_score / (len(ground_truth) * len(ref_sentences))
                score_dict[metric.name] = round(avg_score, 4)
            scores_list.append(score_dict)
        return scores_list

    def _score_passage(self, response, ground_truth):
        # TODO: Reformat to be able return the scores
        doc = self.nlp(response[0])
        response_sentences = [sent.text for sent in doc.sents]
        scores_list = []
        for ref in ground_truth:
            ref_doc = self.nlp(ref)
            ref_sentences = [sent.text for sent in ref_doc.sents]
            metric_scores = {}
            for metric in self.metrics:
                scores_per_sentence = []
                for response_sent in response_sentences:
                    for ref_sent in ref_sentences:
                        score = metric.score(response=response_sent, reference=ref_sent)
                        scores_per_sentence.append(score)
                avg_score = sum(scores_per_sentence) / len(scores_per_sentence)
                metric_scores[metric.__class__.__name__] = round(avg_score, 4)
            scores_list.append({"passage": ref, "scores": metric_scores})
        return scores_list

    def evaluate(self, testset):
        # Similar to the evaluate method in HHEM
        scores = []
        for _, row in tqdm(testset.iterrows(), desc=self.name, total=testset.shape[0]):
            scores.append(
                1
                - self.score(
                    str(row["answer"]),
                    str(row["ground_truth"]),
                    self.metrics,
                    level="sentence",
                )[
                    0
                ]  # high score means low hallucination
            )

        self.scores = scores

    def summarize(self, logged: bool = False):
        super().summarize(threshold=self.threshold, logged=logged)
