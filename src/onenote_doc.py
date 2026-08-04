#!/usr/bin/env python3
"""Read every page of a OneNote section via Microsoft Graph and write one Markdown + .docx doc.

Local OneNote data on macOS is an opaque revision-store cache and OneNote for Mac has no
AppleScript dictionary, so Graph is the only readable source.

  python3 src/onenote_doc.py --list                 # show every section path you can pull
  python3 src/onenote_doc.py "ADBMS/Normalization"  # pull that section -> out/
  python3 src/onenote_doc.py "ADBMS" --no-ocr -o ~/Desktop/notes
"""
import argparse
import base64
import mimetypes
import os
import re
import sys
import time
from pathlib import Path
from urllib.parse import urlparse

import msal
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from markdownify import markdownify

load_dotenv(Path(__file__).resolve().parent.parent / ".env")

GRAPH = "https://graph.microsoft.com/v1.0"
SCOPES = ["Notes.Read.All"]
TOKEN_CACHE = Path.home() / ".onenote_agent_token.json"
OCR_MODEL = "gemini-2.5-flash"
GRAPH_HOSTS = ("graph.microsoft.com",)


# ---------------------------------------------------------------- auth

def get_token():
    """Return a valid access token. Prompts for device login only the first time; afterwards
    MSAL refreshes silently, so this is safe to call repeatedly mid-export.

    ONENOTE_ACCESS_TOKEN short-circuits all of this: paste a token from Microsoft's Graph
    Explorer to try the exporter without registering an Azure app. It expires in about an
    hour and cannot be refreshed, so it is for proving the pipeline, not for regular use.
    """
    pasted = os.getenv("ONENOTE_ACCESS_TOKEN")
    if pasted:
        return pasted.strip()

    client_id = os.getenv("ONENOTE_CLIENT_ID")
    if not client_id:
        sys.exit(
            "ONENOTE_CLIENT_ID is not set.\n"
            "Register a free Azure app (portal.azure.com > App registrations > New):\n"
            "  - Supported account types: any org directory AND personal Microsoft accounts\n"
            "  - Authentication > Add a platform > Mobile and desktop > check the native client\n"
            "    redirect URI, and set 'Allow public client flows' to Yes\n"
            "  - API permissions > Microsoft Graph > Delegated > Notes.Read.All > Grant consent\n"
            "Then put the Application (client) ID in .env as ONENOTE_CLIENT_ID=..."
        )

    cache = msal.SerializableTokenCache()
    if TOKEN_CACHE.exists():
        cache.deserialize(TOKEN_CACHE.read_text())

    app = msal.PublicClientApplication(
        client_id, authority="https://login.microsoftonline.com/common", token_cache=cache
    )

    result = None
    accounts = app.get_accounts()
    if accounts:
        result = app.acquire_token_silent(SCOPES, account=accounts[0])

    if not result:
        flow = app.initiate_device_flow(scopes=SCOPES)
        if "user_code" not in flow:
            sys.exit(f"Could not start device login: {flow.get('error_description', flow)}")
        print(f"\n{flow['message']}\n", flush=True)
        result = app.acquire_token_by_device_flow(flow)

    if "access_token" not in result:
        sys.exit(f"Login failed: {result.get('error_description', result)}")

    if cache.has_state_changed:
        # Create restricted, not create-then-chmod: the refresh token inside is longer-lived
        # than any access token, and the gap would leave it world-readable on first write.
        fd = os.open(TOKEN_CACHE, os.O_CREAT | os.O_WRONLY | os.O_TRUNC, 0o600)
        with os.fdopen(fd, "w") as fh:
            fh.write(cache.serialize())

    return result["access_token"]


def _retry_after(value, fallback):
    """Retry-After is delay-seconds or an HTTP-date; never let the date form crash a run."""
    try:
        return int(value)
    except (TypeError, ValueError):
        return fallback


