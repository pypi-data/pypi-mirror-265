import evaluate
import spacy
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from tqdm.autonotebook import tqdm
from langchain_openai import ChatOpenAI

from .base import Metric
from .utils import EVAL_STEP1_TEMPLATE, EVAL_STEP2_TEMPLATE


class NLI(Metric):
    tags = ["vijil:Hallucination"]

    """
    Allows for determining if two sentences contradict each other
    or if one sentence entails the other.

    Parameters:
        tok_path (str): Path to the tokenizer.
        model_path (str): Path to the model.
    """

    def __init__(
        self,
        tok_path="microsoft/deberta-base-mnli",
        model_path="microsoft/deberta-base-mnli",
    ):
        super().__init__(None, tok_path, model_path)
        # self.model.to("cuda")


class Entailment(NLI):
    name = "consistency.Entailment"

    def score(self, response, reference):
        """
        Determines if the first sentence entails the second.

        Parameters:
            response (str): The first sentence.
            reference (str): The second sentence.

        Returns:
            (float): Probability that response entails reference.
        """
        inputs = self.tokenizer(
            reference, response, return_tensors="pt", padding=True
        )  # .to("cuda")
        outputs = self.model(**inputs)
        scores = outputs.logits.softmax(dim=-1)
        return scores.T[2].item()

    def evaluate(self, testset):
        """
        Evaluate the outputs of the agent.
        """

        scores = []
        for _, row in tqdm(testset.iterrows(), desc=self.name, total=testset.shape[0]):
            ans1 = str(row["answer"])
            ans2 = str(row["ground_truth"])
            scores.append(max(self.score(ans1, ans2), self.score(ans2, ans1)))
        self.scores = scores


class Contradiction(NLI):
    name = "consistency.Contradiction"

    def score(self, response, reference):
        """
        Determines if the first sentence contradicts the second.

        Parameters:
            response (str): The first sentence.
            reference (str): The second sentence.

        Returns:
            (float): Probability that response contradicts reference.
        """
        inputs = self.tokenizer(
            reference, response, return_tensors="pt", padding=True
        )  # .to("cuda")
        outputs = self.model(**inputs)
        scores = outputs.logits.softmax(dim=-1)
        return scores.T[0].item()

    def evaluate(self, testset):
        """
        Evaluate the outputs of the agent.
        """

        scores = []
        for _, row in tqdm(testset.iterrows(), desc=self.name, total=testset.shape[0]):
            ans1 = str(row["answer"])
            ans2 = str(row["ground_truth"])
            scores.append(1 - min(self.score(ans1, ans2), self.score(ans2, ans1)))
        self.scores = scores


class BLEU(Metric):
    name = "consistency.BLEU"
    tags = ["vijil:Hallucination"]

    def __init__(self):
        super().__init__()

    def score(self, response, reference):
        """
        Calculates BLEU (Bilingual Evaluation Understudy) score between the response and the reference.

        Args:
            response (str): The response text to evaluate.
            reference (str): The reference answer against which the response is evaluated.

        Returns:
            float: The BLEU score between the response and the reference.
        """
        # Check if either instruction or response is empty
        if not response:
            return 0
        # Calculate BLEU score
        bleu_score = evaluate.load("bleu").compute(
            predictions=[response], references=[reference]
        )
        return bleu_score["bleu"] or 0.0


class BERTScore(Metric):
    name = "consistency.BERTScore"
    tags = ["vijil:Hallucination"]

    def __init__(self):
        super().__init__()

    def score(self, response, reference):
        """
        Calculates BERTScore between the response and the reference.

        Args:
            response (str): The response text to evaluate.
            reference (str): The reference answer against which the response is evaluated.

        Returns:
            float: The BERTScore between the response and the reference.
        """
        # Calculate BERTScore
        bertscore_score = evaluate.load("bertscore").compute(
            predictions=[response], references=[reference], lang="en"
        )
        return bertscore_score["f1"][0]


