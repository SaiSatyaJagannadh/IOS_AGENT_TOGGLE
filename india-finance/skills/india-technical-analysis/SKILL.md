---
name: india-technical-analysis
description: Chart and indicator material from the note-taker's intraday study notes — leading vs lagging indicators, overlays vs oscillators, price-volume confirmation, advance-decline ratio, and trading styles. Use for chart, indicator, candlestick, or intraday-technique questions.
allowed-tools: Read, Grep, Glob, WebFetch, WebSearch
---

# Technical analysis and intraday

From *Intraday trading by daytrader* [62], the largest page in the notes, plus
*Screener website* [65] and *Chart patterns course* [66].

> Study notes for an intraday course, not a validated system. The note's own opening framing is
> **"focus on inner self to minimise the risk factor."**

## Trading styles

- **Scalping** — 1 to 5 minute frames. Described as an *"active game, risky"*
- **Position trading** — longer holds

Big players in the same market: mutual funds, DIIs, FIIs.

## Terminology the notes correct

**Stocks vs shares** as used here: holding *multiple* companies in a demat account (HDFC, ICICI,
SBI together) versus holding shares *in one* company (ITC).

## Advance–decline ratio

```
A/D = number of advancing stocks / number of declining stocks
```

Tells whether an index or sector is **bullish or bearish on the day**. The note is explicit that
this is **for trend only, not for price**. Live data: `nseindia.com/market-data/live-equity-market`.

## Indicator taxonomy

All indicators derive from **price, volume, or open interest**.

**By signal:**
- **Leading** — useful for buy/sell entries. Example given: **Fibonacci**
- **Lagging** — useful for deciding whether to stay in or exit

**By position:**
- **Overlays** — sit on the price action: **moving averages, Fibonacci, Bollinger Bands, cloud**
- **Oscillators** — do not depend directly on price: **RSI, Stoch RSI**

## Price–volume confirmation

The core discipline on the page: **price must be supported by the volume traded.**

- Read the volume bars for the dates volume spiked — trend, news, or institutional activity
- **If volume validates the price, the move is real**; price moving without volume is not
- Chart used: `in.investing.com/equities/reliance-industries-chart`

## Screeners

Chartink and the Screener queries in `india-stock-analysis` [65].

## Gap

Large parts of [62] — the candlestick taxonomy, chart-pattern catalogue, and the worked
CRR/SLR/repo and inflation-gold-dollar relationships — are partly text and partly screenshots.
The text captured here is what survived an image-stripped export. Re-run with OCR for the rest.

## Scope

This encodes the note-taker's own captured research. It is **not financial advice** and not a
trading system. Surface what the notes say, cite the page, and let the reader decide.
