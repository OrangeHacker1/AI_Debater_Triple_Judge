import os
from dotenv import load_dotenv

def load_environment():
    """
    Loads all environment variables required for the system.
    """

    load_dotenv()

    env = {
        "debater_base": os.getenv("DEBATER_BASE_URL"),
        "debater_model": os.getenv("DEBATER_MODEL"),
        "debater_key": os.getenv("API_DEBATER"),

        "judge_base": os.getenv("JUDGE_BASE_URL"),
        "judge_model": os.getenv("JUDGE_MODEL"),
        "judge_key": os.getenv("API_JUDGE")
    }

    for key, value in env.items():
        if value is None:
            raise ValueError(f"Missing environment variable: {key}")

    return env
