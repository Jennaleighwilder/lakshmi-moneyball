# MATH RULES THAT BIND ALL 12 MARKETS
## The Mathematical Laws That Govern Every Betting System

**Purpose:** The underlying math that constrains all gambling/betting—probability, expectation, arbitrage, ruin.  
**Compiled:** 2026-03-02

---

## 1. KOLMOGOROV PROBABILITY AXIOMS (The Foundation)

**All outcomes must obey:**

| Axiom | Rule | Formula |
|-------|------|---------|
| **Non-negativity** | Probabilities cannot be negative | P(E) ≥ 0 |
| **Unit measure** | Probabilities of all outcomes sum to 1 | P(Ω) = 1 |
| **Additivity** | Mutually exclusive events: add probabilities | P(A ∪ B) = P(A) + P(B) when A∩B = ∅ |

**Binds:** Every market. If outcomes are mutually exclusive and exhaustive, their probabilities must sum to 1.

---

## 2. EXPECTED VALUE (EV)

**Formula:**
```
EV = (P(win) × Amount Won) − (P(lose) × Amount Lost)
```

**For multiple outcomes:**
```
EV = Σ [ P(outcome_i) × Payoff(outcome_i) ]
```

**Rules:**
- EV = 0 → fair bet
- EV > 0 → +EV (favorable)
- EV < 0 → −EV (unfavorable)

**Binds:** Every bet. Long-run average outcome. House edge = −EV to player.

---

## 3. IMPLIED PROBABILITY FROM ODDS

**Decimal odds:** `P = 1 / odds`  
**American negative (−150):** `P = 150 / (150 + 100) = 60%`  
**American positive (+130):** `P = 100 / (130 + 100) = 43.48%`

**Prediction markets:** Price = probability. $0.62 = 62%.

**Binds:** All odds-based markets. Implied P must be extractable from price.

---

## 4. VIG / OVERROUND (Sportsbooks)

**Overround:** Sum of implied probabilities > 100%

```
Overround = Σ (1/odds_i) − 1
```

**Example:** −110 / −110 → 52.4% + 52.4% = 104.8% → 4.8% vig

**No-vig (true) probability:**
```
P_true(i) = P_implied(i) / Σ P_implied(all)
```

**Break-even:** Must win at rate > implied probability to profit. At −110, need >52.4%.

**Binds:** Sports, horse racing (takeout), any house-set odds.

---

## 5. NO-ARBITRAGE CONDITION

**Arbitrage exists when:**
```
Σ (1/odds_i) < 1   for all mutually exclusive outcomes
```

**No arbitrage requires:**
```
Σ P(i) ≥ 1
```

**Arbitrage profit (when ΣP < 1):**
```
Profit = (Investment / ΣP) − Investment
```

**Binds:** All markets. If arbitrage exists, it gets traded away (in theory).

---

## 6. KELLY CRITERION (Optimal Bet Sizing)

**Formula:**
```
f* = (bp − q) / b
```
- f* = fraction of bankroll to bet  
- b = net odds (decimal odds − 1)  
- p = P(win), q = 1 − p  

**Alternative:** `f* = p − q/b`

**Rules:**
- f* ≤ 0 → don't bet
- Betting 2× Kelly → zero expected growth
- Betting > 2× Kelly → certain ruin (long run)

**Binds:** Any +EV bet. Tells you max rational stake.

---

## 7. RISK OF RUIN

**Mason Malmuth (continuous):**
```
RoR = e^(-2μB/σ²)
```
- μ = win rate (edge)
- B = bankroll
- σ² = variance

**Gambler's ruin (discrete, fair game):**
```
P(ruin) = n_opponent / (n_you + n_opponent)
```

**Unfair game (p ≠ 1/2):**
```
Pᵢ = [1 − (q/p)ⁱ] / [1 − (q/p)ᴺ]
```

**Binds:** Finite bankroll. Probability you go broke before hitting goal.

