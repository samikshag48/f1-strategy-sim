from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
import math
import random
from typing import Dict, Tuple, List


class Compound(str, Enum):
    SOFT = "S"
    MEDIUM = "M"
    HARD = "H"


@dataclass(frozen=True)
class TireModel:
    # lap_penalty = base + lin*age + quad*age^2
    base: float
    lin: float
    quad: float


@dataclass(frozen=True)
class RaceParams:
    track: str = "Silverstone"
    laps: int = 52
    base_lap_time: float = 90.0      # seconds (tune later)
    pit_loss: float = 22.0           # seconds lost per pit stop (tune later)
    fuel_effect: float = 0.030       # sec improvement per lap as fuel burns off
    noise_sigma: float = 0.20        # lap-to-lap randomness (seconds)
    pit_sigma: float = 0.60


@dataclass
class Stint:
    compound: Compound
    start_lap: int        # 1-indexed
    end_lap: int          # inclusive
    start_age: int = 0    # tire age at start of stint (normally 0)


@dataclass(frozen=True)
class Strategy:
    name: str
    stints: Tuple[Stint, ...]  # must cover 1..laps exactly


DEFAULT_TIRE_MODELS: Dict[Compound, TireModel] = {
    # Reasonable placeholders. Tune later using your own intuition.
    Compound.SOFT: TireModel(base=0.00, lin=0.060, quad=0.0020),
    Compound.MEDIUM: TireModel(base=0.18, lin=0.045, quad=0.0012),
    Compound.HARD: TireModel(base=0.35, lin=0.030, quad=0.0008),
}


def validate_strategy(params: RaceParams, strat: Strategy) -> None:
    if not strat.stints:
        raise ValueError("Strategy must have at least one stint.")

    expected = 1
    for i, s in enumerate(strat.stints):
        if s.start_lap != expected:
            raise ValueError(f"Stint {i} starts at lap {s.start_lap}, expected {expected}.")
        if s.end_lap < s.start_lap:
            raise ValueError(f"Stint {i} end_lap < start_lap.")
        expected = s.end_lap + 1

    if expected != params.laps + 1:
        raise ValueError(f"Strategy does not cover full race; ends at lap {expected-1}.")


def lap_time(params: RaceParams, tire: TireModel, lap_idx: int, tire_age: int, rng: random.Random) -> float:
    # Fuel term: later laps slightly faster as fuel burns off (simple model)
    fuel_term = -params.fuel_effect * (lap_idx - 1)

    # Tire degradation
    deg = tire.base + tire.lin * tire_age + tire.quad * (tire_age ** 2)

    # Random variability
    noise = rng.gauss(0.0, params.noise_sigma)

    return params.base_lap_time + fuel_term + deg + noise


def simulate_race(
    params: RaceParams,
    strat: Strategy,
    seed: int | None = None,
    tire_models: Dict[Compound, TireModel] = DEFAULT_TIRE_MODELS,
) -> float:
    validate_strategy(params, strat)
    rng = random.Random(seed)

    total = 0.0

    pits = max(0, len(strat.stints) - 1)
    for _ in range(pits):
        pit_time = rng.gauss(params.pit_loss, params.pit_sigma)
        if pit_time < 0:
            pit_time = 0.0
        total += pit_time

    for stint in strat.stints:
        tire = tire_models[stint.compound]
        age = stint.start_age
        for lap in range(stint.start_lap, stint.end_lap + 1):
            total += lap_time(params, tire, lap, age, rng)
            age += 1

    return total


def monte_carlo(
    params: RaceParams,
    strat: Strategy,
    n: int = 5000,
    seed: int = 123,
) -> Tuple[float, float]:
    """Return (mean, std) race time across n runs."""
    rng = random.Random(seed)
    times: List[float] = []
    for _ in range(n):
        run_seed = rng.randint(0, 10**9)
        times.append(simulate_race(params, strat, seed=run_seed))

    mean = sum(times) / len(times)
    var = sum((t - mean) ** 2 for t in times) / (len(times) - 1) if len(times) > 1 else 0.0
    return mean, math.sqrt(var)
