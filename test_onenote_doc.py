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

        def fake_download(_session, url, dest_dir, stem, prefer_ext=""):
            fetched.append(url)
            ext = prefer_ext or (".pdf" if "r2" in url else ".png")
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
    assert "assets/000-1NF-0.png" in md, md
    assert "graph.microsoft.com" not in md, "a Graph URL leaked into the document"
    # <object> survives as a link (markdownify would otherwise drop it entirely)
    assert "Attachment: spec.pdf" in md, md
    # real export saved PDFs as ".bin": Graph serves octet-stream, the filename knows better
    assert "assets/000-1NF-att-0-spec.pdf" in md, md
    assert ".bin" not in md, md
    # markdown conversion actually happened
    assert "**1NF**" in md and "* atomic values" in md, md
    # the page's own <h1>1NF</h1> duplicated the title heading and must be gone
    assert "\n# 1NF" not in md and md.count("1NF\n") == 1, md
    # ocr output appended
    assert "TRANSCRIBED DIAGRAM TEXT" in md and "Text extracted from images" in md


ONENOTE_HTML = """<html lang="en-US"><head><title>Normalization</title></head>
<body data-absolute-enabled="true" style="font-family:Calibri;font-size:11pt">
<div style="position:absolute;left:48px;top:115px;width:624px">
<h1 style="margin-top:0pt">Normalization</h1>
<p>A relation is in <span style="font-weight:bold">1NF</span> when every attribute is
<span style="font-style:italic">atomic</span>.</p>
<ul><li>no repeating groups<ul><li>nested rule</li></ul></li></ul>
<table data-id="tbl1">
<tr><td><p>Form</p></td><td><p>Requirement</p></td></tr>
<tr><td><p>2NF</p></td><td><p>No partial dependency</p></td></tr>
</table></div></body></html>"""


def test_real_onenote_markup():
    """Graph returns absolute-positioned divs with emphasis as inline CSS, not <b>/<i>."""
    with tempfile.TemporaryDirectory() as tmp:
        assets = Path(tmp) / "assets"
        assets.mkdir()
        session = mock.Mock()
        session.get.return_value = mock.Mock(text=ONENOTE_HTML, raise_for_status=lambda: None)
        md = od.page_to_markdown(session, {"id": "p", "title": "Normalization"}, assets,
                                 do_ocr=False)

    # style-based emphasis must survive; markdownify alone drops it
    assert "**1NF**" in md, md
    assert "*atomic*" in md, md
    # first row promoted to header — no invented blank header row
    assert "| Form | Requirement |" in md, md
    assert "|  |  |" not in md, md
    # nested list structure kept
    assert "nested rule" in md, md
    # absolute-positioned wrapper divs must not leak through as markup
    assert "position:absolute" not in md, md


def _resp(status, headers=None):
    return mock.Mock(status_code=status, headers=headers or {})


def test_graph_session_retries_throttling():
    """Graph throttles the OneNote API hard; a 429 must not kill a long export."""
    replies = [_resp(429, {"Retry-After": "3"}), _resp(429, {"Retry-After": "1"}), _resp(200)]
    slept = []
    with mock.patch.object(od.requests.Session, "request", side_effect=replies) as req, \
         mock.patch.object(od.time, "sleep", slept.append):
        s = od.GraphSession(token_fn=lambda: "tok")
        assert s.get("https://graph/x").status_code == 200
    assert slept == [3, 1], slept          # honours Retry-After rather than a fixed backoff
    assert req.call_count == 3


def test_graph_session_caps_retries():
    """A permanently throttled endpoint gives up instead of looping forever."""
    with mock.patch.object(od.requests.Session, "request", return_value=_resp(429)) as req, \
         mock.patch.object(od.time, "sleep", lambda _s: None):
        s = od.GraphSession(token_fn=lambda: "tok")
        assert s.get("https://graph/x").status_code == 429
    assert req.call_count == od.GraphSession.MAX_ATTEMPTS


def test_graph_session_refreshes_expired_token():
    """Tokens last ~1h; a big section with OCR outlives one, so 401 must refresh in place."""
    tokens = iter(["old", "new"])
    with mock.patch.object(od.requests.Session, "request",
                           side_effect=[_resp(401), _resp(200)]), \
         mock.patch.object(od.time, "sleep", lambda _s: None):
        s = od.GraphSession(token_fn=lambda: next(tokens))
        assert s.headers["Authorization"] == "Bearer old"
        assert s.get("https://graph/x").status_code == 200
        assert s.headers["Authorization"] == "Bearer new"


def test_graph_session_skips_pointless_retry():
    """If the refresh hands back the same token, retrying it cannot help — surface the 401."""
    with mock.patch.object(od.requests.Session, "request", return_value=_resp(401)) as req, \
         mock.patch.object(od.time, "sleep", lambda _s: None):
        s = od.GraphSession(token_fn=lambda: "tok")
        assert s.get("https://graph/x").status_code == 401
    assert req.call_count == 1


