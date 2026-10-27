from trello_story_importer.markdown_parser import parse_markdown


def test_parse_multiple_stories_and_fields():
    stories = parse_markdown("""# Historias

## Generales (Autenticación y Perfil)

### HU-24 – Iniciar sesión (usuarios)

Como usuario registrado, quiero iniciar sesión.

**Criterios de aceptación:** El sistema valida las credenciales.
**Nivel de dificultad:** Medio (3 Puntos)
**Campo futuro:** Se conserva.

### HU-25 - Ver perfil

Como usuario, quiero consultar mi perfil.

## Tutorías

### HU-26: Reservar tutoría

**Criterios de aceptación:** Se crea la reserva.
""")

    assert [story.identifier for story in stories] == ["HU-24", "HU-25", "HU-26"]
    assert stories[0].module == "Generales (Autenticación y Perfil)"
    assert stories[0].title == "Iniciar sesión (usuarios)"
    assert stories[0].fields["Campo futuro"] == "Se conserva."
    assert stories[2].module == "Tutorías"


def test_card_name_and_description_preserve_content():
    story = parse_markdown("## Módulo\n### HU-1 - Título\n\nTexto")[0]
    assert story.card_name == "HU-1 – Título"
    assert "Módulo: Módulo" in story.card_description
    assert "Texto" in story.card_description
