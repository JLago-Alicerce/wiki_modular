"""Utility helpers for sidebar and wiki files."""
from __future__ import annotations

import re
from pathlib import Path
from typing import List

from wiki_modular.config import SIDEBAR_FILE, WIKI_DIR


def get_sidebar_links(sidebar: Path | None = None) -> List[str]:
    """Return Markdown links listed inside ``_sidebar.md``."""
    sidebar = sidebar or SIDEBAR_FILE
    if not sidebar.exists():
        return []
    pattern = re.compile(r"\(([^)]+\.md)\)")
    links: List[str] = []
    for line in sidebar.read_text(encoding="utf-8").splitlines():
        match = pattern.search(line)
        if match:
            links.append(match.group(1).lstrip("/"))
    return links


def list_markdown_files(wiki_dir: Path | None = None) -> List[str]:
    """Return all Markdown file paths relative to ``wiki/``."""
    wiki_dir = wiki_dir or WIKI_DIR
    files: List[str] = []
    for p in wiki_dir.rglob("*.md"):
        if p.name.lower() == "readme.md":
            continue
        files.append(str(p.relative_to(wiki_dir)).replace("\\", "/"))
    return files
