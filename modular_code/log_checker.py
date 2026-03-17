import os
import json
import argparse
from glob import glob


def normalize_answer(ans):
    """
    Normalize answers so they can be compared reliably.

    Mapping:
        Yes -> SUPPORTED
        No  -> REFUTED

    Also handles case differences and whitespace.
    """

    if ans is None:
        return None

    ans = str(ans).strip().lower()

    if ans in ["supported", "yes", "y", "agree"]:
        return "SUPPORTED"

    if ans in ["refuted", "no", "n", "reject"]:
        return "REFUTED"

    return ans.upper()


def extract_prediction(data, filename):
    """
    Extract prediction from different log formats.
    """

    # -----------------------------
    # Direct QA
    # -----------------------------
    if filename.startswith("direct_qa"):

        pred = data.get("prediction")

        if isinstance(pred, dict):
            pred = pred.get("prediction")

        return pred

    # -----------------------------
    # Self Consistency
    # -----------------------------
    if filename.startswith("self_consistency"):

        return data.get("prediction")

    # -----------------------------
    # Debate logs
    # -----------------------------
    if filename.startswith("debate"):

        verdict = data.get("judge_verdict")

        if isinstance(verdict, dict):
            return verdict.get("verdict")

        if isinstance(verdict, str):
            try:
                parsed = json.loads(verdict)
                return parsed.get("verdict")
            except Exception:
                return verdict

    return None


def compute_accuracy(results):
    """
    Compute accuracy safely.
    """

    if len(results) == 0:
        return 0.0

    correct = sum(results)
    return correct / len(results)


def check_logs(log_dir):
    """
    Main evaluation function.
    """

    debate_results = []
    direct_results = []
    sc_results = []

    files = glob(os.path.join(log_dir, "*.json"))

    if len(files) == 0:
        print("No JSON files found in:", log_dir)
        return

    for file in files:

        filename = os.path.basename(file)

        try:
            with open(file, "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception as e:
            print("Skipping bad file:", filename, "error:", e)
            continue

        truth = normalize_answer(data.get("ground_truth"))
        pred = normalize_answer(extract_prediction(data, filename))

        if truth is None or pred is None:
            continue

        correct = truth == pred

        if filename.startswith("direct_qa"):
            direct_results.append(correct)

        elif filename.startswith("self_consistency"):
            sc_results.append(correct)

        elif filename.startswith("debate"):
            debate_results.append(correct)

    results = {
        "debate_accuracy": compute_accuracy(debate_results),
        "direct_qa_accuracy": compute_accuracy(direct_results),
        "self_consistency_accuracy": compute_accuracy(sc_results),
        "debate_samples": len(debate_results),
        "direct_samples": len(direct_results),
        "self_consistency_samples": len(sc_results)
    }

    return results


def main():
    """
    CLI entry point.
    """

    parser = argparse.ArgumentParser(description="Check accuracy of debate log files")

    parser.add_argument(
        "--subfolder",
        type=str,
        default=None,
        help="Optional subfolder inside logs/debate_runs"
    )

    args = parser.parse_args()

    base_dir = os.path.join("logs", "debate_runs")

    if args.subfolder:
        log_dir = os.path.join(base_dir, args.subfolder)
    else:
        log_dir = base_dir

    print("Scanning folder:", log_dir)

    results = check_logs(log_dir)

    if results:
        print("\nAccuracy Results")
        print("-------------------------")
        print(json.dumps(results, indent=2))

# Usage: python log_checker.py
# Usage Subfolder: python log_checker.py --subfolder run_1
# Searches: logs/debate_runs/run_1/
if __name__ == "__main__":
    main()