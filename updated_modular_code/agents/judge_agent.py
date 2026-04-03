#"""
# agents/judge_agent.py

import json

class JudgeAgent:

    def __init__(self, llm, prompt):
        self.llm = llm
        self.prompt = prompt

    def evaluate(self, question, transcript):

        full_prompt = self.prompt \
            .replace("{question}", question) \
            .replace("{transcript}", transcript)

        response = self.llm.query(full_prompt)

        # -----------------------------
        # Robust JSON parsing
        # -----------------------------
        try:
            parsed = json.loads(response)

            return {
                "verdict": parsed.get("verdict", "UNKNOWN"),
                "confidence": parsed.get("confidence", 0),
                "analysis": parsed.get("analysis", "").strip(), # Summary of the debate.
                "identification": parsed.get("identification", "").strip(), # Identify the strongest and weakest points on both sides.
                "reasoning": parsed.get("reasoning", "").strip()
            }
            

        except Exception:
            # Fallback if model outputs garbage
            return {
                "verdict": self.extract_verdict(response),
                "confidence": 0,
                "reasoning": str(response).strip()#response
            }

    def extract_verdict(self, text):
        text = str(text).upper()

        if "SUPPORTED" in text:
            return "SUPPORTED"
        if "REFUTED" in text:
            return "REFUTED"

        return "UNKNOWN"



"""
# agents/judge_agent.py
import json
class JudgeAgent:

    def __init__(self, llm, prompt):

        self.llm = llm
        self.prompt = prompt


    def evaluate(self, question, transcript):

        # Convert transcript to string if needed
        #transcript_str = str(transcript)
        transcript_str = json.dumps(transcript, indent=2)
        # Replace only the intended variables
        formatted = self.prompt \
            .replace("{question}", question) \
            .replace("{transcript}", transcript_str)

        response = self.llm.query(formatted)

        return response
        #"""
