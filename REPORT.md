# Methodology
For this project, several different files were created to generate a modular code that can be broken up and change to fit the needs of the assignment.
While building this assignment, there wre several issues that had to be addressed and fixed. This will be talked about in the Experiments section.

There are three types of LLM prompting methods. The first is the **Debate** mwthod, **Direct QA** method, and **Self Consistency**.


# Experiments

There are two major tests to complete this project. The first is a fact_verification dataset. The second is based on commonsense_qa dataset.

The initial tests of this project ran into certian issues. Debates were rare between the agents since they almost always had the same stance. In order to complete the assignment, this will be implimented as required, but I was working on another variation of the assignment that would force the second agent to take the opisite stance if there was a consence. This would force the agents to better debate their stances. Another idea involved using different models to help create friction.

## Fact Verification

Accuracy Results:

- "debate_accuracy": 0.65
-  "direct_qa_accuracy": 0.65
-  "self_consistency_accuracy": 0.62
-  "debate_samples": 100
-  "direct_samples": 100
-  "self_consistency_samples": 100


Accuracy Graph:
![Fact Verification Graph 1](fact_verification_accuracy_plot_1.png "Fact Verification Graph 1")


## Commonsense Q/A Results
xxx

# Analysis

Looking at the Fact Varification section, it was found that there was a 65% accuracy with the debate models. This was due to issues with conflict.
Rather than generating different results, both models were roughly the same.
Another detail that happened in a viriety of examples, was the Judge taking the opisite stance of the debating agents. Despite there being a consensus, the judge would ignore this, citing different evidence that would disprove their case and would lead it to select the opisite stance.


# Prompt Engineering

Initial Debate Prompt:
"
You are a debating agent.

Answer the question and provide reasoning.

Return your response ONLY in JSON format:

{
  "answer": "one word answer",
  "argument": "short explanation supporting your answer"
}

Rules:
- The answer must be either be "REFUTED" or "SUPPORTED".
- Do NOT include chain-of-thought reasoning in the answer.
- Do NOT include <think> blocks in the answer.
- Keep the argument under 10 sentences.
- Think blocks can only be added in the argument section.

Question:
{question}
"

Argument Debate Prompt:
"
You are continuing a debate.

Return JSON only:

{
  "answer": "your final answer",
  "argument": "your rebuttal to the other debater"
}

Rules:
- The answer must be either be "REFUTED" or "SUPPORTED".
- Do NOT include chain-of-thought reasoning in the "answer".
- Do NOT include <think> blocks in the "answer".
- Keep the argument under 10 sentences.
- Think blocks can only be added in the "argument" section.

Question:
{question}

Debate so far:
{transcript}
"


Debate Counter Prompt:
"
You are Debater B challenging the opponent.

Question:
{question}

Debate transcript:
{transcript}

Critically analyze the opponent’s reasoning and present a counterargument.
Remember, the final answer will either be 'REFUTED' or 'SUPPORTED'.

Rules:
- The answer must be either be "REFUTED" or "SUPPORTED".
- Do NOT include chain-of-thought reasoning in the answer.
- Do NOT include <think> blocks in the answer.
- Keep the argument under 10 sentences.
- Think blocks can only be added in the argument section.

Respond with:

Counterargument:
"

XXX  FIX JUDGE   XXX
XXX  FIX JUDGE   XXX
XXX  FIX JUDGE   XXX
Initial Judge:
"
You are an impartial judge evaluating a debate.

Return your evaluation ONLY in JSON format:

{
  "verdict": "final answer",
  "confidence": 1-5,
  "reasoning": "short and concise explanation of why this answer is correct"
}

Rules:
- Verdict must be the final answer to the question. The final answer will either be 'REFUTED' or 'SUPPORTED'.
- Confidence must be between 1 and 5.
- Reasoning must be under 8 sentences.

Question:
{question}

Debate Transcript:
{transcript}
"

# Appendix: Full Prompts
