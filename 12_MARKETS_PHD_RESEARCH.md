# THE 12 MARKETS — PhD-LEVEL RESEARCH COMPENDIUM
## Every Mechanic, Win/Lose Condition, Edge, Source & Community

**Compiled:** 2026-03-02  
**Purpose:** Deep knowledge for hedge fund formula deployment  
**Sources:** Academic papers, platform docs, Reddit, Discord, books, podcasts

---

# CATEGORY 1: PREDICTION MARKETS

## Mechanics
- **Structure:** Binary Yes/No shares priced $0.00–$1.00. Price = implied probability.
- **Trading:** Peer-to-peer; no house. Buy when you think market underprices; sell when overprices.
- **Win:** Correct shares redeem for $1.00; losing shares = $0.00.
- **Exit:** Can exit before resolution to lock profit or cut loss.
- **Fees:** Kalshi ~$0.01/contract; Polymarket US ~0.01% per trade.

## Resolution
- **Kalshi:** Centralized. "Source Agencies" (leagues, govt) determine. Internal team decides within hours.
- **Polymarket:** UMA Optimistic Oracle. Anyone proposes outcome ($750 bond). 2hr challenge. UMA token holders vote if disputed.

## Edge & Mispricing
- **Academic:** Naive traders overprice low-prob outcomes, underprice high-prob. Longshot bias.
- **Kalshi vs Polymarket:** 5%+ divergence 15–20% of time. Arbitrage opportunity.
- **Cross-platform:** ~$40M arbitrage extracted in measured period (Polymarket study).
- **Accuracy:** PredictIt 93% correct; Kalshi 78%; Polymarket 67% (2024 election). Markets often inefficient.

## Sources
- PredictorsBest.com, Polymarket docs, Kalshi news, DefiRate.com
- Academic: "Naive traders and mispricing in prediction markets" (Sciencedirect), "Arbitrage in Political Prediction Markets" (UBPLJ)
- QuantPedia: "Systematic Edges in Prediction Markets"
- AhaSignals: "Kalshi vs Polymarket Arbitrage: 5%+ Divergence"

## Communities
- **Discord:** PredictHQ (1K+ members, $5M collective profits), Kalshi official (8K members), Kalshi Trade Hub
- **Reddit:** r/predictit (political focus)

## Books
- "Information Markets: A New Way of Making Decisions" (AEI-Brookings 2006)
- Robin Hanson: "Issues In Information Market Design," "Foul Play in Information Markets"

---

# CATEGORY 2: SPORTS BETTING

## Mechanics
- **Moneyline:** Pick winner. -180 = bet $180 to win $100; +160 = bet $100 to win $160.
- **Spread:** Team wins by more or fewer points than margin. Levels favorite/underdog.
- **Totals (O/U):** Combined score over or under set number.
- **Parlay:** Multiple legs; all must win. Entire bet loses if one leg loses. Higher payout, higher risk.

## Vig/Juice (House Edge)
- **Standard -110/-110:** 4.54–4.76% vig built in.
- **Reduced juice -105:** 2.44% vig.
- **Live betting:** Often 5%+ vig.
- **Break-even:** Must win >52.4% on -110 to profit.

## Win/Lose
- **Win:** Payout = stake × (odds multiplier). +160 = $100 bet returns $260.
- **Lose:** Lose full stake.

## Sharp vs Square
- **Sharp:** +EV, data-driven, Kelly sizing. Influences lines.
- **Square:** Recreational, gut feelings; drives last-minute line movement.
- **Edge:** Find true odds > implied odds. Remove vig to get true probability.

## Sources
- ESPN, Fox Sports, BettingUSA, SportsBettingDime, Casino.org
- EdgeSlip: "Money Line Betting," "Win Probability Explained"
- Oddsshopper: "Sharp vs Square"

## Communities
- **Reddit:** r/sportsbook (450K+), r/sportsbetting (359K+)
- **Advice:** Avoid parlays; focus straight bets; avoid player props (unless sharp)

## Podcasts
- Sharp or Square (Chad Millman, Simon Hunter)
- The Sharp 600 (Jason Logan, Todd Fuhrman)

---

# CATEGORY 3: DAILY FANTASY / PICK'EM

## Mechanics (PrizePicks)
- Pick 2–6 players; predict More or Less on stat projections.
- **Power:** Higher payout, perfect picks required.
- **Flex:** Can miss 1–2 and still win (smaller payout).
- **Payouts:** 6-pick 25x, 5-pick 15x, 4-pick 10x, 3-pick 5x, 2-pick 3x.

