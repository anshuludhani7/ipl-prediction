from collections import defaultdict
from typing import Iterable

from .models import Bet


def calculate_pools(bets: Iterable[Bet]) -> dict[str, int]:
    """Return W_A, W_B, and pool for a set of bets."""
    weights = defaultdict(int)
    for bet in bets:
        if bet.team in ("A", "B"):
            weights[bet.team] += bet.weight
    w_a = weights["A"]
    w_b = weights["B"]
    pool = w_a + w_b
    return {"W_A": w_a, "W_B": w_b, "pool": pool}


def calculate_multipliers(W_A: int, W_B: int) -> dict[str, float | None]:
    """Pari-mutuel multipliers as defined in spec.

    multiplier_A = Pool / W_A
    multiplier_B = Pool / W_B
    """
    pool = W_A + W_B
    multiplier_a: float | None = None
    multiplier_b: float | None = None

    profit_multiplier_a: float | None = None
    profit_multiplier_b: float | None = None


    if W_A > 0:
        multiplier_a = pool / W_A
        profit_multiplier_a = multiplier_a - 1
    if W_B > 0:
        multiplier_b = pool / W_B
        profit_multiplier_b = multiplier_b - 1
    return {
        "multiplier_A": multiplier_a,
        "multiplier_B": multiplier_b,
        "profit_multiplier_A": profit_multiplier_a,
        "profit_multiplier_B": profit_multiplier_b,
        "pool": pool,
    }

