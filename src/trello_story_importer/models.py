from dataclasses import dataclass, field
from pathlib import Path


@dataclass(frozen=True)
class Story:
    identifier: str
    title: str
    module: str | None
    body: str
    fields: dict[str, str] = field(default_factory=dict)
    source: Path | None = None

    @property
    def card_name(self) -> str:
        return f"{self.identifier} – {self.title}"

    @property
    def card_description(self) -> str:
        module = self.module or "Sin módulo"
        return f"Módulo: {module}\n\n{self.body.strip()}".strip()


@dataclass
class ImportSummary:
    detected: int = 0
    created: int = 0
    skipped: int = 0
    errors: list[str] = field(default_factory=list)
