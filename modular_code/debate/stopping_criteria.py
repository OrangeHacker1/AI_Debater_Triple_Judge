"""
    This file is used for checking if there is
    a consensus between models for x rounds.
    The default is 2. If both agents converge to the same conclusion,
    there is no need to continue running.
"""

def check_convergence(history, threshold=2):

    if len(history) < threshold:
        return False

    last = history[-threshold:]

    answers = [item["answer"] for item in last if "answer" in item]

    if len(answers) < threshold:
        return False

    return len(set(answers)) == 1
