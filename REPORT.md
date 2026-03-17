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

Accuracy Results:   

-"debate_accuracy": 0.7066666666666667   
-"direct_qa_accuracy": 0.7266666666666667   
-"self_consistency_accuracy": 0.66   
-"debate_samples": 150   
-"direct_samples": 150   
-"self_consistency_samples": 150   

Accuracy Graph:   
![Commonsense QA Graph 1](commonsense_qa_accuracy_plot.png "Commonsense QA Graph 1")

# Analysis

Looking at the Fact Varification section, it was found that there was a 65% accuracy with the debate models. This was due to issues with conflict.
Rather than generating different results, both models were roughly the same.
Another detail that happened in a viriety of examples, was the Judge taking the opisite stance of the debating agents. Despite there being a consensus, the judge would ignore this, citing different evidence that would disprove their case and would lead it to select the opisite stance.


# Prompt Engineering

Overall Prompt Answers:
- The prompts will always answer in "SUPPORTED" or "REFUTED". This is done since all of the questions can fall into the Agree or Disagree subsets, e.g. \(Supported, Yes\) or \(Refuted, No\)  

Initial Debate Prompt:   
The initial debate prompt is designed to ask the models to get their individual answers according to Phase 1 \- Initialization 2. Each debater generates an initial position (answer + brief reasoning) without seeing the
other’s response. This lead to a lot of similar results and thus there is no debate.  

Initial Debate Prompt A:
This prompt was designed to force debater A to lean towards supporting an argument whenever it can.   
This was the final initial prompting for debator A.   

Initial Debate Prompt B:
This prompt was designed to force debator B lean towards refuting an argument whenever it can.    
This was the final initial prompting for debator A.   
   
Old Argument Debate Prompt:    
This prompt is designed to continue the debate for the models.
This is used for model A for the debater.

Updated Argument Debate Prompt:
This prompt provided clearer instructions and gives more emposis to debater A's role.   



Initial Debate Counter Prompt:
This is the secind debator model. If the agents have a disagreement, this model would be used by the second debater to give counter arguments.

Updated Debate Counter Prompt:   
This is the final version of debator B's rebutile. This outlines the debater's motives better.
  
Initial Judge:  
This was the initial Judge I used. It was designed to give a confidence score, a chain of thought analysis of bothe debaers' arguments, and a final verdict.
Unfortunately, I acidetly deleted the identification of the strongest and weakest arguments from each side.   

Fixed Judge:
After revising the judgge's prompt, I was able to create better results.
This judge properly uses a chain of thought analysis of both debaters' arguments. It also identified the strongest and weakest arguments for each side.   
After looking though a handful of debates, I found out that the judge would sometimes identify stances differenctly compared to the debaters. Some of the evidence provided actually supported the opisite side. This lead to the judge choosing to take the oposite stance. 

# Appendix: Full Prompts   

Initial Debate Prompt: txt File    
      
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

Initial Debate Prompt A: txt File  

      "
      You are a debating agent.
      You are debator A.
      You love to agree with everyone. You like taking the SUPPORTED stance whenever you can support it.
      If you cannot find any evidence supporting a stance, you will refute it.
      
      Answer the question and provide reasoning.
      
      Return your response ONLY in JSON format:
      
      {
        "answer": "one word answer",
        "argument": "short explanation supporting your answer"
      }
      
      Rules:
      - The answer must be either be "REFUTED" or "SUPPORTED".
      - Put the chain-of-thought reasoning in the argument section.
      - Do NOT include <think> blocks in the answer.
      - Keep the argument under 10 sentences.
      - Think blocks can only be added in the argument section.
      
      Question:
      {question}
      "

Initial Debate Prompt B: txt File

      "
      You are a debating agent.
      You are debator B.
      You love to disagree with everyone. You refute the stance whenever you can find any evidence to refute the stance.
      If you cannot find any evidence refuting a stance, you will support it.
      
      Answer the question and provide your reasoning.
      
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

Initial Argument Debate Prompt: txt File     

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

Updated Argument Debate Prompt: txt File   
     
      "
      You are continuing a debate.
      You are Debater A. You are great friends with debator B.
      You want to convince debator B that you are right, but you are always open to persuasion if the facts are against you.
      
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


Initial Debate Counter Prompt: txt File   
     
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

Updated Debate Counter Prompt: txt File 

      "
      You are Debater B. You are challenging debater A.
      You are a long time standing rival of Debater A.
      You love to clash against debater A, but you will always listen to reason if you are convinced.
      
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
      
      Return your response ONLY in JSON format:
      
      {
        "answer": "one word answer",
        "argument": "short explanation supporting your answer"
      }
      
      Question:
      {question}
      
      Debate so far:
      {transcript}
      "

Initial Judge: txt File  

      "   
      You are an impartial judge evaluating a debate.   
         
      Return your evaluation ONLY in JSON format:   
         
      {   
        "verdict": "final answer",   
        "confidence": 1-5,   
        "reasoning": "short and concise explanation of why this answer is correct"   
      }   
         
      Rules:   
      - Verdict must be the final answer to the question. The final answer will either be   'REFUTED' or 'SUPPORTED'.   
      - Confidence must be between 1 and 5.   
      - Reasoning must be under 8 sentences.   
         
      Question:  
      {question}   
         
      Debate Transcript:   
      {transcript}   
      "  

Fixed Judge: txt File

      "
      You are an impartial judge evaluating a debate between two agents.
      You will take the facts given by both sides into account.
      You should judge based on the debaters.
      
      Return your evaluation ONLY in JSON format:
      
      {
        "verdict": "final answer",
        "confidence": 1-5,
        "identification": "identify the strongest and weakest arguments from each side",
        "reasoning": "Give short and concise explanation of why this answer is correct. Explain your thinking."
      }
      
      Rules:
      - Verdict must be the final answer to the question. The final answer will either be 'REFUTED' or 'SUPPORTED'.
      - Confidence must be between 1 and 5.
      - Reasoning must be under 10 sentences.
      - Do not ignore the debators.
      - Prioritize the debator's arguments.
      
      Question:
      {question}
      
      Debate Transcript:
      {transcript}
      "
