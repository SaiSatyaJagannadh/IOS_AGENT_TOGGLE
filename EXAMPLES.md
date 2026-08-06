# Worked examples — every skill, real output

One question per skill, answered by the `india-finance` and `usa-finance` agents reading the
actual `SKILL.md` files. **These are captured outputs, not illustrations** — nothing below was
written by hand to look good.

19 skills: 13 India, 6 USA.

---

## Verification status

Two fidelity audits were run against the source note text
(`India money management`, 87 pages; `Usa money management`, 40 pages).

**Audit 1** found fabrication and drift. All fixed:

| Finding | Fix |
|---|---|
| `india-fno-trading` claimed page [70]'s strategy list "is not in the text" — it holds 10,277 chars of prose | Rewritten around the real content |
| `india-goal-planning` claimed home-loan prepay [23] was "a spreadsheet, not prose" — it is 871 chars of prose | Real rules restored |
| Crude oil [50] described as "tracked as a signal" — page is empty | Claim removed |
| ITBees rule paraphrased inside quotation marks | Restored verbatim |
| "Spread across banks" presented as the notes' guidance | Relabelled as inference |
| NRI checklist "reproduced in order" — it was regrouped | Corrected |
| Miscitations: SIP-40-years and Fed/IT rule are [52], supplier heuristic [77] | Corrected |

**Audit 2** found **no remaining fabrication**, but 17 items of *missing essence*. All addressed:

- **Three new skills** — `india-investment-priority` [19], `india-market-basics` [47],
  `india-technical-analysis` [62]. The first is the note-taker's master allocation order and had
  been missed entirely; the second is one of the largest pages in the notebook and was cited by
  no skill at all.
- **`india-stock-analysis`** gained the full ratio set (ICR, DSCR, current, quick, D/A), the
  industry life-cycle and competitive-forces analysis, the net-profit-vs-free-cash-flow 70–80%
  test, dividend stocks [10], and the KCPLTD mnemonic [57].
- **`india-mutual-funds`** gained the SIP return strategies [36].
- **`india-sector-themes`** gained the named defence and water holdings, including the political-risk
  flag on Axiscades, plus FPO/OFS/rights-issue definitions.
- **Two overstated gaps corrected** — the intraday page [62] and the F&O strategies are text-rich,
  not "mostly screenshots" as previously claimed.

**A conflict in the source is now surfaced rather than hidden:** page [51] gives ideal ROCE/ROA as
**13–15%**, page [56] says **ROCE 30+ for three years**. The notes never reconcile these, so the
skill reports both.

---

# India — 13 skills

### india-investment-priority
**Q:** I have 2 lakhs spare. Where should it go first?

**A:** Per *Main investment* [19], the notes set a fixed sequence rather than a single "best" instrument: (1) insurance first — health, then term; (2) ETFs, bought when down 5% or more; (3) mutual funds, with step-up SIPs; (4) SWP plan; (5) stocks; (6) NPS; (7) gold. The logic is protection before returns — if health and term cover aren't already in place, the notes treat any stock or fund question as premature (see `india-insurance`). A standing rule sits alongside this: "Need to move money from high risk mfs to debt funds" — a continuous de-risking instruction, not part of the sequence itself. This is the note-taker's own captured method, not financial advice — it names an order, not a recommendation for your ₹2 lakh specifically. Check which of steps 1–4 you already have covered before deciding where new money goes.

### india-market-basics
**Q:** A stock I hold dropped 30% and I can't bring myself to sell. What do the notes say about this?

**A:** This is named directly as **sunk cost bias** in *Investor psychology* [58]: "Refusing to sell a loser hoping it recovers." The notes' counter is to ask *why* it's falling and sell junk rather than hold on hope. Related guidance from *Stock market basics* [47]: "Don't catch a falling knife" — but also, on a *quality* stock that drops, the notes say buy more rather than sell (distinguishing temporary weakness from a broken business). The notes also warn against loss aversion — fearing realizing a loss while inflation erodes uninvested money anyway. The reference given for this material is *The Art of Thinking Clearly*. The notes don't give a numeric threshold for when a drop signals "junk" versus "buy more" — that judgment isn't spelled out, so this stays an open question rather than a rule to apply mechanically.

