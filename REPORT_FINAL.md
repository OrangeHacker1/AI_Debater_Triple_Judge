This is the final report of this project.   
This summarizes and explains the final code and results found while experimenting with this project.   

## Methodology
This project's primary function is gain a better understanding of prompting to LLMs and designing a way for them to interact with each other.  
This project is broken up into 3 parts.
The project uses these parts to run experiments with different prompts and parameters. The parameters used can be modified in the ymal file for different tests.   
The first part of this project involves the command line user interface component. This part is for running tests and making quick changes without having to change any of the files, with the exception of the '.env' and 'config.ymal' files. This section includes the following callable functions:
1. main.py (Runs bulk experiments using datasets saved within the working directory.)
2. log_checker.py (Quickly checks the accuracy results for main.py results.)
3. log_checker1.py (Quickly checks the accuracy results for main.py results, creates an accuracy plot, and returns all incorect predictions for debates.)
4. log_checker.py (Quickly checks the accuracy results for main.py results, creates an accuracy plot, returns all incorect predictions for debates, and all debate files that did not have a concensus.)
The second part of this project does the bulk testing and runing prompts to the designated LLMs. This part is responsible for running the three types of answering methods: (Debate; Direct Question and Answer (Direct QA); Self Consistency). All of these methods work to answer a question with either a SUPPORTED (support, yes, true) or REFUTED (refuted, no, false). This is the main bulk of this project and the focus. It was built in a way to construct a working debate that could even have multiple LLMs joining in without breaking.
The third and final section is for validation. This section is for comparing ground truth values for all three methods mentioned above. The log_checker methods in part one also fall into this category. This was designed to have a way of closely examining the results to come to conclusions and further make predictions and improvements.

## Experiments
This project had 5 major itterations as it was fine tuned.

## Analysis


## Conclusions:
Based on the results found in this experiment, I found that the debate method was not working correctly. This conclusion comes from the fact that the direct answers were generating higher levels of accuracy than the improved method designed to increase accuracy. One of the prominent reasons for this result was the fact that the agents {}      

Unlike in the paper 'Irving, G., Christiano, P., & Amodei, D. (2018). AI Safety via Debate. arXiv:1805.00899.', the agents were somewhat forced to take a side due to never debating and not fulfiling the objective of the project. This could have been what caused the error rate to exceed the base line methods. 

Another interesting theory to test would be changing the promting methods to change the use of 'REFUTED' and 'SUPPORTED' to true and false. This could add a layer of finality (Binary) that the LLMs would better understand.    





## Prompting Methods

For this project, there were five itterations used to fine tune and create better prompts. Despite doing 5 rounds of experimentation, the results didn't come out as expected. This lead to questions on how this could be rectified. Despite not adding much to the Direct QA model, it was able to consistently answer questions and maintain a high level of accuracy. This model was zero shot. Only the output format was defined along with chain of thought prompting.   
The self Consistency prompts had been improved for the final itteration. There were issues with it giving reasonings for its answer instead of a one word answer, even when told not to or told to use only one word. Similarly, zero shot prompting was used.    
The debate prompt is the one with the most trouble. Even the final itteration did not produce good results, compared to the baselines. The method was expected to exceed the baseline of both, yet managed to fail. Both the debate agents and the judge methods required, and still need, fine tuning to get better results. A more in depth explination was given above.   
The prompts used are in the appendex section for review.   

## Appendix: Full Prompts   

Initial Debate Prompt Itteration 1: txt File    
      
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

Initial Debate Prompt A Itteration 2-3: txt File  

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

Initial Debate Prompt A Itteration 4: txt File  
            
            You are a debating agent.
            You are tasked with defending the stance issued by the "question".
            
            Provide reasoning for why this stance is True.
            
            Return your response ONLY in JSON format:
            
            {
              "answer": "SUPPORTED",
              "argument": "short explanation supporting your answer"
            }
            
            Rules:
            - The answer must be "SUPPORTED".
            - "answer" must be "SUPPORTED"
            - Put the chain-of-thought reasoning in the argument section.
            - Do NOT include <think> blocks in the answer.
            - Keep the argument under 10 sentences.
            - Think blocks can only be added in the argument section.
            
            Question:
            {question}

Initial Debate Prompt A Itteration 5: txt File  

            You are a debating agent.
            You are tasked with defending the stance issued by the "question".
            
            You MUST argue that the statement is TRUE regardless of uncertainty.
            You are NOT allowed to agree with the opposing agent.
            
            Return your response ONLY in JSON format:
            
            {
              "answer": SUPPORTED,
              "argument": < A concise explanation supporting your answer. >
            }
            
            Rules:
            - The "answer" must be SUPPORTED.
            - "answer" must be SUPPORTED
            - Keep the "argument" under 8 sentences.
            - Think blocks do not count towards the sentence limit for "argument".
            
            Question:
            {question}

Initial Debate Itteration 2-3 Prompt B: txt File

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

