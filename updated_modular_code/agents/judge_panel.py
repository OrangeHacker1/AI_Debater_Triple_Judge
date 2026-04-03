"""
    Have three agents vote to come to a conclusion.
"""
# evaluation/judge_panel.py

from collections import Counter

class JudgePanel:

    def __init__(self, judge_agents):
        """
        judge_agents: list of JudgeAgent instances
        """
        self.judges = judge_agents

    def evaluate(self, question, transcript):

        results = []
        for i, judge in enumerate(self.judges):

            res = judge.evaluate(question, transcript)

            results.append({
                "judge_id": i,
                "verdict": res.get("verdict", "UNKNOWN"),
                "confidence": res.get("confidence", 0),
                "reasoning": res.get("reasoning", "")
            })

        # -----------------------------
        # Voting
        # -----------------------------
        votes = [r["verdict"] for r in results if r["verdict"] != "UNKNOWN"]

        if len(votes) == 0:
            final = "UNKNOWN"
        else:
            final = Counter(votes).most_common(1)[0][0]

        # -----------------------------
        # Agreement score
        # -----------------------------
        agreement = votes.count(final) / len(votes) if votes else 0

        return {
            "final_verdict": final,
            "agreement": agreement,
            "num_judges": len(self.judges),

            # Clean structured outputs
            "judges": results,  # full detail

            # Convenience fields (VERY useful)
            "reasonings": [r["reasoning"] for r in results],
            "verdicts": [r["verdict"] for r in results]
        }