### india-stock-analysis
**Q:** Walk me through checking whether Reliance is worth buying.

**A:** Per *Checklist to buy a stock* [56] and *Fundamental analysis by money purse* [51], **70–90% of the work is management analysis**, done first: promoter remuneration under 5–10% of profit, promoter pledging under 5–10% (69% is cited as outright rejection), no unusual related-party deals, stable CFO/auditors, clean fraud record. For Reliance specifically, the notes flag: check whether you're reading **standalone or consolidated** statements, since consolidated pulls in Jio and other subsidiaries. Only after management clears do ratios matter: ROCE — notes conflict, [56] says 30+ for three years, [51] says 13–15% ideal, unreconciled; D/E ~1, ICR >3, current ratio 1.33–3; net profit vs free cash flow should match 70–80%. Then valuation: PE against its own sector and historical median, PEG below 1. Position sizing caps any single stock at 5% of a portfolio [56].

### india-mutual-funds
**Q:** How do I pick between two small cap funds?

**A:** Per *Small cap funds* [46] and *MF how to select* [52]/[44], small cap needs a **5-year minimum horizon**, and the notes flag that **AUM above ₹10,000 cr probably won't deliver alpha** — a size ceiling worth checking on both funds. Selection criteria apply generally: always **Direct + Growth**, never dividend option; check the **fund manager's record** and flag frequent manager changes as a risk; compare **standard deviation** (lower is better) and other technical ratios like Sharpe; compare **expense ratio**, but the notes say a higher-expense fund with better performance still wins; and always benchmark against the index, not just against each other. Tools named: Value Research fund pages, AMFI. The notes also cite Nifty Smallcap's swing (−40% FY20, +118% FY21) as a reminder of the category's volatility. This is the note-taker's checklist, not a recommendation of either fund.

### india-etf-index
**Q:** Should I buy an index fund or an ETF for Nifty 50 exposure?

**A:** The notes are explicit on cost: **ETF beats index fund on charges** [5][6]. The worked example given is Nippon India ETF Nifty 50 BeES beating UTI Nifty 50 Index Fund Direct Growth on charges. Before buying the ETF, check: **AUM**, **expense ratio** (low), **tracking error** (low), and **volume/liquidity** on `nseindia.com/market-data/exchange-traded-funds-etf` — the notes stress verifying someone is actually trading it. Buy at the **iNAV** shown on the NSE site, not blindly at market price. Entry timing rule: **buy when the index falls 5% or more** — Nifty 50 BeES is named specifically. Two named exceptions where the notes prefer a fund over an ETF: Motilal Oswal Nifty Bank and Motilal Oswal Nifty 500 — no reason is given for these exceptions in the notes, so that's left open.

### india-insurance
**Q:** I'm 28 and need health insurance. What are my options?

**A:** The health insurance shortlist in [28] names **HDFC Ergo Optima Secure** for under-30, alongside Care Supreme Direct (for older parents, with waiting-period buy-down riders) and Niva Reassured Bronze 2.0+ (best premium "if you disclose honestly"). At 28, Optima Secure is the age-matched pick per the notes. Separately, the notes flag low-cost cover often missed: your bank's debit card may include cover up to ₹10 lakh if used once a month, plus government schemes PMJJBY (₹500/year, ₹2L) and PMSBY (₹20/year, ₹2L accident-only). On claims, the operational rules [28]: intimate the insurer 48 hours before planned surgery, within 24 hours for emergencies, keep every prescription, submit cash bills within 30 days, and renew before 30 days of expiry. The notes flag that health insurance rules changed and single-vs-parent cover need separate treatment — both left open, unresolved in the source.

### india-tax-planning
**Q:** I have 2 lakhs of long term gains this year. How do I reduce the tax?