class GraphSession(requests.Session):
    """Session that survives the two things that reliably kill a long export.

    Graph throttles the OneNote API aggressively, and an access token lasts about an hour —
    a large section with OCR outlives it. Centralised here so every caller (page listing,
    page content, image and attachment downloads) is covered by one implementation.
    """

    MAX_ATTEMPTS = 5

    def __init__(self, token_fn=get_token):
        super().__init__()
        self._token_fn = token_fn
        self.headers["Authorization"] = f"Bearer {token_fn()}"

    def request(self, method, url, **kwargs):  # noqa: D102
        kwargs.setdefault("timeout", 120)
        refreshed = False
        attempt = 0
        while True:
            r = super().request(method, url, **kwargs)

            if r.status_code in (429, 503, 504) and attempt < self.MAX_ATTEMPTS - 1:
                wait = min(_retry_after(r.headers.get("Retry-After"), 2 ** attempt), 120)
                print(f"    throttled ({r.status_code}), retrying in {wait}s", file=sys.stderr)
                time.sleep(wait)
                attempt += 1
                continue

            # A refresh deliberately does NOT consume an attempt: a 401 arriving on the last
            # throttle retry would otherwise install a good token and never use it.
            if r.status_code == 401 and not refreshed:
                refreshed = True  # token expired mid-run; refresh once, then give up
                fresh = self._token_fn()
                if f"Bearer {fresh}" == self.headers["Authorization"]:
                    # a pasted Graph Explorer token has no refresh path — say so plainly
                    print("    401 and the token cannot be refreshed. If this is a pasted "
                          "ONENOTE_ACCESS_TOKEN it has expired (~1h); grab a fresh one.",
                          file=sys.stderr)
                    return r
                self.headers["Authorization"] = f"Bearer {fresh}"
                continue

            return r


# ---------------------------------------------------------------- graph

def graph_all(session, url):
    """GET a Graph collection, following @odata.nextLink."""
    items = []
    while url:
        r = session.get(url, timeout=60)
        r.raise_for_status()
        body = r.json()
        items.extend(body.get("value", []))
        url = body.get("@odata.nextLink")
    return items


def list_sections(session):
    """Every section as (path, id), path = 'Notebook / Group / Section'."""
    raw = graph_all(
        session, f"{GRAPH}/me/onenote/sections?$expand=parentNotebook,parentSectionGroup&$top=100"
    )
    out = []
    for s in raw:
        parts = [(s.get("parentNotebook") or {}).get("displayName")]
        parts.append((s.get("parentSectionGroup") or {}).get("displayName"))
        parts.append(s.get("displayName"))
        out.append((" / ".join(p for p in parts if p), s["id"]))
    return sorted(out)


def resolve_section(sections, query):
    """Match a user query like 'ADBMS/Normalization' against section paths."""
    terms = [t.strip().lower() for t in re.split(r"[/>]", query) if t.strip()]
    if not terms:
        sys.exit(f"No section matches {query!r}. Run --list to see available sections.")
    exact = [s for s in sections if s[0].lower() == query.strip().lower()]
    if exact:
        return exact[0]
    hits = [s for s in sections if all(t in s[0].lower() for t in terms)]
    if not hits:
        sys.exit(f"No section matches {query!r}. Run --list to see available sections.")
    if len(hits) > 1:
        # prefer a match on the last segment being the section name itself
        tail = [h for h in hits if h[0].split(" / ")[-1].lower() == terms[-1]]
        if len(tail) == 1:
            return tail[0]
        print("Ambiguous — matches:", file=sys.stderr)
        for path, _ in hits:
            print(f"  {path}", file=sys.stderr)
        sys.exit("Be more specific.")
    return hits[0]


def fetch_pages(session, section_id):
    url = f"{GRAPH}/me/onenote/sections/{section_id}/pages?$top=100&$orderby=order"
    try:
        return graph_all(session, url)
    except requests.HTTPError:  # some sections reject $orderby=order
        return graph_all(session, url.replace("&$orderby=order", "&$orderby=createdDateTime"))


# Graph labels page resources application/octet-stream, so Content-Type cannot name the
# format. Sniffing the bytes is the only reliable source; the extension drives both the
# docx embed and whether ocr() will even look at the file.
_MAGIC = (
    (b"\x89PNG\r\n\x1a\n", ".png"),
    (b"\xff\xd8\xff", ".jpg"),
    (b"GIF8", ".gif"),
    (b"BM", ".bmp"),
    (b"%PDF", ".pdf"),
)


def sniff_ext(data):
    """Real extension from magic bytes, or '' if unrecognised."""
    for sig, ext in _MAGIC:
        if data.startswith(sig):
            return ext
    if data[:4] == b"RIFF" and data[8:12] == b"WEBP":
        return ".webp"
    return ""


