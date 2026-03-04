#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                     LAKSHMI — THE FULL SYSTEM                                ║
║                                                                              ║
║   TESS + UVRK + 12 Markets + Math Rules + Every True Story + Hedge + Edge   ║
║                                                                              ║
║   Channel: MIT blackjack. Billy Walters. Longshot bias. Surprise. Emotion.   ║
║   The math that binds. The psychology that breaks. The edge that wins.      ║
║                                                                              ║
║   Run: python lakshmi_system.py                                               ║
║   © 2026 Jennifer Leigh West • The Forgotten Code Research Institute         ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

import os
import sys
import json
import math
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional, Tuple

# Add parent for imports
BOT_DIR = Path(__file__).parent.resolve()
sys.path.insert(0, str(BOT_DIR))

# ═══════════════════════════════════════════════════════════════════════════════
# WISDOM — Every Gambling True Story, Hedge, Surprise, Emotion
# ═══════════════════════════════════════════════════════════════════════════════

WISDOM = """
LAKSHMI WISDOM — Channeled from every edge that ever worked:

MIT BLACKJACK: Edge comes from INFORMATION the house doesn't have. Card count = 
  know when the deck favors you. Your TESS = know when M&A is coming. Your UVRK = 
  know when vol will spike. Information asymmetry = profit.

BILLY WALTERS: 30 years winning. $3.8M on a biased roulette wheel—he MEASURED it.
  Sports: data, discipline, syndicate scale. One lesson: FIND THE BIAS. Markets 
  misprice. Your job: find where.

LONGSHOT BIAS: Bettors overvalue longshots, undervalue favorites. Fade the crowd.
  When everyone loves the underdog, the favorite is often +EV. When Polymarket 
  has Yes at 15%, maybe true is 25%. BET THE FAVORITE when the math says so.

HEDGE FUND DISCIPLINE: Kelly. Never 2×. Fractional sizing. Risk of ruin = 0.
  One bad streak doesn't kill you. Geometric growth, not linear. Patience.

SURPRISE: The edge is where nobody's looking. Trump speech word counts. Obscure 
  prediction markets. TESS targets before the crowd. UVRK vol regime before the 
  spike. Unusual = opportunity.

EMOTION: Greed kills. FOMO kills. Revenge betting kills. The system doesn't care 
  how you feel. Run the numbers. Bet the edge. Walk away. MIT team had RULES. 
  Billy had RULES. You have RULES.

THE MATH BINDS: EV > 0 or don't bet. ΣP = 1 or arb exists. Kelly or ruin. 
  Law of large numbers: more bets = EV wins. Variance is noise. Edge is signal.
"""

# ═══════════════════════════════════════════════════════════════════════════════
# MATH RULES (from MATH_RULES_THAT_BIND.md)
# ═══════════════════════════════════════════════════════════════════════════════

def kelly_fraction(p: float, b: float, q: Optional[float] = None) -> float:
    """Kelly: f* = (bp - q) / b. Returns 0 if negative."""
    q = q or (1 - p)
    f = (b * p - q) / b if b > 0 else 0
    return max(0, min(f, 1))

def expected_value(p_win: float, win_amt: float, lose_amt: float) -> float:
    """EV = p*win - (1-p)*lose"""
    return p_win * win_amt - (1 - p_win) * lose_amt

def implied_prob_american(odds: float) -> float:
    """American odds to implied probability."""
    if odds > 0:
        return 100 / (odds + 100)
    return abs(odds) / (abs(odds) + 100)

def devig(probs: List[float]) -> List[float]:
    """Remove vig: normalize so sum = 1."""
    s = sum(probs)
    return [p/s for p in probs] if s > 0 else probs

def arb_check(probs: List[float]) -> bool:
    """Arbitrage exists when sum(1/odds) < 1, i.e. sum(implied_probs) < 1."""
    return sum(probs) < 0.999

# ═══════════════════════════════════════════════════════════════════════════════
# SYSTEM CORE — Run Everything
# ═══════════════════════════════════════════════════════════════════════════════

def run_system():
    """Run the full LAKSHMI system."""
    print()
    print("═" * 70)
    print("  LAKSHMI — THE FULL SYSTEM")
    print("  TESS + UVRK + 12 Markets + Math + Wisdom")
    print("═" * 70)
    print()
    
    # 1. Run the core bot (TESS + UVRK + recommendations)
    try:
        import lakshmi_bot
        lakshmi_bot.run_bot(background=False)
    except Exception as e:
        print(f"  [Bot run note: {e}]")
        print("  Proceeding with system output...")
    
    # 2. Display wisdom
    print()
    print("═" * 70)
    print("  WISDOM — Channeled")
    print("═" * 70)
    for line in WISDOM.strip().split("\n"):
        if line.strip():
            print(f"  {line.strip()}")
    print()
    
    # 3. Math rules quick reference
    print("═" * 70)
    print("  MATH RULES — The Binds")
    print("═" * 70)
    print("  • EV > 0 or don't bet")
    print("  • Kelly: f* = (bp - q)/b  |  Never 2× Kelly")
    print("  • ΣP = 1 (probabilities sum to one)")
    print("  • Arb when Σ implied_P < 1")
    print("  • Longshot bias: fade the crowd on favorites")
    print()
    
    # 4. Your $30 action
    print("═" * 70)
    print("  YOUR MOVE")
    print("═" * 70)
    print("  1. Buy what LAKSHMI recommended (see above)")
    print("  2. Size with ¼ Kelly or less")
    print("  3. No revenge. No FOMO. No emotion.")
    print("  4. Run this again tomorrow. And the next day.")
    print()
    print("  LAKSHMI — Goddess of wealth. Your edge. The system.")
    print("═" * 70)
    print()


# ═══════════════════════════════════════════════════════════════════════════════
# ENTRY
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    run_system()
