import argparse
import logging
from pathlib import Path

from .config import load_settings
from .errors import ImporterError
from .importer import import_stories
from .markdown_parser import parse_file
from .trello_client import TrelloClient


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Importa historias Markdown como tarjetas de Trello.")
    parser.add_argument("input", type=Path, help="Archivo .md o directorio con archivos Markdown")
    parser.add_argument("--dry-run", action="store_true", help="Analiza sin conectarse ni crear tarjetas")
    parser.add_argument("--verbose", action="store_true", help="Activa mensajes detallados")
    return parser


def collect_stories(input_path: Path):
    paths = [input_path] if input_path.is_file() else sorted(input_path.rglob("*.md"))
    if not paths:
        raise ImporterError(f"No se encontraron archivos Markdown en {input_path}")
    stories = []
    for path in paths:
        stories.extend(parse_file(path))
    return stories


def main() -> int:
    args = build_parser().parse_args()
    logging.basicConfig(level=logging.INFO if args.verbose else logging.WARNING, format="%(levelname)s: %(message)s")
    try:
        stories = collect_stories(args.input)
        if args.dry_run:
            settings = None
            client = None
            list_id = "dry-run"
        else:
            settings = load_settings()
            client = TrelloClient(settings.api_key, settings.token, settings.timeout)
            list_id = settings.list_id
        summary = import_stories(stories, client, list_id, args.dry_run)
    except (OSError, ImporterError) as error:
        print(f"Error: {error}")
        return 2

    print(f"Historias detectadas: {summary.detected}")
    print(f"Tarjetas creadas: {summary.created}")
    print(f"Historias omitidas: {summary.skipped}")
    print(f"Errores: {len(summary.errors)}")
    for error in summary.errors:
        print(f"  - {error}")
    return 1 if summary.errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
