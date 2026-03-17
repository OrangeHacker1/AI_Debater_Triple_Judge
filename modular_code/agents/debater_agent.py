# agents/debater_agent.py

import json
"""
class DebaterAgent:

    def __init__(self, name, llm, prompts):
        self.name = name
        self.llm = llm
        self.prompts = prompts

    def initial_position(self, question):
        prompt = self.prompts["initial"].format(question=question)
        response = self.llm.query(prompt)
        return self._parse_json(response)

    def argument(self, question, transcript):
        prompt = self.prompts["argument"].format(
            question=question,
            transcript=transcript
        )
        response = self.llm.query(prompt)
        return self._parse_json(response)

    def counter(self, question, transcript):
        prompt = self.prompts["counter"].format(
            question=question,
            transcript=transcript
        )
        response = self.llm.query(prompt)
        return self._parse_json(response)

    def _parse_json(self, text):
        """"""
        Parse the JSON response from the LLM.
        Ensures 'answer' is only SUPPORTED or REFUTED.
        """ """
        try:
            data = json.loads(text)
            answer = data.get("answer", "").upper()
            if answer not in ["SUPPORTED", "REFUTED"]:
                # fallback if LLM doesn't follow rules
                answer = "SUPPORTED"
            argument = data.get("argument", "")
            return {"answer": answer, "argument": argument}
        except json.JSONDecodeError:
            # fallback if LLM returns malformed text
            return {"answer": "SUPPORTED", "argument": text}

"""
# Class for running debates
class DebaterAgent:

    def __init__(self, name, llm, prompts):
        self.name = name
        self.llm = llm
        self.prompts = prompts


    def initial_position(self, question):

        prompt = self.prompts["initial"].replace(
            "{question}", question
        )

        return self.llm.query(prompt)


    def argument(self, question, transcript):

        transcript_str = str(transcript)

        prompt = self.prompts["argument"] \
            .replace("{question}", question) \
            .replace("{transcript}", transcript_str)

        return self.llm.query(prompt)


    def counter(self, question, transcript):

        transcript_str = str(transcript)

        prompt = self.prompts["counter"] \
            .replace("{question}", question) \
            .replace("{transcript}", transcript_str)

        return self.llm.query(prompt)
       # """