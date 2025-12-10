import os
import secrets
from typing import Optional
from urllib.parse import urlparse

from dotenv import load_dotenv

load_dotenv()


def must(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise RuntimeError(f"Missing required env var {name}")
    return value


class Config:
    ZITADEL_DOMAIN: str = urlparse(must("ZITADEL_DOMAIN")).scheme + "://" + urlparse(must("ZITADEL_DOMAIN")).netloc

    ZITADEL_CLIENT_ID: str = must("ZITADEL_CLIENT_ID")
    ZITADEL_CLIENT_SECRET: str = os.getenv("ZITADEL_CLIENT_SECRET", secrets.token_hex(16))
    ZITADEL_CALLBACK_URL: str = must("ZITADEL_CALLBACK_URL")
    ZITADEL_POST_LOGIN_URL: str = os.getenv("ZITADEL_POST_LOGIN_URL", "/profile")
    ZITADEL_POST_LOGOUT_URL: str = os.getenv("ZITADEL_POST_LOGOUT_URL", "/")
    SESSION_SECRET: str = must("SESSION_SECRET")
    SESSION_DURATION: int = int(os.getenv("SESSION_DURATION", "3600"))

    PORT: Optional[str] = os.getenv("PORT")
    NODE_ENV: Optional[str] = os.getenv("NODE_ENV")


config = Config()
