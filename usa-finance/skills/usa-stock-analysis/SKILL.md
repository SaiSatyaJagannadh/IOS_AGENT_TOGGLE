---
name: usa-stock-analysis
description: Analyse US stocks using the note-taker's approach — finviz screening, PE/PEG/coverage ratio, sector-relative comparison against the S&P 500, and the thematic watchlist with its stated theses. Use for US stock picking, screening, or sector analysis questions.
allowed-tools: Read, Grep, Glob, WebFetch, WebSearch
---

# US stock analysis

From *Fundamental analysis* [26], *Analysis of stock by sector* [31], *Stocks may be multibaggers*
[13], *Stocks unique* [28], *Sector stocks* [30], *Stock check list* [29], *When to buy and sell*
[21], *When to sell* [37].

## Ratios used

- **PE** — price per earnings
- **PEG** — *"PE growth term for one share, how much we are paying in future"*
- **Coverage ratio** — for dividend payers, whether the payout survives; from the balance sheet

## Screening

**finviz** is the primary screener. The note's own saved query:

```
finviz.com/screener.ashx?v=111&f=cap_mega,idx_sp500
```

Filter by sector or any other criterion from there.

## Sector-relative rule [31]

The core discipline on this page: **compare a stock to its S&P 500 sector**, not in isolation, to
judge future growth. Worked observations:

- **Colgate and Kimberly-Clark** — heavily indebted, *but still good companies*
- **Walmart** — more potential, and trading **under the industry PE**
- **Kroger** — retail store segment
- **Kraft** — packaged food, but **growth is not good**
- **Do not buy the cyclical names** on this basis

Sector data: `finance.yahoo.com/sectors/...`

## The watchlist, with the note's stated thesis [13]

| Theme | Names and reasoning |
|---|---|
| Platform / cloud | DigitalOcean (clients Google, Amazon, Microsoft), Salesforce |
| Consumer internet | Chewy (animal food), Fiverr, PayPal (owns Venmo), Uber |
| Mega cap | Amazon, Alphabet, Nvidia |
| Robotics | Intuitive Surgical (robotic surgery), Amazon (robotics), Tesla |
| AI infrastructure | Prologis (storage for AI equipment), **Nvidia's power suppliers** |
| Finance | Chubb (insurance), Ares Capital (lending), NU (banking services), Bank of Montreal (~6% dividend growth) |
| Daily necessity | PG (*"main for every grocery"*), Colgate, JNJ, Coca-Cola |
| Clean energy | Linde, BP, APD — hydrogen, solar, wind |
| Science | Hercules Capital |
| Long term | Visa vs Mastercard, PG, Chevron-type energy |
| Open research | Satellite/data-transfer, waste, water, internet cable and ISP companies |

Also: gold, and industrial ETFs via screener.

**Unique/conviction list** [28]: Microsoft, Visa, AbbVie, Home Depot, Prologis, gold.

## Honest gaps

The pages that would carry the actual buy/sell discipline — *Stock check list* [29],
*When to buy and sell stocks* [21], *When to sell* [37], *What to look* [34],
*Stocks daily wage usage analysis* [32] — captured **no text**. [29] is an Instagram link only.

These are the notes' decision rules and they are not recoverable from this export. Say so rather
than substituting generic criteria. For a checklist that *does* exist in text, the India section's
`india-stock-analysis` is far more complete.

## Scope

This encodes the note-taker's own captured research. It is **not financial advice**, and neither
this skill nor any agent using it should recommend specific buys, sells, or allocations. Surface
what the notes say, name the source page, and let the reader decide.

The notes are undated and name specific tickers. Prices, yields and theses move — verify anything
numeric before acting on it.
