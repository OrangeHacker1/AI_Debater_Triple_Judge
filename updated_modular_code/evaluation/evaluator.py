import json
import os
from collections import Counter
from glob import glob

from evaluation.metrics import accuracy
from config.config_loader import load_config


class Evaluator:
    """
    Evaluator for multi-agent debate system.

    This class:
    - Runs debates and baseline methods (Direct QA, Self-Consistency)
    - Normalizes answers to standardized labels for robust accuracy
    - Logs outputs and reasoning for analysis
    - Can compute metrics from previously saved logs without calling LLM
    """

    def __init__(self, llm, config):
        self.llm = llm
        self.config = config
        self.log_path = config["logging"]["path"]
        os.makedirs(self.log_path, exist_ok=True)

    

    # ------------------------------------------------
    # Utility
    # ------------------------------------------------
    def extract_answer(self, text):
        """Extracts answer from LLM output if formatted with 'Answer:'"""
        if "Answer:" in text:
            return text.split("Answer:")[1].split("\n")[0].strip()
        return text.strip()

    def save_log(self, prefix, data):
        """Save JSON log of predictions/reasoning"""
        filename = os.path.join(
            self.log_path,
            f"{prefix}_{abs(hash(data['question']))}.json"
        )
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

    # ------------------------------------------------
    # Normalize answer labels
    # ------------------------------------------------
    @staticmethod
    def normalize_answer(ans):
        """
        Map multiple answer forms to standardized labels: 'agree' or 'reject'.
        Handles:
            - 'SUPPORTED', 'Yes', 'Y' -> 'agree'
            - 'REFUTED', 'No', 'N' -> 'reject'
        """
        if not ans:
            return ""
        ans_lower = str(ans).strip().lower()
        if ans_lower in ["supported", "yes", "y", "agree"]:
            return "agree"
        if ans_lower in ["refuted", "no", "n", "reject"]:
            return "reject"
        return ans_lower  # fallback, keep other text

    # ------------------------------------------------
    # Direct QA Baseline
    # ------------------------------------------------
    def direct_qa(self, question):
        """Run direct QA baseline with LLM"""
        prompt = f"""
Answer the following question.

Question:
{question}

Format:
Answer:
Reasoning:
"""
        response = self.llm.query(prompt)
        return response

    # ------------------------------------------------
    # Self-Consistency Baseline
    # ------------------------------------------------
    def self_consistency(self, question, itterations=3):
        """Run self-consistency baseline with multiple LLM calls"""
        samples = []
        n = self.config["debate"]["rounds"] * itterations

        for _ in range(n):
            prompt = f"""
Answer the question using step-by-step reasoning.

Question:
{question}

Format:
Answer:
Reasoning:
"""
            response = self.llm.query(prompt)
            answer = self.extract_answer(response)
            samples.append(answer)

        # Take majority vote
        vote = Counter(samples).most_common(1)[0][0]
        return vote, samples

    # ------------------------------------------------
    # Dataset Evaluation (live)
    # ------------------------------------------------
    def evaluate_dataset(self, dataset, orchestrator):
        """
        Evaluate all questions in the dataset:
        - Debate system
        - Direct QA baseline
        - Self-consistency baseline
        """
        debate_results = []
        direct_results = []
        sc_results = []

        for item in dataset:
            question = item["question"]
            truth = self.normalize_answer(item["answer"])

            # ----------------------
            # Debate
            # ----------------------
            debate = orchestrator.run_debate(question, truth)
            if isinstance(debate["judge_verdict"], dict):
                debate_answer = self.normalize_answer(debate["judge_verdict"].get("verdict", ""))
            else:
                debate_answer = self.normalize_answer(debate["judge_verdict"])
            debate_results.append({"truth": truth, "judge": debate_answer})

            # ----------------------
            # Direct QA
            # ----------------------
            direct = self.direct_qa(question)
            direct_answer = ""
            direct_reasoning = ""
            try:
                direct_json = json.loads(direct)
                direct_answer = self.normalize_answer(direct_json.get("answer", ""))
                direct_reasoning = direct_json.get("reasoning", "").strip()
            except json.JSONDecodeError:
                direct_answer = self.normalize_answer(self.extract_answer(direct))
                direct_reasoning = direct.strip()

            direct_log = {
                "method": "direct_qa",
                "question": question,
                "ground_truth": truth,
                "prediction": direct_answer,
                "reasoning": direct_reasoning
            }
            self.save_log("direct_qa", direct_log)
            direct_results.append({"truth": truth, "judge": direct_answer})

            # ----------------------
            # Self-Consistency
            # ----------------------
            sc_answer, samples = self.self_consistency(question)
            sc_answer_str = self.normalize_answer(sc_answer)
            sc_reasoning_list = []

            for s in samples:
                try:
                    sj = json.loads(s)
                    sc_reasoning_list.append(sj.get("reasoning", "").strip())
                except:
                    sc_reasoning_list.append(s.strip())

            sc_log = {
                "method": "self_consistency",
                "question": question,
                "ground_truth": truth,
                "prediction": sc_answer_str,
                "samples_reasoning": sc_reasoning_list
            }
            self.save_log("self_consistency", sc_log)
            sc_results.append({"truth": truth, "judge": sc_answer_str})

        # Compute metrics using normalized answers
        results = {
            "debate_accuracy": accuracy(debate_results),
            "direct_qa_accuracy": accuracy(direct_results),
            "self_consistency_accuracy": accuracy(sc_results)
        }
        return results

    # ------------------------------------------------
    # Evaluate from logs (no LLM calls)
    # ------------------------------------------------
    def evaluate_from_logs(self, log_dir=None):
        """
        Load all JSON logs from a directory and compute accuracy.
        Useful to re-evaluate without rerunning the LLM.
        """
        if log_dir is None:
            log_dir = self.log_path

        debate_results = []
        direct_results = []
        sc_results = []

        # Load all JSON files
        files = glob(os.path.join(log_dir, "*.json"))
        for fpath in files:
            with open(fpath, "r", encoding="utf-8") as f:
                data = json.load(f)

            pred = data.get("prediction")
            truth = data.get("ground_truth")
            method = data.get("method", "")

            if method.lower() == "direct_qa":
                direct_results.append({"truth": truth, "judge": pred})
            elif method.lower() == "self_consistency":
                sc_results.append({"truth": truth, "judge": pred})
            else:
                # Assume debate logs
                debate_results.append({"truth": truth, "judge": pred})

        results = {
            "debate_accuracy": accuracy(debate_results),
            "direct_qa_accuracy": accuracy(direct_results),
            "self_consistency_accuracy": accuracy(sc_results)
        }

        return results

    # ------------------------------------------------
    # Dataset loader
    # ------------------------------------------------
    def load_dataset(self, path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)


# ------------------------------------------------
# Main: run evaluator from logs directly
# ------------------------------------------------
if __name__ == "__main__":
    # Load config
    config = load_config()

    # LLM is None since we just want to read logs
    evaluator = Evaluator(llm=None, config=config)

    results = evaluator.evaluate_from_logs()
    print("Evaluation from saved logs:")
    print(json.dumps(results, indent=2))