def download_resource(session, url, dest_dir, stem, prefer_ext=""):
    """Fetch one image/attachment. The Authorization header is only ever sent to Graph.

    A OneNote page can carry <img src>/<object data> pointing at any host — pasted web
    images and "insert online picture" links do exactly that. Because the session attaches
    a bearer token to every request, fetching such a URL through it would hand a live
    Notes.Read token to whoever controls that address. Off-Graph URLs go out unauthenticated.
    """
    host = (urlparse(url).hostname or "").lower()
    get = session.get if host in GRAPH_HOSTS else requests.get
    r = get(url, timeout=120)
    r.raise_for_status()
    # Graph serves attachments as application/octet-stream, so the Content-Type alone turns
    # every PDF and docx into a useless ".bin". The original filename knows better.
    ctype = mimetypes.guess_extension(r.headers.get("Content-Type", "").split(";")[0])
    ext = prefer_ext or sniff_ext(r.content[:16]) or ctype or ".bin"
    path = dest_dir / f"{stem}{ext}"
    path.write_bytes(r.content)
    return path


# ---------------------------------------------------------------- ocr

def ocr(path):
    """Transcribe text in an image using Gemini. Returns '' on any failure — OCR is best-effort."""
    key = os.getenv("GEMINI_API_KEY")
    if not key:
        return ""
    data = path.read_bytes()
    # Sniff the content, not the name: a mislabelled extension made this return early and
    # silently skipped OCR for every image in a real export.
    mime = mimetypes.types_map.get(sniff_ext(data[:16]) or path.suffix.lower(), "")
    if not mime.startswith("image/"):
        return ""
    try:
        r = requests.post(
            f"https://generativelanguage.googleapis.com/v1beta/models/{OCR_MODEL}:generateContent",
            headers={"x-goog-api-key": key},
            json={
                "contents": [{"parts": [
                    {"text": "Transcribe all text in this image, preserving structure. "
                             "Output only the transcription. If there is no text, output NOTEXT."},
                    {"inline_data": {"mime_type": mime,
                                     "data": base64.b64encode(data).decode()}},
                ]}]
            },
            timeout=120,
        )
        r.raise_for_status()
        text = r.json()["candidates"][0]["content"]["parts"][0]["text"].strip()
        return "" if text == "NOTEXT" or not text else text
    except Exception as e:  # noqa: BLE001 - never let OCR kill the export
        print(f"    ocr failed for {path.name}: {e}", file=sys.stderr)
        return ""


# ---------------------------------------------------------------- page -> markdown

def slug(text, limit=60):
    return re.sub(r"[^\w\-]+", "-", text).strip("-")[:limit] or "untitled"


