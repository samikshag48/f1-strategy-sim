from __future__ import annotations
from .sim import Strategy, Stint, Compound, RaceParams, validate_strategy


def one_stop(params: RaceParams, pit_lap: int, first: Compound, second: Compound) -> Strategy:
    # pit after pit_lap -> first stint ends at pit_lap
    s1 = Stint(first, start_lap=1, end_lap=pit_lap)
    s2 = Stint(second, start_lap=pit_lap + 1, end_lap=params.laps)
    strat = Strategy(name=f"1-stop {first.value}->{second.value} @L{pit_lap}", stints=(s1, s2))
    validate_strategy(params, strat)
    return strat


def two_stop(params: RaceParams, pit1: int, pit2: int, c1: Compound, c2: Compound, c3: Compound) -> Strategy:
    s1 = Stint(c1, 1, pit1)
    s2 = Stint(c2, pit1 + 1, pit2)
    s3 = Stint(c3, pit2 + 1, params.laps)
    strat = Strategy(name=f"2-stop {c1.value}->{c2.value}->{c3.value} @L{pit1},L{pit2}", stints=(s1, s2, s3))
    validate_strategy(params, strat)
    return strat
