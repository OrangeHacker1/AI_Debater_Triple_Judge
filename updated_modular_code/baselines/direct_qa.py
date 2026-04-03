#def direct_qa(llm, question):

    #Fact Verification is either REFUTED or SUPPORTED. # The final answer will either be 'REFUTED' or 'SUPPORTED'. #
    # Commonsence is either a Yes or a No. # The final answer will either be 'Yes' or 'No'. #

#    prompt = f"""
#Answer the question with step-by-step reasoning.
#The final answer will either be 'REFUTED' or 'SUPPORTED'.

#Question:
#{question}
#"""

#    return llm.query(prompt)

# direct_qa.py

# Original simple version (commented out)
# def direct_qa(llm, question):
#     """
#     Ask the LLM the question directly using Chain-of-Thought prompting.
#     Returns just a string answer.
#     """
#     prompt = f"Question: {question}\nAnswer:"
#     return llm.query(prompt)

# ----------------------------
# Updated version with separate prediction and reasoning
# ----------------------------

def direct_qa(llm, question):
    """
    Ask the LLM the question directly using Chain-of-Thought prompting.
    Returns a dictionary with 'prediction' (one-word answer) and 'reasoning'.
    """

    prompt = f"""
Answer the following question in ONE word for the final answer.
Provide reasoning separately under 'Reasoning:'.

Question:
{question}

Format:
Answer: <one word answer> "SUPPORTED" or "REFUTED"
Reasoning: <explanation in 1-3 sentences>
"""

    response = llm.query(prompt)

    # Extract prediction and reasoning
    prediction = None
    reasoning = None

    # Parse response safely
    if "Answer:" in response:
        prediction_part = response.split("Answer:")[1]
        if "Reasoning:" in prediction_part:
            prediction = prediction_part.split("Reasoning:")[0].strip()
            reasoning = prediction_part.split("Reasoning:")[1].strip()
        else:
            prediction = prediction_part.strip()
            reasoning = ""
    else:
        prediction = response.strip()
        reasoning = ""

    return {"prediction": prediction, "reasoning": reasoning}
