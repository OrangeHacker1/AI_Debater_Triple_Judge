"""
Basic evaluation metrics
"""

# evaluation/metrics.py
"""
Basic evaluation metrics
"""

# evaluation/metrics.py
# evaluation/metrics.py

# evaluation/metrics.py

def accuracy(predictions):
    """
    Compute accuracy by comparing predicted answers to ground truth answers.
    
    Both the ground truth and prediction are normalized to a standard
    label before comparison:
        - "SUPPORTED", "Yes", "Y", "Agree" -> "agree"
        - "REFUTED", "No", "N", "Reject" -> "reject"
    
    Handles cases where the prediction may be nested in a dictionary 
    (e.g., judge verdicts stored as {"verdict": "..."}).

    Parameters:
    -----------
    predictions : list of dict
        Each dict must have keys for ground truth and prediction.

    Returns:
    --------
    float
        Accuracy as the fraction of correctly predicted answers.
    """
    def normalize(ans):
        if not ans:
            return ""
        ans = str(ans).strip().lower()
        if ans in ["supported", "yes", "y", "agree"]:
            return "agree"
        if ans in ["refuted", "no", "n", "reject"]:
            return "reject"
        return ans

    correct = 0
    for p in predictions:
        truth = p.get("truth") or p.get("ground_truth")
        pred = p.get("prediction") or p.get("judge") or p.get("judge_verdict")
        if isinstance(pred, dict):
            pred = pred.get("verdict")
        if truth is None or pred is None:
            continue
        if normalize(truth) == normalize(pred):
            correct += 1
    if len(predictions) == 0:
        print("ERROR:There were 0 predictions.")
        return 2.0
    return correct / len(predictions)

"""
Basic evaluation metrics for multi-agent debate system.

This module includes a robust accuracy function that:
- Handles predictions stored as strings or nested dictionaries.
- Normalizes answers to standard labels: "agree" or "reject".
- Ignores whitespace and capitalization differences.
"""


def accuracy11(predictions):
    """
    Compute accuracy by comparing predicted answers to ground truth answers.
    
    Both the ground truth and prediction are normalized to a standard
    label before comparison:
        - "SUPPORTED", "Yes", "Agree" -> "agree"
        - "REFUTED", "No", "Reject" -> "reject"
    
    Handles cases where the prediction may be nested in a dictionary 
    (e.g., judge verdicts stored as {"verdict": "..."}).

    Parameters:
    -----------
    predictions : list of dict
        Each dict must have keys for ground truth and prediction.
        Example entries:
        {
            "truth": "SUPPORTED",
            "prediction": "Yes"
        }
        or
        {
            "ground_truth": "REFUTED",
            "judge_verdict": {"verdict": "REFUTED", "confidence": 4}
        }

    Returns:
    --------
    float
        Accuracy as the fraction of correctly predicted answers.
    """

    def normalize(ans):
        """Normalize the answer to standard labels 'agree' or 'reject'."""
        if not ans:
            return ""
        ans = str(ans).strip().lower()
        if ans in ["supported", "yes", "agree"]:
            return "agree"
        if ans in ["refuted", "no", "reject"]:
            return "reject"
        return ans  # keep other text as-is for future metrics

    correct = 0

    for p in predictions:

        # Extract ground truth
        truth = p.get("truth") or p.get("ground_truth")

        # Extract prediction from multiple possible keys
        pred  = p.get("prediction") or p.get("judge") or p.get("judge_verdict")

        # If the prediction is a dictionary (like judge output), extract 'verdict'
        if isinstance(pred, dict):
            pred = pred.get("verdict")

        # Skip if either is missing
        if truth is None or pred is None:
            continue

        # Compare normalized labels
        if normalize(truth) == normalize(pred):
            correct += 1

    if len(predictions) == 0:
        return 0.0

    return correct / len(predictions)
"""
def accuracy(predictions):
    #"" "
    #Compute accuracy over a list of predictions.
    #Each element should have:
    #    - "truth" or "ground_truth"
    #    - "prediction" or "judge_verdict" (dict or string)
    #"" " 

    correct = 0

    for p in predictions:
        truth = p.get("truth") or p.get("ground_truth")
        pred = p.get("prediction")

        # If judge_verdict is a dict, extract "prediction"
        if pred is None and isinstance(p.get("judge_verdict"), dict):
            pred = p["judge_verdict"].get("prediction")

        if truth is None or pred is None:
            continue

        # Compare lowercase strings
        if str(truth).strip().lower() == str(pred).strip().lower():
            correct += 1

    return correct / len(predictions) if len(predictions) > 0 else 0
"""