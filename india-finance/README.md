# india-finance

Ten skills and one agent, built from an 87-page OneNote section of personal investment research
("India money management"), exported via `src/onenote_doc.py`.

```
india-finance/
  skills/
    india-stock-analysis/    management-first checklist, valuation, screener queries
    india-mutual-funds/      selection, categories, debt funds, exit
    india-etf-index/         ETF vs index on cost, iNAV, dip rule, gold/silver
    india-insurance/         term + health shortlists, claim-rejection rules
    india-tax-planning/      LTCG/STCG harvesting, set-off, FIFO
    india-fixed-income/      FD laddering, gilt/debt, deposit insurance
    india-fno-trading/       futures/options mechanics, the 1% directional rule
    india-goal-planning/     SWP rates and sequencing, corpus targets
    india-sector-themes/     sectors, cyclicality, REITs, IPO mechanics
    india-nri-finance/       NRE/NRO, KYC, what survives the move
  agents/
    india-finance.md         routes questions across the ten
```

## Provenance

Every skill cites the page numbers it came from, e.g. *Checklist to buy a stock* [56]. Nothing
is generic finance writing — where the notes are silent, the skill says so, and where the notes
record an open question, the skill preserves it as open.

## Caveats

- **Not financial advice.** These encode one person's research method.
- **Undated.** Tax slabs, scheme limits and product names were true when written. Verify anything
  numeric or regulatory.
- **Image-heavy pages are thin.** The export that fed this stripped images, so the F&O strategy
  lists, intraday course material and several spreadsheet models are referenced but not
  reproduced. Re-running the export with OCR would recover them.

## Installing

Copies live in `.claude/skills/` and `.claude/agents/` so the harness can load them. This folder
is the canonical source — edit here, then re-copy.