**A:** Per *Tax free 0% tax* [25], LTCG is taxed at **12.5% above ₹1.25 lakh** per year, and the exemption is annual — so the notes' approach is to realise gains each year to use it up. On ₹2 lakh gains, tax applies to ₹75k above the exemption ≈ **₹9k**, versus roughly **₹47k** if unharvested — the notes' own worked example, close to your figure. After selling to use the exemption you can re-buy (buy first, then sell, if liquidity allows), optionally via another broker app if conviction holds. Also offset **LTCG against STCL** where you have losses; losses carry forward 8 years; set-off works across stocks, MFs and ETFs together. Note **FIFO applies on partial sales**, not average cost — check purchase-date lots in your broker's tax report before assuming which shares you're selling.

### india-fixed-income
**Q:** I have 15 lakhs I'll need in about 2 years. Where do I park it?

**A:** For money needed within one to two years, the notes' rule from *Fixed deposit FDs* [24] is to **ladder rather than lock a single deposit** — e.g., FD1 at 1yr 4mo, FD2 at 2yr 2 days, FD3 at 3yr, then roll each as it matures into a fresh 3-year FD. The odd tenures are deliberate since banks price specific buckets differently — check the rate card for the exact break. Also check **deposit insurance**: ₹5 lakh insured per individual per bank (the notes use Stable Money to compare FD rates, without explicitly saying to spread deposits across banks — that's an inference, not stated). *Gilt or debt vs FD* [4] adds gilt/debt funds as an alternative — check 1-year performance and AUM, use growth option only, generally better post-tax than FD over longer holds. If considering a small finance bank, the notes say check its own listed stock as a solvency sniff test.

### india-fno-trading
**Q:** Nifty is range-bound and I expect a move under 1% this week. What does the playbook say?

**A:** Per *Option strategies by DTT* [70], the notes' directional rule is explicit: expected move **under 1% → sell side**, i.e., a put sell (call sell only on a clear downside view). The sell side requires all three conditions together: sub-1% expected move, global markets confirming, and support/resistance in confluence. For range-bound conditions, the note-taker's **primary strategy is the short strangle** — sell a call above and a put below (worked example: market 14,500, sell 15,000 call / 14,100 put) — used on **indexes only, not stocks**, since stock volatility breaks it. Exit above roughly ₹4k profit and roll to next week's strike; adjust a running leg by selling the other at 85–90% of its increased premium. Avoid the sell side Thursday afternoon (decay already low), and skip neutral strategies around results, elections, or all-time highs. This is a study record of one trader's approach, flagged as the highest-risk material in the notes, not a validated system.

### india-goal-planning
**Q:** I'm 5 years from retiring and want monthly income from my corpus. How do I set that up?

**A:** *Systematic withdrawal plan monthly* [12] is the most detailed page here. Key rules: **withdraw 6–8%** to make the corpus last indefinitely; **don't run SWP from volatile funds** — small-cap-type funds fall too hard, use hybrid categories that recover faster; **move the corpus into debt/hybrid/balanced before starting** the SWP; keep a **3–5 year buffer** before withdrawals begin (which lines up with your 5-year horizon); **pause the SWP in a down market** as a sequence-of-returns defence; and **step up the withdrawal 5–6%** over time since a flat amount becomes a rising percentage of a shrinking corpus. Sequencing note: per `india-investment-priority` [19], SWP sits after insurance, ETFs and step-up SIPs in the notes' own order. *Retirement plan* [92] itself captured no text in this export — the underlying model exists only in a `DTT Retirement.xlsx` attachment, not as prose here.

### india-sector-themes
**Q:** Is the defence sector worth entering right now?

