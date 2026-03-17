# Methodology
For this project, several different files were created to generate a modular code that can be broken up and change to fit the needs of the assignment.
While building this assignment, there wre several issues that had to be addressed and fixed. This will be talked about in the Experiments section.

# Experiments

There are two major tests to complete this project. The first is a fact_verification dataset. The second is based on commonsense_qa dataset.

The initial tests of this project ran into certian issues. Debates were rare between the agents since they almost always had the same stance. In order to complete the assignment, this will be implimented as required, but I was working on another variation of the assignment that would force the second agent to take the opisite stance if there was a consence. This would force the agents to better debate their stances. Another idea involved using different models to help create friction.

## Fact Verification

Accuracy Results: \n
{
  "debate_accuracy": 0.65,
  "direct_qa_accuracy": 0.65,
  "self_consistency_accuracy": 0.62,
  "debate_samples": 100,
  "direct_samples": 100,
  "self_consistency_samples": 100
}
Accuracy Graph: \n
## Commonsense Q/A Results
xxx

# Analysis

Looking at the Fact Varification section, it was found that there was a 65% accuracy with the debate models. This was due to issues with conflict.
Rather than generating different results, both models were roughly the same.
Another detail that happened in a viriety of examples, was the Judge taking the opisite stance of the debating agents. Despite there being a consensus, the judge would ignore this, citing different evidence that would disprove their case and would lead it to select the opisite stance.


# Prompt Engineering

# Appendix: Full Prompts
