import scripts.editor_markdown as editor


def test_load_and_save(tmp_path, monkeypatch):
    md = tmp_path / "file.md"
    md.write_text("hola", encoding="utf-8")

    monkeypatch.setattr(editor, "FILE", md, raising=False)
    monkeypatch.setattr(editor, "run", lambda cmd: None)

    client = editor.app.test_client()
    assert client.get("/load").data.decode() == "hola"

    resp = client.post("/save", data="nuevo")
    assert resp.status_code == 200
    assert md.read_text(encoding="utf-8") == "nuevo"