**A:** *Defense sector* [13] is direct about risk: "risk is very high and stock will have volatility, only for long term growth." The notes focus on **PSU** companies and name several technical-edge picks: **Axiscades** (flagged with a political-risk caveat — holding linked to a BJP politician), **Paras**, **Centum** (DRDO work, noted as "needs research"), **Astra Microwave** (radar), **Zen Technologies**, **AI Microsystem** — these are names the note-taker was tracking, not a buy list. Before taking any thematic/sector exposure, the notes say you need a view on cyclical vs non-cyclical dynamics, inflation, and rate direction, or stay out [52]. No entry-timing rule specific to defence is given — general thematic guidance elsewhere says invest lumpsum when a theme is down and check exit load. Whether "right now" fits that is not something the notes can answer since they're undated and don't track current conditions.

### india-nri-finance
**Q:** I'm moving to the US in 3 months. What do I need to do with my Indian accounts?

**A:** Per *NRI precautions India* [32], a 17-item checklist: convert your savings account to **NRO**, open an **NRE** account for easier money conversion, complete **NRI KYC**, check Aadhaar-related KYC issues, and convert your **demat account** to NRI status. Time-sensitive: apply for an **NRI term policy while still resident** — allow ~2 weeks for medical exams (Policybazaar named); this is harder to do after the move. Visit a **CA for taxation** before moving, especially if you hold farm land or property. On existing holdings: **EPF** should be closed if possible (after 7 years it moves to senior citizen funds); **NPS Tier 1** — NRIs can invest, and the notes prefer it over MFs for the SWP option; **PPF** continues if opened as a resident; **SGB cannot** be held as NRI; inherited property/money has no restrictions. The notes flag "visit a CA for taxation" as superseding everything else here, and the page is undated — verify current rules.

### india-technical-analysis
**Q:** A stock jumped 8% today. How do I tell if the move is real?

**A:** Per *Intraday trading by daytrader* [62], the core discipline is **price–volume confirmation**: "price must be supported by the volume traded." Check the volume bars on the day of the spike against recent history — if volume validates the price move, it's real; price moving without volume backing it is not. The notes also point to the **advance-decline ratio** (advancing stocks ÷ declining stocks) to read whether the broader index or sector is bullish or bearish that day, though it's explicitly for trend only, not price. Chart tool named: `in.investing.com/equities/reliance-industries-chart`; live A/D data via `nseindia.com/market-data/live-equity-market`. Beyond this, the notes' candlestick and chart-pattern catalogue for confirming single-day moves is largely images that didn't survive this export — that detail is a genuine gap here, not something the notes are silent on by choice.

---

# USA — 6 skills

### usa-etf-selection
**Q:** I already hold VOO. Should I add QQQ?

**A:** The notes treat VOO and VTI as interchangeable core holdings and separately work through the QQQ/SCHD question directly. QQQ is described as "most considered due to higher returns" than VOO or VTI, but the notes flag that QQQ and VOO are both already tech-heavy. Their conclusion: *"more tech related investment done in both QQQ or VOO, better invest in this SCHD"* — i.e., SCHD is the better addition because it diversifies away from the concentration QQQ would deepen, rather than doubling down on it [1][5]. VT is also named as globally diversified but with lower expected returns, and not chosen. This is the note-taker's own reasoning, not general portfolio-theory advice — per *Comparison of ETFs* [1] and *6 best ETFs* [5]. Verify current overlap/returns yourself before acting; the notes are undated.

### usa-dividend-investing
**Q:** How do I know a dividend is safe before buying for income?

**A:** The notes' one analytical rule here: check the **coverage ratio**, calculated from the balance sheet, which tells you whether a company can keep paying its dividend in the future — per *Fundamental analysis* [26]. Yield alone isn't treated as a buy reason. Worth noting the dividend page itself opens with the note-taker's own caveat: *"growth stocks are better than dividend ones"* [6] — the dividend work proceeds anyway, but that framing is theirs. Separately, dividends are described as credited after tax, so any income target should be built on the net figure [27]. The notes don't give a numeric coverage-ratio threshold or a step-by-step safety checklist beyond this — the page that would size an actual income target, *How much invest for dividend to live life* [23], captured no text (screenshot); re-export with OCR to recover it.

### usa-stock-analysis
**Q:** How should I decide whether to buy Walmart?