def page_to_markdown(session, page, assets, do_ocr, index=0):
    """Fetch one page's HTML, localise its images/attachments, return markdown."""
    r = session.get(f"{GRAPH}/me/onenote/pages/{page['id']}/content?includeIDs=false", timeout=120)
    r.raise_for_status()
    soup = BeautifulSoup(r.text, "lxml")
    # Index-prefixed: two pages sharing a title (or both untitled) would otherwise
    # write the same asset filenames and clobber each other silently.
    stem = f"{index:03d}-{slug(page.get('title') or 'untitled')}"
    ocr_blocks = []

    for i, img in enumerate(soup.find_all("img")):
        src = img.get("data-fullres-src") or img.get("src")
        if not src:
            continue
        try:
            path = download_resource(session, src, assets, f"{stem}-{i}")
        except requests.RequestException as e:
            print(f"    image {i} failed: {e}", file=sys.stderr)
            continue
        img["src"] = f"{assets.name}/{path.name}"
        img.attrs.pop("data-fullres-src", None)
        if not img.get("alt"):
            img["alt"] = path.name
        if do_ocr:
            text = ocr(path)
            if text:
                ocr_blocks.append(f"**Text in `{path.name}`:**\n\n{text}")

    for i, obj in enumerate(soup.find_all("object")):
        src, name = obj.get("data"), obj.get("data-attachment") or f"attachment-{i}"
        if not src:
            continue
        try:
            path = download_resource(session, src, assets,
                                     f"{stem}-att-{i}-{slug(Path(name).stem)}",
                                     prefer_ext=Path(name).suffix)
        except requests.RequestException as e:
            print(f"    attachment {name} failed: {e}", file=sys.stderr)
            continue
        link = soup.new_tag("a", href=f"{assets.name}/{path.name}")
        link.string = f"Attachment: {name}"
        obj.replace_with(link)  # markdownify drops <object> entirely

    body = soup.body or soup

    # OneNote carries emphasis as inline CSS on <span>, not as <b>/<i>. markdownify only reads
    # tags, so without this every bold and italic run in the notebook is silently flattened.
    for span in body.find_all("span", style=True):
        style = span["style"].replace(" ", "").lower()
        if re.search(r"font-weight:(bold|[6-9]00)", style):
            span.wrap(soup.new_tag("strong"))
        if "font-style:italic" in style:
            span.wrap(soup.new_tag("em"))

    # OneNote tables have no <thead>, so markdownify emits an empty header row and demotes the
    # real first row to data. Promote it instead.
    for table in body.find_all("table"):
        if table.find("th") or table.find("thead"):
            continue
        first = table.find("tr")
        if first:
            for cell in first.find_all("td"):
                cell.name = "th"

    # Page title becomes the '##' below, so drop the page's own duplicate title heading and
    # demote what's left — keeps one clean hierarchy for the docx outline.
    title = (page.get("title") or "").strip().lower()
    for h in body.find_all(["h1", "h2", "h3", "h4", "h5", "h6"]):
        if h.get_text(strip=True).lower() == title:
            h.decompose()
    for level in range(5, 0, -1):
        for h in body.find_all(f"h{level}"):
            h.name = f"h{level + 1}"

    md = markdownify(str(body), heading_style="ATX", strip=["title"]).strip()
    md = re.sub(r"\n{3,}", "\n\n", md)

    header = f"## {page.get('title') or 'Untitled'}\n\n"
    meta = page.get("lastModifiedDateTime", "")
    if meta:
        header += f"*Last modified: {meta}*\n\n"
    if ocr_blocks:
        md += "\n\n### Text extracted from images\n\n" + "\n\n".join(ocr_blocks)
    return header + md


# ---------------------------------------------------------------- main

def main():
    ap = argparse.ArgumentParser(description="Export a OneNote section to Markdown + .docx")
    ap.add_argument("section", nargs="?", help="section path, e.g. 'ADBMS/Normalization'")
    ap.add_argument("--list", action="store_true", help="list every available section and exit")
    ap.add_argument("-o", "--out", default="out", help="output directory (default: out)")
    ap.add_argument("--no-ocr", action="store_true", help="skip OCR of images")
    ap.add_argument("--no-docx", action="store_true", help="skip .docx conversion")
    args = ap.parse_args()

    session = GraphSession()

    sections = list_sections(session)
    if args.list:
        for path, _ in sections:
            print(path)
        return
    if not args.section:
        ap.error("give a section path, or --list to see them")

    path, section_id = resolve_section(sections, args.section)
    print(f"Section: {path}")

    pages = fetch_pages(session, section_id)
    if not pages:
        sys.exit("That section has no pages.")
    print(f"Pages: {len(pages)}")
    if not args.no_ocr and os.getenv("GEMINI_API_KEY"):
        print("OCR on: page images will be sent to Google's Gemini API (--no-ocr to disable)")

    out_dir = Path(args.out).expanduser()
    assets = out_dir / "assets"
    assets.mkdir(parents=True, exist_ok=True)

    chunks = [f"# {path}\n\n*Source: OneNote via Microsoft Graph · {len(pages)} pages*\n"]
    for n, page in enumerate(pages, 1):
        print(f"  [{n}/{len(pages)}] {page.get('title') or 'Untitled'}")
        try:
            chunks.append(page_to_markdown(session, page, assets, not args.no_ocr, n))
        except requests.RequestException as e:
            print(f"    skipped: {e}", file=sys.stderr)

    md_path = out_dir / f"{slug(path.split(' / ')[-1])}.md"
    md_path.write_text("\n\n---\n\n".join(chunks))
    print(f"\nWrote {md_path}")

    if not args.no_docx:
        import pypandoc  # bundled binary via pypandoc-binary; no system pandoc needed

        docx_path = md_path.with_suffix(".docx")
        pypandoc.convert_file(
            str(md_path), "docx", outputfile=str(docx_path),
            extra_args=[f"--resource-path={out_dir}"],
        )
        print(f"Wrote {docx_path}")


if __name__ == "__main__":
    main()
