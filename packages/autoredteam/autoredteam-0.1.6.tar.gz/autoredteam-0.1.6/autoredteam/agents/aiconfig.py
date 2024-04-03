from typing import List
from autoredteam.agents.base import Agent
from autoredteam.agents.anyscale import AnyscaleAPI
from autoredteam.agents.openai import OpenaiAgent


class AIConfigAgent(Agent):
    """
    The AIConfigAgent class is a wrapper for agents created through [AIConfig](https://aiconfig.lastmileai.dev/).

    Currently supports LLMs-as-agents hosted in OpenAI and Anyscale.
    """

    def __init__(self, name, provider, generations):
        """
        Initializes the Agent class.
        Args:
            name (str): The name of the agent.
            provider (str): The provider of the agent.
            generations (int): The number of generations to use.
        """
        self.name = name
        self.provider = provider
        self.generations = generations
        self.model = None
        self.fullname = "autoredteam.agents.aiconfig.AIConfigAgent"

        try:
            if self.provider == "Anyscale":
                self.model = AnyscaleAPI(name=name, generations=self.generations)
            elif self.provider == "OpenAI":
                self.model = OpenaiAgent(name=name, generations=self.generations)
            else:
                raise ValueError("Invalid provider specified.")
        except Exception as e:
            print(f"An error occurred during initialization: {e}")

    def _call_model(self, prompt: str) -> List[str] | str | None:
        """Calls the agent with the given prompt.

        Args:
            prompt (str): The prompt to send to the agent.

        Returns:
            List[str]: The response(s) from the agent.
        """
        return self.model._call_model(prompt)
