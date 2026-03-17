import yaml
import os
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

from main import build_system
from evaluation.evaluator import Evaluator

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

orchestrator = None
llm = None
config = None


class QuestionRequest(BaseModel):
    question: str


class ConfigRequest(BaseModel):
    temperature: float
    max_tokens: int
    rounds: int
    early_stop_rounds: int
    samples: int


class EnvRequest(BaseModel):
    debater_base: str
    debater_model: str
    debater_key: str
    judge_base: str
    judge_model: str
    judge_key: str


@app.post("/set_config")
def set_config(cfg: ConfigRequest):

    config_data = {
        "generation": {
            "temperature": cfg.temperature,
            "max_tokens": cfg.max_tokens
        },
        "debate": {
            "rounds": cfg.rounds,
            "early_stop_rounds": cfg.early_stop_rounds
        },
        "logging": {
            "path": "logs/debate_runs/"
        },
        "self_consistency": {
            "samples": cfg.samples
        }
    }

    with open("config/config.yaml", "w") as f:
        yaml.dump(config_data, f)

    return {"status": "config saved"}


@app.post("/set_env")
def set_env(env: EnvRequest):

    env_text = f"""
DEBATER_BASE_URL={env.debater_base}
DEBATER_MODEL={env.debater_model}
API_DEBATER={env.debater_key}

JUDGE_BASE_URL={env.judge_base}
JUDGE_MODEL={env.judge_model}
API_JUDGE={env.judge_key}
"""

    with open(".env", "w") as f:
        f.write(env_text)

    return {"status": "env saved"}


@app.post("/run_debate")
def run_debate(req: QuestionRequest):

    global orchestrator, llm, config

    if orchestrator is None:
        orchestrator, llm, config = build_system()

    evaluator = Evaluator(llm, config)

    debate_result = orchestrator.run_debate(req.question)

    direct = evaluator.direct_qa(req.question)
    sc_answer, _ = evaluator.self_consistency(req.question)

    return {
        "debate": debate_result,
        "direct_qa": direct,
        "self_consistency": sc_answer
    }


def launch_server():
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

#python main.py --ui