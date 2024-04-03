import contextlib
from .base import Perturbation
import garak.buffs.paraphrase as pp_buff
from consistencybench.perturbations.paraphrase import llm_prompting
from langchain_openai import ChatOpenAI
from ..agents.openai import OpenaiAgent
from .utils import INPUT_TEMPLATE, ISSUE

"""This module contains perturbations that generate paraphrases of a prompt or prompts in a test."""

# this = sys.modules[__name__]


class PegasusT5(Perturbation):
    """Perturbations that generate paraphrases of a prompt or prompts in a test."""

    name = "paraphrase.PegasusT5"
    description = "Paraphrase perturbation using PegasusT5"

    def __init__(self, num_paraphrases=6):
        self.num_paraphrases = num_paraphrases
        with contextlib.redirect_stdout(None):
            self.buff = pp_buff.PegasusT5()
        self.buff.num_return_sequences = self.num_paraphrases
        self.buff.num_beams = self.num_paraphrases
        self.uri = self.buff.uri
        self.__doc__ = self.buff.__doc__

        super().__init__()

    def perturb(self, prompt: str):
        return self.buff._get_response(prompt)


class Realistic(Perturbation):
    """Generate realistic paraphrases using guided prompting to an LLM."""

    name = "paraphrase.Realistic"
    description = (
        "Realistic paraphrase perturbation using LLM, uses the consistencybench library"
    )
    tags = ["vijil:Hallucination"]

    def __init__(self, num_paraphrases=6, pp_model_name="gpt-3.5-turbo"):
        self.pp_agent = ChatOpenAI(model_name=pp_model_name)
        super().__init__(num_paraphrases)

    def perturb(self, prompt: str):
        return [
            llm_prompting(input=prompt, method=i, llm=self.pp_agent) for i in range(5)
        ]


class Confusing(Perturbation):
    """Generate confusing paraphrases using guided prompting to an LLM."""

    name = "paraphrase.Confusing"
    description = "Confusing paraphrase perturbation using LLM"
    tags = ["vijil:Robustness"]

    def __init__(self, num_paraphrases=6, pp_model_name="gpt-3.5-turbo"):
        self.num_paraphrases = num_paraphrases
        # self.pp_agent = ChatOpenAI(model_name=pp_model_name)
        self.pp_agent = OpenaiAgent(
            name=pp_model_name, generations=self.num_paraphrases
        )
        super().__init__(num_paraphrases)

    def perturb(self, persona, data):
        inputs = INPUT_TEMPLATE.format(
            question=data["prompt"],
            answer=data["context"],
            issue_description=ISSUE,
            model_name=persona,
        )
        return self.pp_agent.generate(inputs)


# # TODO: make Fast work
# buff_list = ["PegasusT5", "Fast"]
# for buff_name in buff_list:
#     buff_instance = getattr(buff_module, buff_name)()

#     setattr(
#         this,
#         buff_name,
#         type(
#             buff_name,
#             (Perturbation,),
#             {
#                 "__init__": local_constructor,
#                 "__doc__": buff_instance.__doc__,
#                 "buff": buff_instance,
#                 "uri": buff_instance.uri,
#                 "num_return_sequences": buff_instance.num_return_sequences,
#                 "num_beams": buff_instance.num_beams,
#                 "perturb": perturb
#             },
#         ),
#     )
