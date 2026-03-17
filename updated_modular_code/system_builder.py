
from config.env_loader import load_environment
from config.config_loader import load_config

from agents.base_llm import LLMInterface
from agents.debater_agent import DebaterAgent
from agents.judge_agent import JudgeAgent

from debate.debate_orchestrator import DebateOrchestrator


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

    prompts = {
        "initial_A": open("prompts/debater_initial_A.txt", encoding="utf-8").read(),
        "initial_B": open("prompts/debater_initial_B.txt", encoding="utf-8").read(),
        "argument": open("prompts/debater_argument.txt", encoding="utf-8").read(),
        "counter": open("prompts/debater_counter.txt", encoding="utf-8").read(),
        "judge": open("prompts/judge_prompt.txt", encoding="utf-8").read()
    }

    debaterA = DebaterAgent("A", debater_llm, prompts)
    debaterB = DebaterAgent("B", debater_llm, prompts)
    judge = JudgeAgent(judge_llm, prompts["judge"])

    orchestrator = DebateOrchestrator(debaterA, debaterB, judge, config)

    return orchestrator, debater_llm, config