import os
import json
import argparse
from glob import glob
import matplotlib.pyplot as plt


# --------------------------------------------------
# Normalize answers
# --------------------------------------------------

def normalize_answer(ans):
    """
    Normalize answers so they can be compared reliably.

    Mapping:
        Yes -> SUPPORTED
        No  -> REFUTED
    """

    if ans is None:
        return None

    ans = str(ans).strip().lower()

    if ans in ["supported", "yes", "y", "agree"]:
        return "SUPPORTED"

    if ans in ["refuted", "no", "n", "reject"]:
        return "REFUTED"

    return ans.upper()


# --------------------------------------------------
# Extract predictions from different log formats
# --------------------------------------------------

def extract_prediction(data, filename):

    # Direct QA
    if filename.startswith("direct_qa"):

        pred = data.get("prediction")

        if isinstance(pred, dict):
            pred = pred.get("prediction")

        return pred

    # Self-consistency
    if filename.startswith("self_consistency"):

        return data.get("prediction")

    # Debate
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

# Only use on debate files with a Judge_Panels. 
def extract_panel_prediction(data, filename):
    verdict_panel = None
    if filename.startswith("debate"):
        verdict_panel = data.get("judge_panel_verdict")

    return verdict_panel

# --------------------------------------------------
# Compute accuracy
# --------------------------------------------------

def compute_accuracy(results):

    if len(results) == 0:
        return 0.0

    correct = sum(results)
    return correct / len(results)


# --------------------------------------------------
# Plot results
# --------------------------------------------------

def plot_results(results, save_path):

    methods = [
        "Debate",
        "Debate Panel",
        "Direct QA",
        "Self Consistency"
    ]

    scores = [
        results["debate_accuracy"],
        results["debate_panel_accuracy"],
        results["direct_qa_accuracy"],
        results["self_consistency_accuracy"]
    ]

    plt.figure()

    plt.bar(methods, scores)

    plt.title("Debate vs Baseline Accuracy")
    plt.ylabel("Accuracy")
    plt.ylim(0, 1)

    plt.savefig(save_path)
    plt.close()

    print("Saved accuracy plot to:", save_path)


# --------------------------------------------------
# Main log checker
# --------------------------------------------------

def check_logs(log_dir):

    debate_results = []
    direct_results = []
    sc_results = []
    debate_panel_results = []

    misclassified = []

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

        # Save misclassified examples
        if not correct:
            misclassified.append({
                "file": filename,
                "question": data.get("question"),
                "truth": truth,
                "prediction": pred
            })

        if filename.startswith("direct_qa"):
            direct_results.append(correct)

        elif filename.startswith("self_consistency"):
            sc_results.append(correct)

        elif filename.startswith("debate"):
            debate_results.append(correct)
            # If there is a debate, you need to grab the judge pannel as well. Call a second helper function.
            #HELPER FUNCTION for judge_panel_verdict.
            pred_panel = normalize_answer(extract_panel_prediction(data, filename))
            debate_panel_results.append(pred_panel == truth)

    results = {
        "debate_accuracy": compute_accuracy(debate_results),
        "debate_panel_accuracy": compute_accuracy(debate_panel_results),
        "direct_qa_accuracy": compute_accuracy(direct_results),
        "self_consistency_accuracy": compute_accuracy(sc_results),
        "debate_samples": len(debate_results),
        "direct_samples": len(direct_results),
        "self_consistency_samples": len(sc_results)
    }

    return results, misclassified


# --------------------------------------------------
# Print misclassified examples
# --------------------------------------------------

def print_misclassified(misclassified):

    if len(misclassified) == 0:
        print("\nNo misclassified examples.")
        return

    print("\nMisclassified Examples")
    print("---------------------------------\n")

    for item in misclassified[:20]:  # limit to first 20

        print("File:", item["file"])
        print("Question:", item["question"])
        print("Truth:", item["truth"])
        print("Prediction:", item["prediction"])
        print()


# --------------------------------------------------
# CLI entry point
# --------------------------------------------------

def main():

    parser = argparse.ArgumentParser(description="Check accuracy of debate logs")

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

    results, misclassified = check_logs(log_dir)

    print("\nAccuracy Results")
    print("---------------------------------")
    print(json.dumps(results, indent=2))

    print_misclassified(misclassified)

    plot_path = os.path.join(log_dir, "accuracy_plot.png")
    plot_results(results, plot_path)

# Usage: python log_checker.py
# Usage Subfolder: python log_checker.py --subfolder run_1
# Searches: logs/debate_runs/run_1/
if __name__ == "__main__":
    main()
