---
name: india-fno-trading
description: Explain Indian futures and options mechanics and the note-taker's own option-selling playbook — the 1% directional rule, short strangle and straddle, iron fly and condor, credit spreads, the 9:30 short straddle, and Strangle 2.0. Use for F&O, options, intraday or derivatives questions.
allowed-tools: Read, Grep, Glob, WebFetch, WebSearch
---

# Indian F&O and options

From *Futures and options* [68], *Option strategies by DTT* [70], *Notes on F&O* [73],
*Options selection strike and exit* [72], *Intraday trading by daytrader* [62],
*Pledging stocks* [74], *Commodity trading* [59], *Trading and intraday tax* [60].

> This is the highest-risk material in the notes. It is a study record of one trader's approach,
> not a validated system. Sizing, stop-losses and adjustments are the note-taker's own.

## Futures mechanics [68]

- Three series: **near, next, far**. Expiry: **futures monthly Thursday, options weekly**
- `25FEBFUT` = that month's Thursday February contract; spot = live price
- **Stated purpose is hedging** — an offsetting position to cut risk from adverse moves
- Sellers need not hold full cash upfront but must fund **2–5 days before expiry** or be squared off
- Physical settlement means the seller must actually hold the shares

## The directional rule [70]

| Expected move | Action |
|---|---|
| **Greater than 1%** | **Buy** side — call buy |
| **Less than 1%** | **Sell** side — put sell |

Worked example: market 33,100, resistance 33,280 → under 1% headroom → **put sell**.

Sell side requires all three: sub-1% expected move, global markets confirming, **and**
support/resistance in confluence. Call sell only on a clear downside view.

**Thursday afternoon: avoid the sell side** — decay is already low into expiry.

## When to avoid neutral strategies

1. Company results  2. Meetings or elections  3. Global meetings or uncertainty
4. Continuous all-time highs  5. Stock not sustaining at that zone

## The strategy set [70]

**Short strangle** — the note-taker's primary. Sell a call above and a put below.
Example at 14,500: sell 15,000 call, sell 14,100 put.
- Used when the market is **range bound**
- **Indexes only, not stocks** — stock volatility breaks it. Higher probability on index
- Weekly positions; **exit above ~₹4k profit** and roll to next week's strike
- Strikes chosen by support/resistance or open interest
- Adjustment: as one leg runs, sell the other at **85–90% of the increased premium**

**Straddle** — call and put sold at the *same* strike. A strangle whose legs converge becomes a
straddle. Margin can be cut by buying 5–10% protection against the sold legs.

**Iron fly** — straddle plus bought protection. **Iron condor** — strangle plus hedging.
An iron condor tightening becomes an iron fly. The note's verdict: **"strangle is better than
anything."**

**Credit spreads** — *"follow credit strategies"* (bull put, bear call), because they profit if
the market closes neutral or in your direction.
- Market up → **bull put spread**;  market down → **bear call spread**
- **Stop loss at 0.3% of at-the-money**
- OTM buy + ATM sell keeps margin low

**Cash secured put** — regular income and acquires stock at a discount. Needs large capital.
**Covered call** — only if you already hold the shares; lot sizes demand heavy capital.
**Put calendar spread** — for volatility, but the note flags it as **stopped by SEBI — check the
rules**.

## The 9:30 short straddle [70]

For volatile markets. **Entry 9:30, exit 15:00. Stop loss 20–30% of premium, target 50%.**
Stop placed on the sold put or call at 20–30% of the premium.

## Strangle 2.0 [73]

1. **Monthly expiry only**, selected by date
2. **3% max profit** from investment — pick strikes giving 3% profit, halved across put and call
3. **0.5–0.7% per week**; exit and adjust per strangle rules if losing
4. After 0.5%, exit and re-derive strikes from profit ÷ lot size
5. Losses require adjustment, not hope

Stop loss matters; test support and resistance on stocks first.

## Option buying [70]

- **Intraday only.** Buy **in-the-money — not OTM**
- Judge by **beta and delta, not the premium**
- Respect time: expiry and events
- Worked hedge example: buy 17,700 ITM call at 195 premium, sell an 18,000 call at ~46 to protect
  capital, chosen because the 150-point spread against the 195 premium leaves the sold leg
  decaying if the market stays range bound

## Related

Pledging stocks raises trading margin [74]. Intraday and F&O carry their own tax treatment,
separate from capital gains [60].

## Gap

*Intraday trading by daytrader* [62] is the largest page in the notes (~50k chars) and is mostly
screenshots of charts; the text captured here is partial. The "5 golden rules", the paper-trade
walkthrough and several adjustment tables are referenced in [70] but exist only as images.
Re-export with OCR to recover them.

## Scope

This encodes the note-taker's own captured research method. It is **not financial advice**, and
neither this skill nor any agent using it should recommend specific buys, sells, or allocations.
Apply the checklist, surface what the notes say, name the source page, and let the reader decide.

Where the notes are uncertain they say so — preserve that uncertainty rather than resolving it.
