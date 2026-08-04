---
name: onenote-doc
version: 1.0.0
description: "Read every page of a OneNote section (given a notebook/section path) via Microsoft Graph and produce one Markdown + .docx document, with embedded images downloaded and OCR'd. Use when the user asks to export, pull, read, or turn OneNote notes into a document."
allowed-tools:
  - Bash
  - Read
  - AskUserQuestion
---

# /onenote-doc

Pull a whole OneNote section into one document.

## Usage

```
/onenote-doc                          # list sections, ask which one
/onenote-doc ADBMS/Normalization      # pull that section
/onenote-doc "Basics" -o ~/Desktop    # choose the output directory
```

## Steps

1. **Resolve the section.** If the user did not name one, or named one ambiguously, run:
   ```bash
   python3 onenote_doc.py --list
   ```
   Show the paths and use AskUserQuestion to pick. Do not guess between two similar names.

2. **Export.** From the repo root:
   ```bash
   python3 onenote_doc.py "<Notebook>/<Section>" -o out
   ```
   Flags: `--no-ocr` (skip image transcription, much faster), `--no-docx` (markdown only),
   `-o DIR` (output directory, default `out/`).

3. **Report** the written paths and the page count. If pages were skipped, say which and why —
   individual page failures are logged to stderr and do not abort the run.

## First run

The first invocation prints a device-login code and URL — the user must open it in a browser and
sign in with the Microsoft account that owns the notebook. The token is cached at
`~/.onenote_agent_token.json` (mode 600) and refreshed silently afterwards; later runs need no login.

If it exits complaining `ONENOTE_CLIENT_ID is not set`, the user has to register a free Azure app
first — the error message spells out the four portal steps. Relay them, do not try to work around it.

## Constraints

- Graph is the only source. macOS keeps OneNote content in an opaque revision-store cache and
  OneNote for Mac exposes no AppleScript dictionary — there is nothing local to parse.
- OCR uses `GEMINI_API_KEY` from `.env`. Missing key or a failed call degrades to no transcription;
  it never fails the export.
- `.docx` conversion uses the pandoc binary bundled in the `pypandoc-binary` pip package. No Homebrew.

## Dependencies

`pip3 install msal markdownify pypandoc-binary` (plus `requests`, `beautifulsoup4`, `lxml`,
`python-dotenv`, already present).

## Verify

```bash
python3 test_onenote_doc.py     # offline checks for section matching + page HTML localisation
```
