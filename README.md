# IOS_AGENT_TOGGLE

Export a OneNote section to Markdown and `.docx` via the Microsoft Graph API — every page,
with embedded images and attachments downloaded and diagram text transcribed.

```bash
python3 src/onenote_doc.py --list            # every section you can pull
python3 src/onenote_doc.py "System design"   # -> out/System-design.{md,docx}
python3 tests/test_onenote_doc.py            # offline tests
```

Flags: `--no-ocr` (skip image transcription), `--no-docx` (markdown only), `-o DIR`.

## Setup

Needs `ONENOTE_CLIENT_ID` in `.env` — a public-client Azure app registration with
`Notes.Read.All`. Run it without one and it prints the portal steps. To try it without
registering anything, paste a token from
[Graph Explorer](https://developer.microsoft.com/graph/graph-explorer) as
`ONENOTE_ACCESS_TOKEN`; it lasts about an hour.

OCR sends page images to the Gemini API using `GEMINI_API_KEY`. Use `--no-ocr` to keep them
local.

```bash
pip3 install msal markdownify pypandoc-binary requests beautifulsoup4 lxml python-dotenv
```

Exports land in `out*/`, which is gitignored — they are personal notes and are not committed.

MIT licensed.