**A:** The notes don't give Walmart a standalone checklist, but *Analysis of stock by sector* [31] names it directly under the sector-relative rule: compare a stock to its S&P 500 sector, not in isolation, to judge future growth. On that basis, Walmart is noted as having "more potential" and trading **under the industry PE** — a relative-valuation observation, not a target price. The broader ratio toolkit used elsewhere is PE, PEG ("PE growth term for one share, how much we are paying in future"), and coverage ratio for payers [26]. The pages that would carry actual buy/sell mechanics — *Stock check list* [29], *When to buy and sell* [21], *When to sell* [37], *What to look* [34] — captured no text (screenshots); that discipline isn't recoverable from this export without OCR re-export.

### usa-reits
**Q:** Which REITs do the notes track and why?

**A:** From *REIT* [12]: **Realty Income (O)** — tenants named as 7-Eleven and other grocery/convenience names, tracked by 30-day yield; **LTC** — medical real estate; **Prologis (PLD)** — warehousing, specifically called out as "storage for AI equipment"; and **SCHH** — a REIT ETF, also tracked by 30-day yield. Realty Income also appears in the dividend notes among companies that raise their dividend every year [6], and Prologis appears on the separate conviction/"unique" list [28] — so both are treated as core rather than satellite holdings. The Prologis thesis is the note-taker's own AI-infrastructure framing: warehouse REITs as picks-and-shovels exposure to data-centre/equipment-storage demand without buying chipmakers directly, echoing the "Nvidia power suppliers" idea elsewhere in the watchlist [13].

### usa-retirement-tax
**Q:** Roth IRA or Roth 401(k) — which should I prioritise?

**A:** The notes don't state a prioritisation — they lay out eligibility and limits as captured on *Roth IRA vs 401k* [35]: a **Roth IRA** can be opened by anyone with earned income regardless of employer, with a limit of **$7k/year**; a **Roth 401(k)** is only available through an employer plan, with a **$23k** limit combined with the pre-tax side. The page is undated and IRS limits change annually, so verify current-year figures before acting. The one prescriptive behavioural note is unrelated to this choice: raise your 401(k) contribution by 10% when you get a pay raise. Nothing beyond this — job-switching/rollover mechanics and a fuller tax comparison [36] are flagged topics whose underlying content is a screenshot or video links and did not survive this export.

### usa-research-toolkit
**Q:** Where do I check what an ETF actually paid out last year?

**A:** Per the toolkit notes [14][7][9]: use **nasdaq.com/market-activity/etf/\<TICKER\>/dividend-history** (the notes give the JEPQ URL as the worked example: `nasdaq.com/market-activity/etf/jepq/dividend-history`); the same pattern's `/stocks/` equivalent works for individual dividend payers too. This is referenced both directly in the dividend notes [6][9] and in the toolkit's dividend-history entry. For DRIP maths on top of that payout history, the notes point to **marketbeat.com**, the DRIP calculator [9]. If you also want fundamentals or filings context around the payout, the toolkit lists **stockanalysis.com**, **gurufocus.com**, and **morningstar.com** as the fundamentals stack [14].

---

## What these outputs demonstrate

Behaviours worth checking for in any future change to the skills — each is visible above:

1. **The source conflict is surfaced, not hidden.** The Reliance answer reports *both* ROCE figures
   and says they are unreconciled, rather than picking the tidier one.
2. **Inference is labelled as inference.** The fixed-income answer flags that "spread deposits
   across banks" is not stated in the notes.
3. **Gaps are named, not filled.** The Walmart and dividend-income answers say which pages captured
   no text instead of substituting general knowledge.
4. **No personalised advice.** The defence answer declines to say whether "right now" is a good
   time, on the grounds the notes are undated.
5. **The note-taker's own caveats survive.** The dividend answer leads with their line that
   *"growth stocks are better than dividend ones."*

## Reproducing

```
@india-finance  I have 2 lakhs spare. Where should it go first?
@usa-finance    I already hold VOO. Should I add QQQ?
```

Or invoke a skill directly, e.g. `/india-stock-analysis`.
