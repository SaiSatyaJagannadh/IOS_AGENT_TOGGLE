#!/usr/bin/env python3
"""Offline checks for the two bits of real logic: section matching and page HTML localisation.

    python3 test_onenote_doc.py
"""
import sys
import tempfile
from pathlib import Path
from unittest import mock

import onenote_doc as od

SECTIONS = [
    ("ADBMS / Unit 1 / Normalization", "id-norm"),
    ("ADBMS / Unit 2 / Indexing", "id-index"),
    ("Basics / Normalization", "id-basics-norm"),
    ("Jobs / Applications", "id-jobs"),
]


def test_resolve():
    assert od.resolve_section(SECTIONS, "ADBMS/Normalization")[1] == "id-norm"
    assert od.resolve_section(SECTIONS, "Indexing")[1] == "id-index"
    assert od.resolve_section(SECTIONS, "Jobs / Applications")[1] == "id-jobs"
    # exact full-path match wins over substring scanning
    assert od.resolve_section(SECTIONS, "basics / normalization")[1] == "id-basics-norm"
    # ambiguous -> exits rather than silently picking one
    try:
        od.resolve_section(SECTIONS, "Normalization")
    except SystemExit:
        pass
    else:
        raise AssertionError("ambiguous query should have exited")
    # no match -> exits
    try:
        od.resolve_section(SECTIONS, "Nonexistent")
    except SystemExit:
        pass
    else:
        raise AssertionError("unmatched query should have exited")


PAGE_HTML = """<html><head><title>1NF</title></head><body>
<h1>1NF</h1>
<p>A relation is in <b>1NF</b> when every attribute is atomic.</p>
<img src="https://graph.microsoft.com/v1.0/me/onenote/resources/r1/$value"
     data-fullres-src="https://graph.microsoft.com/v1.0/me/onenote/resources/r1full/$value" />
<object data-attachment="spec.pdf" type="application/pdf"
        data="https://graph.microsoft.com/v1.0/me/onenote/resources/r2/$value"></object>
<ul><li>atomic values</li><li>no repeating groups</li></ul>
</body></html>"""


def test_page_to_markdown():
    with tempfile.TemporaryDirectory() as tmp:
        assets = Path(tmp) / "assets"
        assets.mkdir()
        fetched = []

        def fake_download(_session, url, dest_dir, stem):
            fetched.append(url)
            ext = ".pdf" if "r2" in url else ".png"
            p = dest_dir / f"{stem}{ext}"
            p.write_bytes(b"stub")
            return p

        session = mock.Mock()
        session.get.return_value = mock.Mock(text=PAGE_HTML, raise_for_status=lambda: None)
        page = {"id": "p1", "title": "1NF", "lastModifiedDateTime": "2026-08-03T00:00:00Z"}

        with mock.patch.object(od, "download_resource", fake_download), \
             mock.patch.object(od, "ocr", lambda _p: "TRANSCRIBED DIAGRAM TEXT"):
            md = od.page_to_markdown(session, page, assets, do_ocr=True)

    assert md.startswith("## 1NF"), md[:80]
    assert "2026-08-03" in md
    # full-res image preferred over the thumbnail src
    assert any("r1full" in u for u in fetched), fetched
    # image rewritten to the local relative path, not the Graph URL
    assert "assets/1NF-0.png" in md, md
    assert "graph.microsoft.com" not in md, "a Graph URL leaked into the document"
    # <object> survives as a link (markdownify would otherwise drop it entirely)
    assert "Attachment: spec.pdf" in md, md
    assert "assets/1NF-att-0-spec.pdf" in md, md
    # markdown conversion actually happened
    assert "**1NF**" in md and "* atomic values" in md, md
    # the page's own <h1>1NF</h1> duplicated the title heading and must be gone
    assert "\n# 1NF" not in md and md.count("1NF\n") == 1, md
    # ocr output appended
    assert "TRANSCRIBED DIAGRAM TEXT" in md and "Text extracted from images" in md


def test_slug():
    assert od.slug("Unit 1: Normalization / BCNF") == "Unit-1-Normalization-BCNF"
    assert od.slug("") == "untitled"
    assert len(od.slug("x" * 200)) == 60


if __name__ == "__main__":
    for name, fn in sorted(globals().items()):
        if name.startswith("test_"):
            fn()
            print(f"ok  {name}")
    print("\nall passed", file=sys.stderr)
