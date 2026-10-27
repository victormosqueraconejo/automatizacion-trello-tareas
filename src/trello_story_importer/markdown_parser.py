import re
from pathlib import Path

from .errors import MarkdownParseError
from .models import Story

MODULE_RE = re.compile(r"^##(?!#)\s+(.+?)\s*$")
STORY_RE = re.compile(r"^###\s+(HU-\d+)\s*(?:[-–—:]\s*)?(.+?)\s*$", re.IGNORECASE)
FIELD_RE = re.compile(r"^\*\*(?P<name>[^*]+?):\*\*\s*(?P<value>.*)$")


def parse_markdown(text: str, source: Path | None = None) -> list[Story]:
    lines = text.splitlines()
    stories: list[Story] = []
    current_module: str | None = None
    current_match: re.Match[str] | None = None
    current_start = 0

    def finish(end: int) -> None:
        nonlocal current_match
        if current_match is None:
            return
        identifier = current_match.group(1).upper()
        title = current_match.group(2).strip()
        body_lines = lines[current_start + 1:end]
        body = "\n".join(body_lines).strip()
        fields = {
            match.group("name").strip(): match.group("value").strip()
            for line in body_lines
            if (match := FIELD_RE.match(line.strip()))
        }
        stories.append(Story(identifier, title, current_module, body, fields, source))

    for index, line in enumerate(lines):
        module_match = MODULE_RE.match(line)
        story_match = STORY_RE.match(line)
        if module_match:
            finish(index)
            current_match = None
            current_module = module_match.group(1).strip()
        elif story_match:
            finish(index)
            current_match = story_match
            current_start = index
    finish(len(lines))

    validate_stories(stories)
    return stories


def parse_file(path: Path) -> list[Story]:
    if not path.is_file() or path.suffix.lower() != ".md":
        raise MarkdownParseError(f"El archivo no es un Markdown válido: {path}")
    try:
        return parse_markdown(path.read_text(encoding="utf-8"), path)
    except UnicodeDecodeError as error:
        raise MarkdownParseError(f"No se pudo leer {path} como UTF-8: {error}") from error


def validate_stories(stories: list[Story]) -> None:
    seen: set[str] = set()
    for story in stories:
        if not story.identifier or not story.title:
            raise MarkdownParseError("Cada historia debe tener identificador y título")
        if story.identifier in seen:
            location = f" en {story.source}" if story.source else ""
            raise MarkdownParseError(f"Identificador duplicado {story.identifier}{location}")
        seen.add(story.identifier)
