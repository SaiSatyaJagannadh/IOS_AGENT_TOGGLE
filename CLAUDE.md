# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

A OneNote → document exporter. `onenote_doc.py` pulls every page of a named OneNote section through
the Microsoft Graph API and writes one Markdown file plus a `.docx`, downloading embedded images and
attachments and transcribing image text via Gemini.

## Layout

```
src/onenote_doc.py          the exporter (all of it)
tests/test_onenote_doc.py   offline tests; adds ../src to sys.path itself
.claude/skills|agents/      the /onenote-doc command and subagent
CLAUDE.md, README.md        must stay at the root
out*/                       export destinations, gitignored — never commit these
```

Exported notes are personal content. The ignore rule is `out*/`, deliberately wider than
one directory: an earlier `-o out_sd` slipped past a narrower `out/` rule and got pushed.

## Commands

```bash
python3 src/onenote_doc.py --list                       # list every section path available
python3 src/onenote_doc.py "ADBMS/Normalization"        # export that section to out/
python3 src/onenote_doc.py "Basics" --no-ocr --no-docx  # markdown only, no image transcription
python3 tests/test_onenote_doc.py                         # the whole test suite (offline, no network)
```

There is no test framework — `tests/test_onenote_doc.py` is plain asserts run as a script. To run a single
test, call it directly: `python3 -c "import sys; sys.path.insert(0, "tests"); import test_onenote_doc as t; t.test_resolve()"`.

## Why Graph, and not local files

macOS stores OneNote content in `~/Library/Containers/com.microsoft.onenote.mac/` as opaque
revision-store `.bin` cache files, and OneNote for Mac ships no AppleScript dictionary. There is
nothing locally parseable. Any "read OneNote faster by going local" idea is a dead end — don't retry it.

## Auth

`ONENOTE_ACCESS_TOKEN` short-circuits auth entirely — paste a token from Microsoft's Graph
Explorer (developer.microsoft.com/graph/graph-explorer, sign in, consent to Notes.Read.All, copy
the Access token tab) to prove the pipeline without any Azure app. It dies after ~1h and cannot
refresh, so it is for a first real run, not regular use.

Otherwise: MSAL device-code flow against the `common` authority, scope `Notes.Read.All`. Requires
`ONENOTE_CLIENT_ID` in `.env` — a public-client Azure app registration with "Allow public client
flows" enabled. The token cache lands at `~/.onenote_agent_token.json` (mode 600) and refreshes
silently; only the first run prompts for a browser login.

## Shape of the export

`page_to_markdown()` is where the real work happens: it fetches a page's Graph HTML, downloads each
`<img>` (preferring `data-fullres-src` over the thumbnail `src`) and each `<object>` attachment into
`out/assets/`, rewrites their URLs to local relative paths, converts `<object>` to `<a>` (markdownify
drops `<object>` outright), strips the page's duplicate title heading and demotes the rest so the
docx outline has one clean hierarchy, then converts to markdown.

Failures are deliberately non-fatal and per-page: a broken image, a failed OCR call, or a page that
500s is logged to stderr and skipped rather than aborting a long export.

## Dependencies

`msal`, `markdownify`, `pypandoc-binary` (bundles the pandoc binary — Homebrew is not installed on
this machine, so do not suggest `brew install pandoc`), plus `requests`, `beautifulsoup4`, `lxml`,
`python-dotenv`, `pillow`, already present.

## Skill and agent

`.claude/skills/onenote-doc/SKILL.md` (`/onenote-doc`) and `.claude/agents/onenote-doc.md` wrap the
script. Both are project-scoped. Keep their documented flags in sync with `main()`'s argparse.

## .env

Gitignored via the `*.env` rule. Holds `ONENOTE_CLIENT_ID` and `GEMINI_API_KEY` (used for OCR). The
`MONGODB_URI` / `JWT_SECRET` / `PORT` / `NODE_ENV` / `OPENAI_API_KEY` keys predate this code and are
unused by it.
