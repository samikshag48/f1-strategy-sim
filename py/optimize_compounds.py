from __future__ import annotations
from itertools import product
from typing import List, Tuple, Optional

from .sim import RaceParams, monte_carlo, Compound
from .strategies import one_stop


def valid_one_stop_pairs() -> List[Tuple[Compound, Compound]]:
    # You can adjust these rules later if you want to enforce "must use 2 compounds"
    pairs = [
        (Compound.SOFT, Compound.MEDIUM),
        (Compound.SOFT, Compound.HARD),
        (Compound.MEDIUM, Compound.HARD),
        (Compound.HARD, Compound.MEDIUM),
    ]
    return pairs


def find_best_one_stop_any_compounds(
    params: RaceParams,
    lap_min: int = 10,
    lap_max: int = 40,
    n: int = 2000,
    risk_lambda: float = 1.0,
) -> Tuple[float, float, float, str]:
    """
    Returns (score, mean, std, strategy_name) for best strategy by expected time.
    """
    results = []
    best = None

    for first, second in valid_one_stop_pairs():
        for pit_lap in range(lap_min, lap_max + 1):
            strat = one_stop(params, pit_lap, first, second)
            mean, std = monte_carlo(params, strat, n=n, seed=999)
            score = mean + risk_lambda * std  # minimize expected time
            results.append((first, second, pit_lap, mean, std, score))

            if best is None or score < best[0]:
                best = (score, mean, std, strat.name)
                print(f"NEW BEST: {strat.name:30s} mean={mean:.2f}s std={std:.2f}s")

    results.sort(key=lambda x: x[5])

    print("\nTop 5 strategies by risk-adjusted score:")
    for r in results[:5]:
        first, second, pit_lap, mean, std, score = r
        print(
            f"{first.value}->{second.value} @L{pit_lap} | "
            f"score={score:.2f} mean={mean:.2f} std={std:.2f}"
        )

    assert best is not None
    return best


def main():
    params = RaceParams(
        track="Silverstone",
        laps=52,
        base_lap_time=90.0,
        pit_loss=22.0,
        fuel_effect=0.030,
        noise_sigma=0.35,
    )

    print(f"Optimizing 1-stop (compound order + pit lap) on {params.track}...")

    for lam in [0.0, 0.5, 1.0, 2.0]:
        print(f"\n=== Risk-adjusted optimization (λ={lam}) ===")
        best = find_best_one_stop_any_compounds(params, lap_min=10, lap_max=40, n=1500, risk_lambda=lam)
        score, mean, std, name = best
        print(f"BEST (λ={lam}): {name} | score={score:.2f} mean={mean:.2f} std={std:.2f}")

if __name__ == "__main__":
    main()
