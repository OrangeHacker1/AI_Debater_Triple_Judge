import json
import os

from baselines.direct_qa import direct_qa
from baselines.self_consistency import self_consistency

from evaluation.metrics import accuracy


def save_log(prefix, question, truth, prediction, config, extra=None):
    """
    Save baseline results to the same logging directory as debates.
    """

    log_path = config["logging"]["path"]

    os.makedirs(log_path, exist_ok=True)

    filename = os.path.join(
        log_path,
        f"{prefix}_{abs(hash(question))}.json"
    )

    data = {
        "method": prefix,
        "question": question,
        "ground_truth": truth,
        "prediction": prediction
    }

    if extra:
        data.update(extra)

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


def run_dataset(dataset_path, orchestrator, llm, config):

    with open(dataset_path, encoding="utf-8") as f:
        dataset = json.load(f)

    debate_results = []
    direct_results = []
    sc_results = []

    # Match debate compute budget
    debate_calls = config["debate"]["rounds"] * 2

    for item in dataset:

        q = item["question"]
        truth = item["answer"]

        # ---------------------------------
        # Debate System
        # ---------------------------------

        debate = orchestrator.run_debate(q, truth)

        debate_results.append({
            "truth": truth,
            "judge": debate["judge_verdict"]
        })

        # ---------------------------------
        # Direct QA Baseline
        # ---------------------------------

        direct = direct_qa(llm, q)

        direct_results.append({
            "truth": truth,
            "judge": direct
        })

        save_log(
            "direct_qa",
            q,
            truth,
            direct,
            config
        )

        # ---------------------------------
        # Self Consistency Baseline
        # ---------------------------------

        sc_answer, samples = self_consistency(llm, q, debate_calls)

        sc_results.append({
            "truth": truth,
            "judge": sc_answer
        })

        save_log(
            "self_consistency",
            q,
            truth,
            sc_answer,
            config,
            extra={"samples": samples}
        )

    # ---------------------------------
    # Print Results
    # ---------------------------------

    print("Debate Accuracy:", accuracy(debate_results))
    print("Direct QA Accuracy:", accuracy(direct_results))
    print("Self Consistency Accuracy:", accuracy(sc_results))