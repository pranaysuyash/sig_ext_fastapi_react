import os
from dataclasses import dataclass
from dotenv import load_dotenv


@dataclass
class AppConfig:
    api_base_url: str


def load_config() -> AppConfig:
    # Load .env from repo root if present
    load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "..", ".env"))
    api_base_url = os.getenv("API_BASE_URL", "http://127.0.0.1:8000")
    return AppConfig(api_base_url=api_base_url)
