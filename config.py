import os
from dataclasses import dataclass
from typing import Optional
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

@dataclass
class Config:
    bot_token: str
    webapp_url: str
    webhook_url: Optional[str] = None
    webapp_port: int = 8000
    data_file: str = "data/users.json"
    
    @classmethod
    def from_env(cls):
        return cls(
            bot_token=os.getenv("BOT_TOKEN", ""),
            webapp_url=os.getenv("WEBAPP_URL", "http://localhost:8080"),
            webhook_url=os.getenv("WEBHOOK_URL"),
            webapp_port=int(os.getenv("WEBAPP_PORT", "8000")),
        )

config = Config.from_env()