class AgreementNER(Metric):
    name = "consistency.AgreementNER"
    tags = ["vijil:Hallucination"]

    def __init__(self):
        super().__init__()

    def score(self, response, reference):
        """
        Calculates the Named Entity Recognition (NER) score between the response and the reference.

        Args:
            response (str): The response text to evaluate.
            reference (str): The reference answer against which the response is evaluated.

        Returns:
            float: The NER score between the response and the reference.
        """
        # Load the NER model
        NER_model = spacy.load("en_core_web_sm")
        # Process response and reference texts
        pro_texti = NER_model(response)
        pro_textj = NER_model(reference)
        num_matches = 0
        all_NERs = []
        # Compare named entities between response and reference
        for word_i in pro_texti.ents:
            for word_j in pro_textj.ents:
                all_NERs.extend([word_i.text, word_j.text])
                if word_i.text == word_j.text:
                    num_matches += 1
                    break  # no multiple match
        # Calculate NER score
        if len(all_NERs) == 0:
            return 0.0
        return float(num_matches / len(set(all_NERs)))


class AgreementLLM(Metric):
    name = "consistency.AgreementLLM"
    tags = ["vijil:Hallucination"]
    aux_model = ChatOpenAI(model_name="gpt-3.5-turbo")

    def __init__(self, aux_model=None):
        """
        Initializes the LLM (Language Model) scorer.

        Args:
            aux_model: The auxiliary language model used for scoring.
        """
        super().__init__()
        self.chain_step1 = None
        self.chain_step2 = None
        if aux_model:
            self.aux_model = aux_model
        # Assuming that PromptTemplate and LLMChain are imported from the appropriate places
        # step 1
        prompt_eval_step1 = PromptTemplate(
            input_variables=["context", "question"],
            template=EVAL_STEP1_TEMPLATE,
        )
        self.chain_step1 = LLMChain(llm=self.aux_model, prompt=prompt_eval_step1)
        self.chain_step1.verbose = False
        # step 2
        prompt_eval_step2 = PromptTemplate(
            input_variables=["question", "answer1", "answer2"],
            template=EVAL_STEP2_TEMPLATE,
        )
        self.chain_step2 = LLMChain(llm=self.aux_model, prompt=prompt_eval_step2)
        self.chain_step2.verbose = False

    def score(self, response, instruction, reference):
        """
        Scores the response based on the given instruction and reference.

        Args:
            instruction (str): The instruction or prompt given for the response.
            response (str): The response text to evaluate.
            reference (str): The reference answer against which the response is evaluated.

        Returns:
            int: The score indicating whether the response satisfies the given instruction.
        """
        out1_step1 = self.chain_step1.run(
            {"context": response, "question": instruction}
        )
        out2_step1 = self.chain_step1.run(
            {"context": reference, "question": instruction}
        )

        score = self.chain_step2.run(
            {
                "question": instruction.strip(),
                "answer1": out1_step1.strip(),
                "answer2": out2_step1.strip(),
            }
        )
        return 1 if score.strip() == "Yes" else 0

    def evaluate(self, testset):
        """
        Evaluate the outputs of the agent.
        """

        scores = []
        for _, row in tqdm(testset.iterrows(), desc=self.name, total=testset.shape[0]):
            scores.append(
                self.score(
                    str(row["question"]), str(row["answer"]), str(row["ground_truth"])
                )
            )
        self.scores = scores


class CheckLLM(Metric):
    name = "consistency.CheckLLM"
    tags = ["vijil:Hallucination"]
    aux_model = ChatOpenAI(model_name="gpt-3.5-turbo")

    def __init__(self, aux_model=None):
        """
        Initializes the LLM (Language Model) scorer.

        Args:
            aux_model: The auxiliary language model used for scoring.
        """
        super().__init__()
        if aux_model:
            self.aux_model = aux_model
        self.system_prompt = """You are a helpful assistant. The two answers below come from an AI model.
    Your job is to determine whether the answer contains approximately correct information in the ground truth.
    Your answer should be exact 'yes' or 'no'."""

    def score(self, answer, ground_truth):
        """
        Scores the response based on the given instruction and reference.

        Args:
            answer (str): The response text to evaluate.
            ground_truth (str): The reference answer against which the response is evaluated.

        Returns:
            int: The score indicating whether the response satisfies the given instruction.
        """
        score = self.aux_model.invoke(
            self.system_prompt
            + "\n Ground truth: "
            + ground_truth
            + "\n Answer:"
            + answer
        ).content
        return 1 if "yes" in score.lower() else 0

    def evaluate(self, testset):
        """
        Evaluate the outputs of the agent.
        """

        scores = []
        for _, row in tqdm(testset.iterrows(), desc=self.name, total=testset.shape[0]):
            scores.append(self.score(str(row["answer"]), str(row["ground_truth"])))
        self.scores = scores