Initial Debate Itteration 4 Prompt B: txt File   

            You are a debating agent.
            You are tsked with disproving the stance in the "Question" section.
            
            You MUST argue that the statement is TRUE regardless of uncertainty.
            You are NOT allowed to agree with the opposing agent.
            The opposing agent has chosen SUPPORTED. Therefore, you must prove the stance false.
            
            Return your response ONLY in JSON format:
            
            {
              "answer": "REFUTED",
              "argument": "short explanation supporting your answer"
            }
            
            Rules:
            - The answer must be "REFUTED".
            - "answer" must be "REFUTED"
            - Do NOT include chain-of-thought reasoning in the answer.
            - Do NOT include <think> blocks in the answer.
            - Keep the argument under 10 sentences.
            - Think blocks can only be added in the argument section.
            
            Question:
            {question}

Initial Debate Itteration 4 Prompt B: txt File   

            You are a master debating agent.
            You are tasked with disproving the stance in the "Question" section.
            
            You MUST argue that the statement is FALSE regardless of uncertainty.
            You are NOT allowed to agree with the opposing agent.
            The opposing agent has chosen SUPPORTED. Therefore, you must prove the stance false.
            
            Return your response ONLY in JSON format:
            
            {
              "answer": REFUTED,
              "argument": <concise explanation proving the question wrong>
            }
            
            Rules:
            - The "answer" must be REFUTED.
            - "answer" must be REFUTED
            - Keep the argument under 4 sentences.
            - Think blocks will not add to the sentence count.
            
            Question:
            {question}

Direct QA Itteration 1-5 Prompt: txt  File (RESPONSE IS STR.)

      "
      Answer the following question in ONE word for the final answer.
      Provide reasoning separately under 'Reasoning:'.
      
      Question:
      {question}
      
      Format:
      Answer: <one word answer> "SUPPORTED" or "REFUTED"
      Reasoning: <explanation in 1-3 sentences>
      "

Self Consistency Itteration 1-4 Prompt: txt File   

      "
      Answer the question using step-by-step reasoning.
      The final answer will either be 'REFUTED' or 'SUPPORTED'.
      
      Question:
      {question}
      
      Format:
      Answer:
      Reasoning:
      "

Self Consistency Itteration 5 Prompt: txt File   

            You must answer only in valid JSON. No extra text.
            
            Question:
            {question}
            
            Provide reasoning separately in 'reasoning:'.
            
            Return JSON only:
            
            {
                  "answer": "REFUTED or SUPPORTED",
                  "reasoning": " Concise explination of your reasoning for "answer""
            }
            
            Rules:
            - Output MUST be valid JSON (parsable with json.loads)
            - "answer" must be either REFUTED or SUPPORTED.
            - "answer" must be one word.
            - Do not include any text before json.
            - Do NOT include <think> or hidden reasoning
            - "reasoning" cannot be more than 8 sentences.
            
            Return only json.


Argument Debate Itteration 1 Prompt: txt File     

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

Argument Debate Itteration 2-3 Prompt: txt File   

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

Argument Debate Itteration 4 Prompt: txt File   

            You are continuing a debate.
            
            Question:
            {question}
            
            Here is the debate so far:
            {transcript}
            
            You must:
            - Analyze the opponent’s argument
            - Strengthen your position
            - Do NOT repeat previous reasoning
            
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


Argument Debate Itteration 5 Prompt: txt File   

            You are debater A.
            You are continuing a debate.
            
            Question:
            {question}
            
            Your job:
            - Analyze Debater B's argument
            - Identify flaws in Debater B's argument
            - Provide counter-evidence
            - Strengthen your position
            - Maintain your stance as SUPPORTED
            
            Here is the debate so far:
            {transcript}
            
            Return JSON only:
            
            {
              "answer": "your final answer",
              "argument": "your rebuttal to the other debater"
            }
            
            Rules:
            - The answer must be either be "REFUTED" or "SUPPORTED".
            - Keep the argument within 4 sentences.
            - Think blocks can only be added in the "argument" section.


Debate Counter Itteration 1 Prompt: txt File   
     
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

Debate Counter Itteration 2-3 Prompt: txt File 

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
Debate Counter Itteration 4 Prompt: txt File

            You are Debater B.
            
            The Question:
            {question}
            
            Your job:
            - Identify flaws in Debater A's argument
            - Provide counter-evidence
            - Maintain your stance as REFUTED
            
            Debate so far:
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

      

Debate Counter Itteration 5 Prompt: txt File  

            You are Debater B.

            The Question:
            {question}
            
            Your job:
            - Analyze Debater A's argument
            - Identify flaws in Debater A's argument
            - Strengthen your position
            - Provide counter-evidence
            - Maintain your stance as REFUTED
            
            Debate so far:
            {transcript}
            
            Critically analyze the opponent’s reasoning and present a counterargument.
            Remember, the final answer will either be 'REFUTED' or 'SUPPORTED'.
            
            Rules:
            - The answer must be either be "REFUTED" or "SUPPORTED".
            - Keep the argument under 4 sentences.
            - Think blocks will not be counted towards the argument limit.
            
            Return your response ONLY in JSON format:
            
            {
              "answer": "one word answer",
              "argument": "short explanation supporting your answer"
            }

Judge Itteration 1: txt File  

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

Judge Itteration 2-3: txt File

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

Judge Itteration 4 Prompt: txt File

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


Judge Itteration 5 Prompt: txt File

            You are an impartial judge evaluating a debate between two agents.
            You will take the facts given by both sides into account.
            You should judge based on the debaters.
            
            Return your evaluation ONLY in JSON format:
            
            {
              "verdict": "final answer",
              "confidence": 1-5,
              "analysis": "Sumarize the debate so far.",
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
