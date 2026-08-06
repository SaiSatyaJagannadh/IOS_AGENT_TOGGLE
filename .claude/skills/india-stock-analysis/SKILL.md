---
name: india-stock-analysis
description: Evaluate an Indian listed company using the note-taker's own fundamental checklist — management integrity, promoter pledging, PE/PEG/valuation, and screener queries. Use when asked to analyse, screen, or sanity-check an Indian stock.
allowed-tools: Read, Grep, Glob, WebFetch, WebSearch
---

# Indian stock analysis

From *Fundamental analysis by money purse* [51], *Checklist to buy a stock* [56],
*Valuation of stocks* [53], *PE ratio for good companies* [45], *Stocks Buying by DTT/PEG* [77],
*Screener website* [65], *Investor psychology* [58].

## The weighting that drives everything

**70–90% of the work is management analysis**, not ratios. The notes are emphatic about this and
repeat it in two separate pages. Ratios come after, and only for companies that already passed.

## Step 1 — Management (do this first)

| Check | Red flag |
|---|---|
| Remuneration | Taking >5–10% of profit, or above the MCA-prescribed limit → eliminate |
| Salary pattern | Identical VP remuneration year over year signals a pattern worth probing |
| Related-party transactions | Investments into promoter-relative companies → avoid |
| Promoter pledging | >5–10% is bad; the notes cite 69% as an outright rejection |
| Executive churn | CFO/auditors exiting frequently → avoid |
| Audit fees | Growing abnormally fast vs peers |
| Criminal record / media stunts | Search company + "fraud"; check *Moneylife News Bites* |
| Qualification fit | Pharma should be run by pharma people, not a tech manager |

Sources: annual report via `screener.in/company/<TICKER>/consolidated/`, conference calls via
Trendlyne, BSE annual report PDFs.

## Step 2 — Qualitative checklist

1. Understand the business completely
2. Sustainable competitive edge (the notes cite Pidilite, Titan — monopoly or industry growth)
3. Track competition — *"ICICI Securities was leading, then Zerodha came No. 1"*
4. Management stable and unchanged
5. Promoter fraud history clean

## Step 3 — Quantitative

- Cash flow, balance sheet — prefer debt-free
- Past performance, cyclical vs non-cyclical
- **ROCE 30+ for the last three years** (per [56] — but see the conflict with [51]'s 13–15% below)
- **ROE above 15% across the last 5–10 years** — from *Stock analysis by fund manager Mohan*
  [61], computed as net income ÷ average shareholders' equity, off the P&L
- **Debt-to-equity below 1** (screener queries use <0.2)
- PE under control

## Step 3b — Industry analysis [51]

**Life cycle** — where is the industry?
- **Pioneering** — just started, must show future growth
- **Maturity / saturation** — safe, brand-type companies
- **Decline** — no market growth

Worked example: PPE-kit makers profited in Covid and not since — a short-stage industry. The
internet is at maturity. Sector data: `ibef.org/industry/...`

**Competitive forces**, each with the note's own example:

| Force | Example |
|---|---|
| Level of competition | More companies around it → lower returns |
| Threat of new entrants | **Jio disrupted Airtel and Vodafone** |
| Threat to retail | **JioMart, Zepto** — medium risk, don't expect huge returns |
| Threat of substitutes | **Netflix/Prime**; **iPhone cameras** replacing camera makers |
| Supplier power | No uniqueness + limited client base → weak growth |
| Buyer power | Buyers not buying → risk |
| Entry barriers | **IRCTC, Nestlé** — network effects cap rivals' share |
| Government protection | **Harley-Davidson exited over tax** — check protection and permissions |

## Step 3c — Balance sheet and ratios [51]

Check **solvency** (can it clear debt) and **liquidity** (does it have cash flow). Know whether
you are reading **standalone** or **consolidated** statements — for Reliance, consolidated pulls
in Jio and the rest.

**Don't lead with the P&L — lead with cash flow.** The test:
> **Net profit must be high and free cash flow must match it 70–80%** for a good company.

(Cash-flow method differs for banks and NBFCs.)

| Ratio | The note's threshold |
|---|---|
| **ROI** | Must exceed **cost of capital** |
| **ROCE / ROA** | **Ideal range 13–15%** |
| **D/E** | **~1**; above 1 and rising → leave. Excludes banks, real estate, NBFCs |
| **D/A** | **< 0.5** — above it implies assets get sold to clear debt |
| **ICR** | **< 2 bad, > 3 good** |
| **DSCR** | **< 1 bad, 1.5–2 good** |
| **Current ratio** | **1.33–3 ideal**; above 3 means cash is being managed poorly |
| **Quick ratio** | **> 1 and < 2.0** |

For **banks and NBFCs use ROE only** — ROCE includes debt, which distorts them. Don't read ROE
blindly for loss-making companies.

> **Note a conflict in the source.** [51] gives ROCE/ROA ideal as **13–15%**, while
> *Checklist to buy a stock* [56] says **ROCE 30+ for three years**. The notes do not reconcile
> these. Surface both rather than picking one.

## Step 4 — Valuation

- **PE** — compare only within one sector; does not account for future earnings
- **PE vs its own median** — buy at or below the company's median PE, *only for good companies*
- **PEG** — `PE / growth`. Below 1 good, ~1 fair, >1 expensive but check growth
- **P/CF** — addresses cash flow
- **P/S** and **EV/EBITDA** for loss-making companies: 6–10 fair, above 20 expensive
- **P/B < 1** for banks/NBFCs and cyclicals
- **Intrinsic value via DCF** — Money Purse excel → upload at `screener.in/excel/`, fill yellow
  fields from Tijori, share count from BSE shareholding pattern

## Step 5 — Position sizing

- Hold **10–15 stocks** — as many as can actually be tracked
- **Max 5% to a new stock** (₹10L portfolio → ₹50k)
- Do not chase on FOMO. *"Ignoring the fundamentals won't support the market in future."*

## Screener queries [65]

```
Blue chip:  Market Cap >50000  & Sales Growth 3Y >10% & Profit Growth 3Y >10%
            & ROE > Avg ROE 3Y & ROCE > Avg ROCE 3Y & Debt/Equity <0.2
Growth:     Market Cap 5000-20000, same growth/return filters
High risk:  Market Cap 1000-10000, same growth filters
```

## Dividend stocks [10]

ITC is cited at ~3% yield. **Check the last 5 years of growth and capital** — the notes split
payers into those that grow *with* the dividend and those that don't, where risk is higher.

## Idea sourcing

Top-down by sector (Tijori) or bottom-up by screener query. Cloning is allowed —
Dataroma, Ratestar, Quant/PPFAS monthly portfolio disclosures — but the notes warn twice:
**"don't go into comfort zone by taking stocks from famous person's cloning"**; re-run your own
analysis. Look for micro-cap suppliers behind macro names (KPIT, Uno Minda → auto OEMs).

Mindset, from *Copy cat investors* [57]: **KCPLTD — Knowledge, Conviction, Patience, Lucky.**

## Scope

This encodes the note-taker's own captured research method. It is **not financial advice**, and
neither this skill nor any agent using it should recommend specific buys, sells, or allocations.
Apply the checklist, surface what the notes say, name the source page, and let the reader decide.

Where the notes are uncertain they say so — preserve that uncertainty rather than resolving it.
