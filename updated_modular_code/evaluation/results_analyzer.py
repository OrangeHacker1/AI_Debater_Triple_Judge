import os
import json
import matplotlib.pyplot as plt


LOG_DIR = "logs"
RESULT_DIR = "results"

os.makedirs(RESULT_DIR, exist_ok=True)


def extract_answer(text):

    if "Answer:" in text:
        return text.split("Answer:")[1].split("\n")[0].strip()

    return text.strip()


def compute_accuracy():

    debate_correct = 0
    debate_total = 0

    direct_correct = 0
    direct_total = 0

    sc_correct = 0
    sc_total = 0

    for file in os.listdir(LOG_DIR):

        path = os.path.join(LOG_DIR, file)

        with open(path) as f:
            data = json.load(f)

        truth = data.get("ground_truth")

        pred = data.get("prediction") or data.get("judge_verdict")

        if pred:
            pred = extract_answer(pred)

        if file.startswith("debate"):

            debate_total += 1

            if truth.lower() in pred.lower():
                debate_correct += 1

        elif file.startswith("direct_qa"):

            direct_total += 1

            if truth.lower() in pred.lower():
                direct_correct += 1

        elif file.startswith("self_consistency"):

            sc_total += 1

            if truth.lower() in pred.lower():
                sc_correct += 1

    results = {
        "Debate": debate_correct / debate_total if debate_total else 0,
        "Direct QA": direct_correct / direct_total if direct_total else 0,
        "Self Consistency": sc_correct / sc_total if sc_total else 0
    }

    return results


def plot_results():

    results = compute_accuracy()

    methods = list(results.keys())
    scores = list(results.values())

    plt.figure()

    plt.bar(methods, scores)

    plt.ylabel("Accuracy")

    plt.title("Debate vs Baselines")

    plt.savefig(os.path.join(RESULT_DIR, "accuracy_plot.png"))

    plt.close()


if __name__ == "__main__":

    plot_results()

    print("Plots saved to results/")