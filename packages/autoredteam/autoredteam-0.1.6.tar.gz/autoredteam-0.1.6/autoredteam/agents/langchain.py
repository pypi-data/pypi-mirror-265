import contextlib
from garak.generators.langchain import LangChainLLMGenerator
from ..engine.config import _get_default_agent_config


class LangChainAgent(LangChainLLMGenerator):
    def __init__(self, name, generations: int = 10):
        # TODO
        # The env variable will  have to be set outside because the model
        # that is pulled is dependant on the provider. Langchain uses its own
        # os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_TOKEN")

        self.family = "LangChain"
        print(f"Loading {self.family} Agent: {name}")
        with contextlib.redirect_stdout(None):
            super().__init__(name, generations=generations)
        # if config is None:
        config = _get_default_agent_config(family="", name=self.name)
        for field in [
            "max_tokens",
            "presence_penalty",
            "temperature",
            "top_k",
            "seed",
            "presence_penalty",
            # "supports_multiple_generations",
        ]:
            if hasattr(config, field):
                setattr(self, field, getattr(config, field))


default_class = "LangChainAgent"
