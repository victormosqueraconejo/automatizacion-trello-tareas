# Trello Story Importer

Importa historias de usuario desde Markdown como tarjetas de Trello usando la API REST oficial.

## Instalación

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[test]"
cp .env.example .env
```

Completa `.env` con la API key y el token obtenidos en la página de desarrolladores de Trello, además del `TRELLO_LIST_ID`. `TRELLO_BOARD_ID` se conserva para identificar el tablero configurado.

## Uso

```bash
python -m trello_story_importer archivo.md --dry-run
python -m trello_story_importer archivo.md
python -m trello_story_importer ./historias/
```

El modo normal consulta las tarjetas existentes de la lista y omite cualquier historia cuyo identificador `HU-XX` ya aparezca en el nombre de una tarjeta. Los fallos de una tarjeta se informan y no detienen las siguientes. El resumen muestra historias detectadas, creadas, omitidas y errores.

El parser reconoce módulos `##`, historias `### HU-XX – título` y campos como `**Criterios de aceptación:** valor`. Conserva el bloque completo de cada historia, incluidos campos no conocidos.

La primera versión usa una lista común para todas las historias y no actualiza tarjetas existentes.

## Pruebas

```bash
pytest
```
