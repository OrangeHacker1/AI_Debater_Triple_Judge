# agents/judge_agent.py

class JudgeAgent:

    def __init__(self, llm, prompt):

        self.llm = llm
        self.prompt = prompt


    def evaluate(self, question, transcript):

        """
        Evaluates a debate transcript and returns the judge's verdict.
        """

        # Convert transcript to string if needed
        transcript_str = str(transcript)

        # Replace only the intended variables
        formatted = self.prompt \
            .replace("{question}", question) \
            .replace("{transcript}", transcript_str)

        response = self.llm.query(formatted)

        return response