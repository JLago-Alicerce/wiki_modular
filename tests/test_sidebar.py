from scripts.generar_sidebar import build_sidebar_lines


def test_build_sidebar_lines():
    data = {
        "secciones": [
            {"titulo": "Intro", "id": 1},
            {"titulo": "SQL", "slug": "sql", "subtemas": ["Server"]},
        ]
    }
    lines = build_sidebar_lines(data, tolerant=True)
    expected = [
        "* [Inicio](README.md)",
        "* [Intro](1_intro.md)",
        "* [SQL](sql.md)",
        "  * [Server](sql/server.md)",
        "",
    ]
    assert lines == expected
