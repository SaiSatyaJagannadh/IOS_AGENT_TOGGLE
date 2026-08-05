# usa-finance

Six skills and one agent, built from the 40-page OneNote section "Usa money management",
exported via `src/onenote_doc.py`.

```
usa-finance/
  skills/
    usa-etf-selection/       VOO/VTI/QQQ/SCHD, the six-ETF set, the SCHD diversification argument
    usa-dividend-investing/  payer shortlist with theses, DRIP, dividend ETFs, coverage ratio
    usa-stock-analysis/      finviz screening, sector-relative comparison, thematic watchlist
    usa-reits/               Realty Income, LTC, Prologis, SCHH
    usa-retirement-tax/      Roth IRA vs 401(k), contribution behaviour, dividend tax
    usa-research-toolkit/    the screener/fundamentals/cloning stack, by job
  agents/
    usa-finance.md           routes across the six
```

## How this differs from `india-finance`

The India section ran 87 pages and 206 KB of text. **This one is 40 pages and 7.8 KB** — 22 of
its pages captured no text at all, because they are screenshots and the export that fed this
stripped images.

The consequence is specific and worth knowing: **the US buy/sell discipline is missing.**
*Stock check list*, *When to buy and sell stocks*, *When to sell* and *What to look* are all
empty pages. Each affected skill says so rather than filling the gap with generic advice.

Re-running the export with OCR (`src/onenote_doc.py "Usa money management"` without `--no-ocr`)
would recover most of it.

## Caveats

- **Not financial advice.** These encode one person's research.
- **Undated, and ticker-specific.** Contribution limits, yields and theses all move.

## Installing

Copies live in `.claude/skills/` and `.claude/agents/`. This folder is canonical — edit here,
then re-copy.
