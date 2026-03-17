import json
import os
from debate.stopping_criteria import check_convergence

debate = 1

class DebateOrchestrator:

    def __init__(self, debaterA, debaterB, judge, config):

        self.A = debaterA
        self.B = debaterB
        self.judge = judge
        self.config = config


    def run_debate(self, question, truth=None):

        print(f"Debate: {debate}")
        globals()["debate"] += 1
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
        if answerA == answerB:
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

        verdict = self.judge.evaluate(question, transcript_str)

        result = {
            "question": question,
            "ground_truth": truth,
            "consensus": consensus,
            "transcript": transcript,
            "judge_verdict": verdict
        }

        self.save_log(result)

        return result

    def extract_answer(self, response):
        if isinstance(response, dict):
            return response.get("answer", "SUPPORTED")
        return "SUPPORTED"
    """
    def extract_answer(self, text):

        if "Answer:" in text:
            return text.split("Answer:")[1].split("\n")[0].strip()

        return text.strip()
    """

    def save_log(self, result):

        path = self.config["logging"]["path"]

        os.makedirs(path, exist_ok=True)

        filename = os.path.join(
            path,
            f"debate_{abs(hash(result['question']))}.json"
        )

        with open(filename, "w", encoding="utf-8") as f:
            json.dump(result, f, indent=2)