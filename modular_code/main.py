import argparse
import json
from config.env_loader import load_environment
from config.config_loader import load_config

from agents.base_llm import LLMInterface
from agents.debater_agent import DebaterAgent
from agents.judge_agent import JudgeAgent

from debate.debate_orchestrator import DebateOrchestrator
from experiments.run_experiments import run_dataset
from ui.debate_ui import launch_ui

from evaluation.evaluator import Evaluator  # Updated: import Evaluator
from api.server import launch_server

def build_system():
    env = load_environment()
    config = load_config()

    debater_llm = LLMInterface(
        env["debater_base"],
        env["debater_key"],
        env["debater_model"],
        config["generation"]["temperature"],
        config["generation"]["max_tokens"]
    )

    judge_llm = LLMInterface(
        env["judge_base"],
        env["judge_key"],
        env["judge_model"],
        config["generation"]["temperature"],
        config["generation"]["max_tokens"]
    )

    # Load all prompts
    prompts = {
        "initial": open("prompts/debater_initial.txt", encoding="utf-8").read(),
        "argument": open("prompts/debater_argument.txt", encoding="utf-8").read(),
        "counter": open("prompts/debater_counter.txt", encoding="utf-8").read(),
        "judge": open("prompts/judge_prompt.txt", encoding="utf-8").read()
    }

    debaterA = DebaterAgent("A", debater_llm, prompts)
    debaterB = DebaterAgent("B", debater_llm, prompts)
    judge = JudgeAgent(judge_llm, prompts["judge"])

    orchestrator = DebateOrchestrator(debaterA, debaterB, judge, config)

    return orchestrator, debater_llm, config


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset", type=str)
    parser.add_argument("--ui", action="store_true")
    parser.add_argument("--from_logs", action="store_true", help="Evaluate from saved logs instead of rerunning LLM")
    args = parser.parse_args()

    orchestrator, llm, config = build_system()
    evaluator = Evaluator(llm, config)

    if args.ui:
        launch_server()
    elif args.from_logs:
        results = evaluator.evaluate_from_logs()
        print("Evaluation from saved logs:")
        print(json.dumps(results, indent=2))
    elif args.dataset:
        run_dataset(args.dataset, orchestrator, llm, config)
    else:
        print("Specify --dataset, --ui, or --from_logs")


if __name__ == "__main__":
    main()