## Rake & Overlay
- **Rake:** 10–13% (higher on low-dollar).
- **Overlay:** GPP prize pool > total entry fees. Free EV when contest unfilled.
- **Formula:** Overlay = GPP amount − (entrants × entry fee).

## Win/Lose
- **Win:** Payout based on lineup size and correct picks.
- **Lose:** Lose entry fee. Flex: partial refund if 1 miss.

## Edge
- Overlay = positive EV. Fewer entrants = higher ROI.
- Cash games: High rake + similar projections = hard to beat.
- GPP: Better risk-adjusted despite variance.

## Sources
- PrizePicks.com, OddsJam, OddsAssist, DailyFantasySports101
- OneWeekSeason: "Defining Overlay and Rake"

---

# CATEGORY 4: ESPORTS BETTING

## Mechanics
- **Odds:** Decimal (e.g., 2.50 = $2.50 return per $1).
- **Implied prob:** 1 ÷ Decimal Odds × 100.
- **Format matters:** Bo1 (high upset), Bo3 (moderate), Bo5 (low upset).

## Markets
- **LoL:** Match winner, map winner, handicap, total kills, first objectives, race to X kills.
- **CS2:** Match winner, total rounds O/U, map handicaps.
- **Share:** CS2 57%, LoL 26%, Dota 2 9%.

## Win/Lose
- Same as sports: decimal odds × stake = return.

## Sources
- TipsterCompetition, 1xbetesports, BettingInEsports, esports.gg

---

# CATEGORY 5: STOCKS & OPTIONS

## Options Mechanics
- **Call:** Right to buy at strike. Profit when stock > strike + premium.
- **Put:** Right to sell at strike. Profit when stock < strike − premium.
- **Contract:** 100 shares. Price quoted per share.

## Win/Lose
- **Call win:** Stock rises above strike + premium.
- **Call lose:** Expires worthless; lose premium. Time decay.
- **Put win:** Stock falls below strike.
- **Put lose:** Expires worthless; lose premium.

## Greeks
- **Delta:** $ change per $1 stock move. ±0.50 ATM.
- **Gamma:** Delta acceleration.
- **Theta:** Time decay (negative for long options).
- **Vega:** Sensitivity to implied volatility.

## Edge (UVRK fit)
- Buy options when IV low; sell when IV high.
- Vega = volatility exposure.

## Sources
- Investopedia, Charles Schwab, CME Group, StrikeWatch, ApexVol

---

# CATEGORY 6: CRYPTO

## Perpetual Futures
- **No expiry.** Price kept near spot via funding rates.
- **Funding:** Longs pay shorts (or vice versa) every 8hr (or 1hr on DEX).
- **Formula:** Funding = Premium Index + Interest Rate.
- **Positive funding:** Perps > spot → longs pay shorts.

## Win/Lose
- **Long:** Profit if price rises; lose if falls. Pay funding if positive.
- **Short:** Profit if price falls; lose if rises. Pay funding if negative.
- **Leverage:** Amplifies gains and losses.

## US Access
- Bitnomial (CFTC) for perpetuals, futures, options.

## Sources
- Perpstrading.org, Binance Academy, Coinbase Learn, DayTrading.co

---

# CATEGORY 7: INSURANCE-LINKED (CAT BONDS)

## Mechanics
- **Structure:** SPV issues bonds. Principal in collateral. Sponsor pays premium.
- **Typical:** 3–5yr maturity, $100M–$400M per deal.

## Win/Lose
- **Win:** No catastrophe. Get principal + interest.

- **Lose:** Triggered event (hurricane, earthquake, etc.) → forfeit principal to insurer.

## Retail Access
- Via mutual funds, closed-end funds. Not direct.

## Sources
- Wikipedia, FINRA, Investopedia, LegalClarity, III

---

# CATEGORY 8: CASINO

## House Edge
- **House edge:** Casino % advantage. RTP = 100% − edge.
- **Slots:** ~5% edge, 95% RTP. Varies by game.
- **Blackjack:** 0.3–1% with basic strategy.

## Win/Lose
- **Win:** Payout per game rules.
- **Lose:** House edge compounds over time.

## Key
- Theoretical cost = edge × total wagered.
- Blackjack: 42.22% win, 8.48% push, 49.10% loss (optimal play).

## Sources
- ActionNetwork, USBets, SlotDecoded, Casino.us, GamblingNerd

---

# CATEGORY 9: HORSE RACING

## Pari-Mutuel
- **Pool:** All bets combined. Takeout removed (15–25% US).
- **Odds:** (Pool − takeout) ÷ winning bets = payout per $1.

## Win/Lose
- **Win:** Payout from pool.
- **Lose:** Lose stake.
- **Takeout:** 15–25% US; higher on exotics (trifecta, superfecta).

