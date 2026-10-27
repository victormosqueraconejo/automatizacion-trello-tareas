import logging
import time
from typing import Any

import requests

from .errors import TrelloAPIError
from .models import Story

LOGGER = logging.getLogger(__name__)


class TrelloClient:
    base_url = "https://api.trello.com/1"

    def __init__(self, api_key: str, token: str, timeout: float = 20.0, session: requests.Session | None = None):
        self.session = session or requests.Session()
        self.auth = {"key": api_key, "token": token}
        self.timeout = timeout

    def _request(self, method: str, path: str, **kwargs: Any) -> Any:
        params = dict(kwargs.pop("params", {}))
        params.update(self.auth)
        for attempt in range(3):
            try:
                response = self.session.request(method, self.base_url + path, params=params, timeout=self.timeout, **kwargs)
            except requests.RequestException as error:
                if attempt == 2:
                    raise TrelloAPIError(f"Error de conexión con Trello: {error}") from error
                time.sleep(2**attempt)
                continue
            if response.status_code == 429 or response.status_code >= 500:
                if attempt == 2:
                    break
                retry_after = response.headers.get("Retry-After", "1")
                try:
                    delay = min(float(retry_after), 30.0)
                except ValueError:
                    delay = 1.0
                time.sleep(delay)
                continue
            if not response.ok:
                detail = response.text[:300]
                raise TrelloAPIError(f"Trello respondió HTTP {response.status_code}: {detail}")
            return response.json()
        raise TrelloAPIError(f"Trello no respondió después de varios intentos (HTTP {response.status_code})")

    def list_cards(self, list_id: str) -> list[dict[str, Any]]:
        return self._request("GET", f"/lists/{list_id}/cards", params={"fields": "name,id"})

    def create_card(self, list_id: str, story: Story) -> dict[str, Any]:
        return self._request("POST", "/cards", params={"idList": list_id, "name": story.card_name, "desc": story.card_description})
