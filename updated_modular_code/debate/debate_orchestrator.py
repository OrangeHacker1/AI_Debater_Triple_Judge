import json
import os
from debate.stopping_criteria import check_convergence

debate = 1

class DebateOrchestrator:

    def __init__(self, debaterA, debaterB, judge, config):

        self.A = debaterA
        self.B = debaterB
        self.judge = judge # Judge Panel
        self.config = config


    def run_debate(self, question, truth=None):

        print(f"Debate: {debate}")
        #debate = debate +1
        transcript = []
        history = []
        consensus = False

        # ----------------------------
        # Phase 1 — Initial positions
        # ----------------------------

        initA = self.A.initial_position_A(question)
        initB = self.B.initial_position_B(question)

        answerA = self.extract_answer(initA)
        answerB = self.extract_answer(initB)

        transcript.append({
            "agent": "A",
            "type": "initial",
            "answer": answerA,
            "argument": initA
        })

        transcript.append({
            "agent": "B",
            "type": "initial",
            "answer": answerB,
            "argument": initB
        })

        # Check immediate consensus
        if answerA is not None and answerB is not None and answerA == answerB:
            consensus = True

        # ----------------------------
        # Phase 2 — Debate Rounds
        # ----------------------------

        if not consensus:

            for r in range(self.config["debate"]["rounds"]):

                print(f"Round {r+1}")

                # Debater A argument
                argA = self.A.argument(question, transcript)
                answerA = self.extract_answer(argA)

                recordA = {
                    "agent": "A",
                    "round": r+1,
                    "answer": answerA,
                    "argument": argA
                }

                transcript.append(recordA)
                history.append(recordA)

                # Debater B counterargument
                argB = self.B.counter(question, transcript)
                answerB = self.extract_answer(argB)

                recordB = {
                    "agent": "B",
                    "round": r+1,
                    "answer": answerB,
                    "argument": argB
                }

                transcript.append(recordB)
                history.append(recordB)

                # Check convergence
                if check_convergence(history):
                    print("Debaters converged. Ending debate early.")
                    break


        # Convert transcript to string for judge
        transcript_str = json.dumps(transcript, indent=2)

        # ----------------------------
        # Phase 3 — Judge Evaluation
        # ----------------------------


        # Modify for triple Judge
        verdict = self.judge.evaluate(question, transcript_str)

        result = {
            "question": question,
            "ground_truth": truth,
            "consensus": consensus,
            "transcript": transcript,

            # Final answers
            "judge_verdict": verdict["judges"][0], # First Judge Response
            "judge_panel_verdict": verdict["final_verdict"], # Judge Pooling

            # Panel details
            "judge_panel": verdict,

            # NEW: Direct reasoning access
            "judge_reasonings": verdict["reasonings"]
        }

        self.save_log(result)
        globals()["debate"] += 1
        return result


    def extract_answer(self, response):
        """
        Extract answer from LLM JSON output safely.
        """

        if response is None:
            return None

        # If already dict
        # Check for type.
        if isinstance(response, dict):
            return response.get("answer")

        # If string → try parsing JSON
        if isinstance(response, str):
            try:
                parsed = json.loads(response)
                return parsed.get("answer")
            except Exception:
                # fallback: try to detect manually
                text = response.lower()
                if "supported" in text:
                    return "SUPPORTED"
                if "refuted" in text:
                    return "REFUTED"

        return None


    def save_log(self, result):

        path = self.config["logging"]["path"]

        os.makedirs(path, exist_ok=True)

        filename = os.path.join(
            path,
            #f"debate_{abs(hash(result['question']))}.json"
            f"debate_{debate}.json"
        )

        with open(filename, "w", encoding="utf-8") as f:
            json.dump(result, f, indent=2)