## Sources
- GlobalRacing.com, GettingOutOfTheGate, Wikipedia, HarnessRacing.com

---

# CATEGORY 10: SWEEPSTAKES CASINO

## Mechanics
- **Gold Coins (GC):** Non-redeemable.
- **Sweeps Coins (SC):** Redeemable for cash.
- **Legal:** No real money wagered; sweepstakes model.

## Win/Lose
- **Win:** Accumulate SC; redeem via bank, Skrill, gift cards.
- **Lose:** Lose SC (no cash lost directly).
- **Timeline:** 5–10 working days for redemption.

## Restrictions
- Not WA, KY, ID, DE, MD (Chumba).

## Sources
- ChumbaCasino.com, TheGruelingTruth, ChumbaCasinoGames

---

# CATEGORY 11: DERIVATIVES (FUTURES)

## Mechanics
- **Contract:** Standardized; buy/sell asset at preset price, future date.
- **Margin:** Fraction of notional. Initial + maintenance.
- **Mark-to-market:** Daily P&L; margin call if below maintenance.

## Settlement
- **Cash:** Index futures settle at final price.
- **Physical:** Commodities can require delivery.

## Win/Lose
- **Win:** Price moves in your favor; profit credited.
- **Lose:** Price moves against; loss debited. Margin call possible.

## Sources
- Investopedia, JustinTrading, Bankrate, FuturesTradingPedia

---

# CATEGORY 12: UNUSUAL/NICHE MARKETS

## Examples
- **Trump SOTU:** Word counts, phrase mentions (Trillion 93%, AI 90%+). $11.97M volume on Kalshi (2026).
- **Pop culture:** South Park baby, GTA VI before X.
- **Geopolitical:** Nuclear detonation, strikes.
- **Bizarre:** Sip of water (19%), kicked out (43%), "discombobulator" (10%).

## Mechanics
- Same as prediction markets: binary, $0–$1.

## Win/Lose
- Same: $1 if correct, $0 if wrong.

## Sources
- DefiRate, Kalshi news, Washington Examiner

---

# UNIVERSAL: KELLY CRITERION

**Formula:** f* = (bp − q) / b  
- p = win prob, q = 1−p, b = decimal odds − 1

**Use:** Fractional Kelly (half, quarter). Full Kelly = aggressive.

**Critical:** Overestimating edge → over-betting → ruin.

**Sources:** Wikipedia, PuntLab, Bettored, Oddsshopper

---

# SOURCE INDEX

| Type | Examples |
|------|----------|
| **Academic** | Sciencedirect, UBPLJ, AEI-Brookings, GMU (Hanson), RePEc |
| **Platform docs** | docs.polymarket.com, news.kalshi.com |
| **News** | DefiRate, Bloomberg, Washington Examiner |
| **Reddit** | r/sportsbook, r/sportsbetting |
| **Discord** | PredictHQ, Kalshi official, Kalshi Trade Hub |
| **Podcasts** | Sharp or Square, The Sharp 600 |
| **Books** | "Information Markets" (Hahn, Tetlock, AEI 2006) |
| **Reference** | Investopedia, Wikipedia, FINRA |
| **APIs** | docs.kalshi.com, gamma-api.polymarket.com, isvdocs.polymarket.us |

---

# API REFERENCES (For Bot Building)

**Polymarket:** gamma-api.polymarket.com, clob.polymarket.com | py-clob-client, @polymarket/clob-client  
**Kalshi:** api.elections.kalshi.com/trade-api/v2 | kalshi-python, @anthropic-ai/kalshi-ts  
**Source:** AgentBets.ai, PredictorsBest.com

---

# QUICK REFERENCE: WIN/LOSE BY CATEGORY

| # | Market | Win | Lose |
|---|--------|-----|------|
| 1 | Prediction | $1/share | $0 |
| 2 | Sports | Odds × stake | Full stake |
| 3 | DFS/Pick'em | 3–25× entry | Entry fee |
| 4 | Esports | Same as sports | Full stake |
| 5 | Options | Premium → intrinsic | Full premium |
| 6 | Crypto perps | Price move − funding | Price move + funding |
| 7 | Cat bonds | Principal + interest | Principal (if triggered) |
| 8 | Casino | Game payout | House edge |
| 9 | Horse racing | Pool payout | Full stake |
| 10 | Sweepstakes | Redeem SC | Lose SC |
| 11 | Futures | Mark-to-market profit | Mark-to-market loss |
| 12 | Unusual | $1 (binary) | $0 |

---

**END OF COMPENDIUM**

© 2026 Jennifer Leigh West • The Forgotten Code Research Institute
