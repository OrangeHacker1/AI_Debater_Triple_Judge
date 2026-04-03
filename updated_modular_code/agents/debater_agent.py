# agents/debater_agent.py

import json

# Class for running debates
class DebaterAgent:

    def __init__(self, name, llm, prompts):
        self.name = name
        self.llm = llm
        self.prompts = prompts


    """def initial_position(self, question):

        prompt = self.prompts["initial"].replace(
            "{question}", question
        )

        return self.llm.query(prompt)"""

    def initial_position_A(self, question):

        prompt = self.prompts["initial_A"].replace(
            "{question}", question
        )

        return self.llm.query(prompt)
    
    def initial_position_B(self, question):

        prompt = self.prompts["initial_B"].replace(
            "{question}", question
        )

        return self.llm.query(prompt)


    def argument(self, question, transcript):

        transcript_str = json.dumps(transcript, indent=2)

        prompt = self.prompts["argument"] \
            .replace("{question}", question) \
            .replace("{transcript}", transcript_str)

        return self.llm.query(prompt)


    def counter(self, question, transcript):

        transcript_str = json.dumps(transcript, indent=2)#str(transcript)

        prompt = self.prompts["counter"] \
            .replace("{question}", question) \
            .replace("{transcript}", transcript_str)

        return self.llm.query(prompt)
       # """
