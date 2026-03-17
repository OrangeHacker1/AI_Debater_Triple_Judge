# AI_Debater_Triple_Judge
Assignment 2 of LLM Class. This is a basic AI agent program that can invoke 3 agents. 2 agents are responsible for picking a stance and defending their claims, while the remaining 1 serves as a judge to decide what the answer is based on the discussion/debate with the debater agents.   
This is also compared with a direct qa and a self_consistency with 6 tests. This was used to run a base line to compare the efficiency of the debate model compare to other solutions.   
For this project, two datasets were used. The answers being either ("SUPPORTED" or "REFUTED") or ("Yes" or "No").   

**SETUP:**

There are 2 ways to run this program.   
  1. VSCode / Local
  2. Website  

**REQUIREMENTS:** In order to run this program, the following packages must be installed:   
  1. Matlib   
  2. PyYAML   
  3. fastapi  
  4. uvicorn  
  5. fastapi uvicorn   
  6. python-dotenv   

**Dependencies:**   
In order to repeat this, you need to download the code files and use the following command to initiate connection to the LLMs: "python main.py --dataset datasets/<NAME_OF_DATASET>.json"   
The following datasets are fact verification and commonsense qa. These datasets were gathered from [SciFact](https://github.com/allenai/scifact?tab=readme-ov-file) and [StrategyQA](https://huggingface.co/datasets/voidful/StrategyQA/resolve/main/strategyqa_train.json) 
NAME_OF_DATASET:
  1. fact_verification  
  2. commonsense_qa  

To run the  program locally, you need to downlad the modular code section and store it in the acctive directory.  
You then need to add all of the other files. The exception includes the datasets. Two datasets were included. These are the datasets I used.    

 
Checking Results:     
The following are commands to run phase 4 (Accuracy).    
It is possible to check both the "logs\debate_runs" and "logs\debate_runs\<subfolder>".      
The subfolder can be used within the debate_runs folder to isolate datasets.   
\# Usage: python log_checker.py   
\# Usage Subfolder: python log_checker.py --subfolder run_1   
\# Searches: logs/debate_runs/run_1/    

In order to run the UI website, you need to run the following comand:   

    python main.py --UI   

After running the UI, you need to connect to your local server using the following:   

    http://localhost:8000

