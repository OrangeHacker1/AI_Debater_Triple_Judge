# PROJECT NAME: AI DEBATER TRIPLE JUDGE

## SUMMARY:

This project is designed to use LLMs to hold a debate to further increase accuracy and diswade digital halucinations.   
The goal is to design a program that can uphold a debate with multiple agents and have both a judge and a panel of Judges review the debate to determine the output.   
Baseline models were used to construct a basline accuracy for the LLM used in project.    
API keys will not be provided. The specs of the LLMs will be listed in the .env file and included in the dependency section in this file.
All questions used for this debate will be statements that are either (SUPPORTED, yes, true) or (REFUTED, no, false).   

## USAGE:
This project has two methods of interaction with users:
1. Hard Code  
2. User Interface (UI)   
    
Hard Code: This method involves invoking the main method to load specific datasets with ground truth values and questions. The format for datasets must be in json. This will store the json outputs for all three output files in the designated 'logging' section of the 'config.ymal' file. The path can be modified for different folder usage.   
Command:

    python main.py --dataset {datasets_folder}/{dataset}.json
NOTE: The '--dataset' command checks the working directory.   

User Interface (UI): This is a dynamic approach for asking individual questions. This can be used to prompt and test individual questions to the debate and base methods. There is no storage method to save or test accuracies. Nor is there a way to test ground truth values. This method will launch a website hosted on the local machine. You can connected to the website via: 'http://localhost:8000'.    
Command:   

    python main.py --ui
NOTE: This command will open a webpage. You need to connect via a webpage.

## Required Packages:

  1. Matlib   
  2. PyYAML   
  3. fastapi  
  4. uvicorn  
  5. fastapi uvicorn   
  6. python-dotenv

## Dependencies:

To use this project, you need at least 1 LLM that can be called. The LLMs used for this project to get the results in REPORT_FINAL.md are as follows:

            DEBATER_MODEL=Qwen/Qwen3-8B
            JUDGE_MODEL=meta-llama/Llama-3.1-8B-Instruct

## Datasets Used

There are two main datasets used.   
The following datasets are fact verification and commonsense qa. These datasets were gathered from [SciFact](https://github.com/allenai/scifact?tab=readme-ov-file) and [StrategyQA](https://huggingface.co/datasets/voidful/StrategyQA/resolve/main/strategyqa_train.json).     
NAME_OF_DATASET:    
  1.  fact_verification   
  2. commonsense_qa   


## Check Results:
There are three methods for running tests. Each method is designed to extract additional information for examination. The '--subfolder' pareameter is optional.    
1. log_checker.py: This python file is designed to scrape a folder to gather all of the results within the logging folder. It is also possible to scrape a subfolder. The commands are as follows.
Command Line Code:

        python log_checker.py --subfolder {subfolder}

3. log_checker1.py: Completes the tasks of log_ckecker.py and looks for mismatched ground truth values and predictions for debates. Debate panels were not included due to overlap. The final output is an accuracy graph. This is saved to the file used.     
Command Line Code:

        python log_checker1.py --subfolder {subfolder}

5. log_checker2.py: Completes the tasks of logchecker1.py and looks for debates. This is designed to find debates and filter out concensuses.
Command Line Code:

       python log_checker2.py --subfolder {subfolder}


