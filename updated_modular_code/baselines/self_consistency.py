from collections import Counter

def self_consistency(llm, question, n_samples):
    """
    Self-Consistency baseline:
    - Sample the LLM 'n_samples' times
    - Extract answer from each response
    - Return the majority vote and all samples for logging
    # Fact Verification is either REFUTED or SUPPORTED. # The final answer will either be 'REFUTED' or 'SUPPORTED'. #
    """

    samples = []

    for _ in range(n_samples):

        prompt = f"""
Answer the question using step-by-step reasoning.
The final answer will either be 'REFUTED' or 'SUPPORTED'.

Question:
{question}

Format:
Answer:
Reasoning:
"""

        # Use query(), not generate()
        response = llm.query(prompt)

        # Extract the answer
        if "Answer:" in response:
            answer = response.split("Answer:")[1].split("\n")[0].strip()
        else:
            answer = response.strip()

        samples.append(answer)

    # Take majority vote
    majority_vote = Counter(samples).most_common(1)[0][0]

    return majority_vote, samples