---

## 8. LAW OF LARGE NUMBERS (LLN)

**Rule:** As n → ∞, sample average → expected value.

**Implication:**
- House edge compounds. More bets → closer to theoretical loss.
- +EV compounds. More bets → closer to theoretical profit.
- Variance shrinks relative to mean as n grows.

**Binds:** All repeated betting. Short-term = variance. Long-term = EV dominates.

---

## 9. PARI-MUTUEL (Horse Racing, Pools)

**Pool available:**
```
Pool_net = Pool_total × (1 − Takeout)
```

**Payout per $1 on winner:**
```
Payout = Pool_net / Amount_on_winner
```

**Takeout:** 15–26% US. Higher on exotics.

**Binds:** Horse racing, some DFS pools. You bet against the pool, not a house.

---

## 10. PREDICTION MARKET BINARY

**Price = probability** (under risk-neutral / mean-belief assumptions)

**Yes + No ≈ $1** (minus spread)

**Payoff:** $1 if correct, $0 if wrong.

**EV of buying Yes at price p:**
```
EV = P(true) × $1 − p = P(true) − p
```
+EV when P(true) > p.

**Binds:** Kalshi, Polymarket, all binary event contracts.

---

## 11. OPTIONS (Black-Scholes Framework)

**Greeks bind price to:**
- Δ (delta): dPrice/dSpot
- Γ (gamma): dΔ/dSpot
- Θ (theta): dPrice/dTime
- ν (vega): dPrice/dIV

**Put-call parity:**
```
C − P = S − K×e^(-rT)
```

**Binds:** Options markets. Arbitrage if violated.

---

## 12. MARTINGALE (Why It Fails)

**Strategy:** Double after each loss.

**Math:** Each bet independent. EV unchanged. Variance of outcome sequence unchanged.

**Ruin:** Finite bankroll + table limits → eventual bust. Consecutive losses occur with probability 1 over infinite play.

**Binds:** No system beats negative EV. Martingale only changes *when* you lose, not *whether*.

---

# SUMMARY: THE MATH THAT BINDS THEM ALL

| # | Rule | Formula / Constraint |
|---|------|----------------------|
| 1 | **Probability axioms** | P ≥ 0, ΣP = 1, additivity |
| 2 | **Expected value** | EV = Σ P(i) × Payoff(i) |
| 3 | **Odds → probability** | P = 1/odds (decimal) |
| 4 | **Vig / overround** | Σ implied P > 1 |
| 5 | **No arbitrage** | Σ P ≥ 1 (or arb exists) |
| 6 | **Kelly** | f* = (bp − q)/b; 2× Kelly = zero growth |
| 7 | **Risk of ruin** | RoR = e^(-2μB/σ²) |
| 8 | **Law of large numbers** | n→∞ ⇒ sample avg → EV |
| 9 | **Pari-mutuel** | Payout = Pool×(1−takeout) / bets_on_winner |
| 10 | **Binary price = prob** | Yes + No ≈ 1 |
| 11 | **Put-call parity** | C − P = S − K×e^(-rT) |
| 12 | **No free lunch** | Martingale / systems don't beat −EV |

---

# WHAT THIS MEANS FOR YOUR FORMULAS

- **UVRK:** Volatility (σ) feeds risk of ruin, Kelly. Low vol = can size up.
- **TESS:** P(M&A) = your edge. Kelly says: bet more when P_true > P_market.
- **EV:** Every bet reduces to EV. Your job: find P_true > P_implied.
- **Arbitrage:** Kalshi vs Polymarket divergence = ΣP < 1 somewhere. Math says it's possible.

---

**Sources:** Wikipedia, Investopedia, Wolfram MathWorld, Gambling101, FairOdds, NBER, LibreTexts, Wizard of Odds, Rutgers, StackExchange

© 2026 Jennifer Leigh West • The Forgotten Code Research Institute
