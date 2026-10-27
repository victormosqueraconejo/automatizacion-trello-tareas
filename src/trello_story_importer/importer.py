import re
from collections.abc import Iterable

from .models import ImportSummary, Story
from .trello_client import TrelloClient

ID_RE = re.compile(r"\bHU-\d+\b", re.IGNORECASE)


def import_stories(stories: Iterable[Story], client: TrelloClient | None, list_id: str, dry_run: bool = False) -> ImportSummary:
    stories = list(stories)
    summary = ImportSummary(detected=len(stories))
    existing_ids: set[str] = set()
    if not dry_run:
        if client is None:
            raise ValueError("Se necesita un cliente Trello fuera de dry-run")
        existing_ids = {match.group(0).upper() for card in client.list_cards(list_id) if (match := ID_RE.search(card.get("name", "")))}

    for story in stories:
        if story.identifier.upper() in existing_ids:
            summary.skipped += 1
            continue
        if dry_run:
            summary.created += 1
            continue
        try:
            client.create_card(list_id, story)
            summary.created += 1
        except Exception as error:  # noqa: BLE001 - se informa y continúa con la siguiente historia
            summary.errors.append(f"{story.identifier}: {error}")
    return summary
