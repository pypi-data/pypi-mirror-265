import importlib
import os
import pandas as pd
from tqdm.autonotebook import tqdm
from langchain_openai.chat_models import ChatOpenAI
from langchain_openai.embeddings import OpenAIEmbeddings
from langchain.text_splitter import TokenTextSplitter
from ragas.llms import LangchainLLMWrapper
from ragas.embeddings.base import LangchainEmbeddingsWrapper
from ragas.testset.docstore import InMemoryDocumentStore
from ragas.testset.extractor import KeyphraseExtractor
from ragas.testset.generator import TestsetGenerator, DEFAULT_DISTRIBUTION
from ragas.testset.evolutions import simple, reasoning, multi_context


CHUNK_SIZE = 1024
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_TOKEN")
generator_llm = LangchainLLMWrapper(ChatOpenAI(model="gpt-3.5-turbo-16k"))
critic_llm = LangchainLLMWrapper(ChatOpenAI(model="gpt-4"))
embeddings = LangchainEmbeddingsWrapper(
    OpenAIEmbeddings(model="text-embedding-ada-002")
)
docstore = InMemoryDocumentStore(
    splitter=TokenTextSplitter(chunk_size=CHUNK_SIZE, chunk_overlap=0),
    embeddings=embeddings,
    extractor=KeyphraseExtractor(llm=generator_llm),
)


class TestsetAgent:
    """
    Generates synthetic test dataset, currently uses the Ragas framework.
    Uses OpenAI models and embeddings to generate test dataset.
    """

    generator = TestsetGenerator(
        generator_llm=generator_llm,
        critic_llm=critic_llm,
        embeddings=embeddings,
        docstore=docstore,
    ).with_openai()
    # TODO: refactor to use Agent classes from autoredteam

    def __init__(self, documents):
        """
        Initialize the TestGenerator object with a source and list of documents.

        Parameters
        ----------
        documents : list
            List of langchain or llamaindex documents to use for generating questions.
        """
        parsed_source = str(type(documents[0]))
        if "langchain" in parsed_source:
            self.source = "langchain"
        elif "llama_index" in parsed_source:
            self.source = "llamaindex"
        else:
            raise ValueError(
                "Invalid source. Upload a list of Langchain or LlamaIndex documents."
            )
        print(f"Loading Test set generator agent with given {self.source} documents")
        self.documents = documents

    def generate(self, n, distribution=None):
        """
        Generate test dataset with documents using LangChain documents.

        Parameters
        ----------
        n : int
            Number of questions to generate.
        distribution : dict
            Dictionary of question type distributions, denoting probabilities for three types of questions
            `simple`, `multi_context`, and `reasoning`. See [Ragas docs](https://docs.ragas.io/en/latest/concepts/testset_generation.html)
            for more details.
            Default is `None`, which uses [0.5, 0.25, 0.25] as probabilities.

        Returns
        -------
        Testset
            Testset object containing generated questions and answers.
        """
        print("Generating testset of size", n)
        if distribution is not None:
            if list(distribution.keys()) != ["simple", "multi_context", "reasoning"]:
                raise ValueError(
                    "Invalid distributions keys. Must be ['simple', 'multi_context', 'reasoning']"
                )

            ragas_dist = {
                simple: distribution["simple"],
                multi_context: distribution["multi_context"],
                reasoning: distribution["reasoning"],
            }
        else:
            ragas_dist = DEFAULT_DISTRIBUTION

        if self.source == "langchain":
            ret = self.generator.generate_with_langchain_docs(
                documents=self.documents, test_size=n, distributions=ragas_dist
            )
        else:
            ret = self.generator.generate_with_llamaindex_docs(
                documents=self.documents, test_size=n, distributions=ragas_dist
            )
        return ret.to_pandas().drop(columns=["episode_done"])


class ChaosAgent:
    """
    Given a test dataset, uses a specific type of perturbation to generate a new test dataset.
    """

    def __init__(self, testset):
        """
        Initialize the ChaosAgent object with a test dataset.

        Parameters
        ----------
        testset : DataFrame
            Test dataset to use for generating new questions.
            Must contain columns `question` and `ground_truth`.
        """
        self.testset = testset

    def generate(self, perturbation=None, agent_persona=None):
        """
        Generate new test dataset with a specific type of perturbation.

        Parameters
        ----------
        perturbation : str
            Type of perturbation to use. Must be `benign-paraphrases`, `adversarial-paraphrases`, `prompt-injection`.
            Defaults to a list conatining all types of perturbations.
        agent_persona : str
            For `adversarial paraphrases`, use this to specify persona of the agent to confuse
            when generating confusing questions. Defaults to `None`.

        Returns
        -------
        Testset
            Testset object containing generated questions and answers.
        """
        PERTURBATION_DICT = {
            "benign-paraphrases": "paraphrase.Realistic",
            "adversarial-paraphrases": "paraphrase.Confusing",
            "prompt-injection": "promptinject.GoalHijacking",
        }
        if perturbation is None:
            perturbation = PERTURBATION_DICT
        elif perturbation in list(PERTURBATION_DICT.keys()):
            perturbation = {perturbation: PERTURBATION_DICT[perturbation]}
        else:
            raise ValueError(
                f"Invalid perturbation. Must be one of {list(PERTURBATION_DICT.keys())}"
            )

        perturbed_testsets = []
        for pk, pv in perturbation.items():
            print(f"Generating perturbed testset with perturbation {pk}")
            pp_module = importlib.import_module(
                f"autoredteam.perturbations.{pv.split('.')[0].lower()}"
            )
            pp_instance = getattr(pp_module, pv.split(".")[1])()

            paraphrases = []
            for _, row in tqdm(self.testset.iterrows(), total=len(self.testset)):
                if "Confusing" in pv:
                    paraphrases.append(
                        pp_instance.perturb(
                            persona=agent_persona,
                            data={
                                "prompt": row["question"],
                                "context": row["ground_truth"],
                            },
                        )
                    )
                else:
                    paraphrases.append(pp_instance.perturb(prompt=row["question"]))

            # create a new testset with the paraphrases
            new_df = []
            for idx, row in tqdm(self.testset.iterrows(), total=len(self.testset)):
                for pp in paraphrases[idx]:
                    new_df_dict = {"question": pp}
                    for col in self.testset.columns:
                        if col != "question":
                            new_df_dict[col] = row[col]
                        else:
                            new_df_dict["original_question"] = row[col]
                    new_df_dict["perturbation"] = pk

                    new_df.append(new_df_dict)

            # add perturbation name and store
            perturbed_testsets.append(pd.DataFrame(new_df))

        return pd.concat(perturbed_testsets)
