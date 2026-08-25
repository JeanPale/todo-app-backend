import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()

@dataclass(frozen=True)
class Settings:
    database_url: str
    cors_allowed_origins: list[str]

settings = Settings(
        database_url=os.environ["DATABASE_URL"],
        cors_allowed_origins=os.environ["CORS_ALLOWED_ORIGINS"].split(','),
)
