from trello_story_importer.importer import import_stories
from trello_story_importer.markdown_parser import parse_markdown


class FakeClient:
    def __init__(self):
        self.created = []

    def list_cards(self, list_id):
        return [{"name": "HU-24 – Existente"}]

    def create_card(self, list_id, story):
        self.created.append((list_id, story.card_name))


def test_import_skips_duplicates_and_creates_new_cards():
    stories = parse_markdown("### HU-24 - Existente\n\nTexto\n### HU-25 - Nueva\n\nTexto")
    client = FakeClient()
    summary = import_stories(stories, client, "list-1")
    assert (summary.detected, summary.created, summary.skipped, summary.errors) == (2, 1, 1, [])
    assert client.created == [("list-1", "HU-25 – Nueva")]


def test_dry_run_does_not_call_trello():
    stories = parse_markdown("### HU-25 - Nueva\n\nTexto")
    summary = import_stories(stories, None, "dry-run", dry_run=True)
    assert summary.created == 1
