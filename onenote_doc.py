#!/usr/bin/env python3
"""Read every page of a OneNote section via Microsoft Graph and write one Markdown + .docx doc.

Local OneNote data on macOS is an opaque revision-store cache and OneNote for Mac has no
AppleScript dictionary, so Graph is the only readable source.

  python3 onenote_doc.py --list                 # show every section path you can pull
  python3 onenote_doc.py "ADBMS/Normalization"  # pull that section -> out/
  python3 onenote_doc.py "ADBMS" --no-ocr -o ~/Desktop/notes
"""
import argparse
import base64
import json
import mimetypes
import os
import re
import sys
from pathlib import Path

import msal
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from markdownify import markdownify

load_dotenv(Path(__file__).parent / ".env")

GRAPH = "https://graph.microsoft.com/v1.0"
SCOPES = ["Notes.Read.All"]
TOKEN_CACHE = Path.home() / ".onenote_agent_token.json"
OCR_MODEL = "gemini-2.5-flash"


# ---------------------------------------------------------------- auth

def get_token():
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
        TOKEN_CACHE.write_text(cache.serialize())
        TOKEN_CACHE.chmod(0o600)  # token cache is a credential

    return result["access_token"]


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


def download_resource(session, url, dest_dir, stem):
    r = session.get(url, timeout=120)
    r.raise_for_status()
    ext = mimetypes.guess_extension(r.headers.get("Content-Type", "").split(";")[0]) or ".bin"
    path = dest_dir / f"{stem}{ext}"
    path.write_bytes(r.content)
    return path


# ---------------------------------------------------------------- ocr

def ocr(path):
    """Transcribe text in an image using Gemini. Returns '' on any failure — OCR is best-effort."""
    key = os.getenv("GEMINI_API_KEY")
    if not key:
        return ""
    mime = mimetypes.guess_type(path.name)[0] or "image/png"
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
                                     "data": base64.b64encode(path.read_bytes()).decode()}},
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


def page_to_markdown(session, page, assets, do_ocr):
    """Fetch one page's HTML, localise its images/attachments, return markdown."""
    r = session.get(f"{GRAPH}/me/onenote/pages/{page['id']}/content?includeIDs=false", timeout=120)
    r.raise_for_status()
    soup = BeautifulSoup(r.text, "lxml")
    stem = slug(page.get("title") or "untitled")
    ocr_blocks = []

    for i, img in enumerate(soup.find_all("img")):
        src = img.get("data-fullres-src") or img.get("src")
        if not src:
            continue
        try:
            path = download_resource(session, src, assets, f"{stem}-{i}")
        except requests.HTTPError as e:
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
            path = download_resource(session, src, assets, f"{stem}-att-{i}-{slug(Path(name).stem)}")
        except requests.HTTPError as e:
            print(f"    attachment {name} failed: {e}", file=sys.stderr)
            continue
        link = soup.new_tag("a", href=f"{assets.name}/{path.name}")
        link.string = f"Attachment: {name}"
        obj.replace_with(link)  # markdownify drops <object> entirely

    body = soup.body or soup
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

    session = requests.Session()
    session.headers["Authorization"] = f"Bearer {get_token()}"

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

    out_dir = Path(args.out).expanduser()
    assets = out_dir / "assets"
    assets.mkdir(parents=True, exist_ok=True)

    chunks = [f"# {path}\n\n*Source: OneNote via Microsoft Graph · {len(pages)} pages*\n"]
    for n, page in enumerate(pages, 1):
        print(f"  [{n}/{len(pages)}] {page.get('title') or 'Untitled'}")
        try:
            chunks.append(page_to_markdown(session, page, assets, not args.no_ocr))
        except requests.HTTPError as e:
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
