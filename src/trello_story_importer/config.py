from dataclasses import dataclass
import os

from dotenv import load_dotenv

from .errors import ConfigurationError


@dataclass(frozen=True)
class Settings:
    api_key: str
    token: str
    board_id: str
    list_id: str
    timeout: float = 20.0


def load_settings() -> Settings:
    load_dotenv()
    values = {name: os.getenv(name, "").strip() for name in (
        "TRELLO_API_KEY", "TRELLO_TOKEN", "TRELLO_BOARD_ID", "TRELLO_LIST_ID"
    )}
    missing = [name for name, value in values.items() if not value]
    if missing:
        raise ConfigurationError(
            "Faltan variables de entorno: " + ", ".join(missing)
        )
    return Settings(values["TRELLO_API_KEY"], values["TRELLO_TOKEN"], values["TRELLO_BOARD_ID"], values["TRELLO_LIST_ID"])
