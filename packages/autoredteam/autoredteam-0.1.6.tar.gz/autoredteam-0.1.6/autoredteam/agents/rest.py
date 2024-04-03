import os
import requests
from .base import Agent


class RestAPI(Agent):
    """
    Generic class to instantiate Agent based on an URL and API token.
    Details of prompt and response handling are added to a dict and supplied as input.
    """

    # def __init__(self, name, config: AgentConfig=None):
    def __init__(self, config, generations: int = 10):
        """
        Initializes the Agent class, given a configuration and number of generations.
        
        Args:
            config (dict): The configuration of the agent.
            generations (int): The number of generations to run the agent.
        """

        print("Loading REST Agent: ", config["name"])
        self.family = "REST"

        # check for the environment variable
        if config["token_name"] not in os.environ:
            raise ValueError(
                f"Put the {self.family} API token in the {config['token_name']} environment variable\n \
                e.g.: export {config['token_name']}='abc123'"
            )
        os.environ["REST_API_TOKEN"] = os.getenv(config["token_name"])

        self.config = config
        self.generations = generations
        self.fullname = "autoredteam.agents.rest.RestAPI"

        # define response parser
        exec(self.config["output_handler"])
        self.parse = locals()["parse"]

    def _call_model(self, prompt: str):
        """
        Calls the agent with the given prompt.
        
        Args:
            prompt (str): The prompt to send to the agent.
            
        Returns:
            str: The response from the agent.
        """

        # add prompt to payload
        payload = self.config["prompt_handler"].copy()
        for k, v in payload.items():
            if isinstance(v, str) and "$PROMPT" in v:
                payload[k] = v.replace("$PROMPT", prompt)

        response = requests.post(
            self.config["url"],
            headers={
                "Accept": "application/json",
                "Authorization": f"""Bearer {os.environ["REST_API_TOKEN"]}""",
                "Content-Type": "application/json",
            },
            json=payload,
        )
        # return response
        return self.parse(response)

default_class = "RestAPI"