def test_graph_session_gives_up_after_one_real_refresh():
    """A genuinely revoked grant retries once with the new token, then surfaces."""
    tokens = iter(["old", "new", "newer"])
    with mock.patch.object(od.requests.Session, "request", return_value=_resp(401)) as req, \
         mock.patch.object(od.time, "sleep", lambda _s: None):
        s = od.GraphSession(token_fn=lambda: next(tokens))
        assert s.get("https://graph/x").status_code == 401
    assert req.call_count == 2  # original + exactly one refresh attempt


def test_pasted_token_short_circuits_msal():
    """A Graph Explorer token must bypass MSAL entirely so the pipeline can be proven
    without an Azure app registration."""
    with mock.patch.dict(od.os.environ, {"ONENOTE_ACCESS_TOKEN": "  paste-me  "}, clear=False):
        assert od.get_token() == "paste-me"


def test_bearer_token_never_sent_off_graph():
    """A page can hotlink any host. The Graph token must never ride along to one."""
    with tempfile.TemporaryDirectory() as tmp:
        dest = Path(tmp)
        ok = mock.Mock(headers={"Content-Type": "image/png"}, content=b"x",
                       raise_for_status=lambda: None)
        session = mock.Mock()
        session.get.return_value = ok

        with mock.patch.object(od.requests, "get", return_value=ok) as bare:
            od.download_resource(session, "https://evil.example/steal.png", dest, "a")
        # off-Graph URL goes through plain requests.get, which carries no Authorization
        assert bare.call_count == 1, "off-Graph fetch must not use the authorised session"
        assert session.get.call_count == 0, "Graph token was sent to a third-party host"

        with mock.patch.object(od.requests, "get", return_value=ok) as bare:
            od.download_resource(
                session, "https://graph.microsoft.com/v1.0/me/onenote/resources/r/$value",
                dest, "b")
        # genuine Graph resource still needs the token, so it uses the session
        assert session.get.call_count == 1, "Graph resource must use the authorised session"
        assert bare.call_count == 0


def test_resolve_rejects_delimiter_only_query():
    """'/' split to zero terms, which matched every section and then crashed on terms[-1]."""
    for query in ("/", " > ", "//"):
        try:
            od.resolve_section(SECTIONS, query)
        except SystemExit:
            pass
        else:
            raise AssertionError(f"{query!r} should have exited cleanly")


def test_same_titled_pages_get_distinct_assets():
    """Two pages sharing a title previously wrote the same asset filenames, clobbering each other."""
    written = []

    def fake_download(_session, _url, dest_dir, stem, prefer_ext=""):
        p = dest_dir / f"{stem}.png"
        written.append(p.name)
        p.write_bytes(b"x")
        return p

    html = '<html><body><img src="https://graph.microsoft.com/x/$value"/></body></html>'
    with tempfile.TemporaryDirectory() as tmp:
        assets = Path(tmp) / "assets"
        assets.mkdir()
        session = mock.Mock()
        session.get.return_value = mock.Mock(text=html, raise_for_status=lambda: None)
        with mock.patch.object(od, "download_resource", fake_download):
            for i in (1, 2):
                od.page_to_markdown(session, {"id": f"p{i}", "title": "Notes"}, assets,
                                    do_ocr=False, index=i)

    assert len(set(written)) == 2, f"asset filenames collided: {written}"


def test_sniff_ext_beats_octet_stream():
    """Graph labels page images application/octet-stream. Trusting that saved every PNG as
    .bin, and .bin resolves to application/octet-stream, which silently disabled OCR."""
    assert od.sniff_ext(b"\x89PNG\r\n\x1a\n\x00\x00") == ".png"
    assert od.sniff_ext(b"\xff\xd8\xff\xe0abcd") == ".jpg"
    assert od.sniff_ext(b"GIF89a__") == ".gif"
    assert od.sniff_ext(b"%PDF-1.7_") == ".pdf"
    assert od.sniff_ext(b"RIFF\x00\x00\x00\x00WEBP") == ".webp"
    assert od.sniff_ext(b"nonsense") == ""


def test_ocr_reads_content_not_filename():
    """A PNG named .bin must still be OCR'd; the old name-based check bailed out."""
    import base64 as _b64
    png = _b64.b64decode(
        "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8z8BQDwAEhQGAhKmMIQAAAABJRU5ErkJggg==")
    with tempfile.TemporaryDirectory() as tmp:
        p = Path(tmp) / "image-saved-as.bin"
        p.write_bytes(png)
        seen = {}

        def fake_post(_url, headers=None, json=None, timeout=None):
            seen["mime"] = json["contents"][0]["parts"][1]["inline_data"]["mime_type"]
            return mock.Mock(raise_for_status=lambda: None, json=lambda: {
                "candidates": [{"content": {"parts": [{"text": "HELLO"}]}}]})

        with mock.patch.dict(od.os.environ, {"GEMINI_API_KEY": "k"}, clear=False), \
             mock.patch.object(od.requests, "post", fake_post):
            assert od.ocr(p) == "HELLO"
        assert seen["mime"] == "image/png", seen


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
