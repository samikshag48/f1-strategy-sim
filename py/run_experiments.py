from .sim import RaceParams, monte_carlo, Compound
from .strategies import one_stop, two_stop


def main():
    params = RaceParams(
        track="Silverstone",
        laps=52,
        base_lap_time=90.0,
        pit_loss=22.0,
        fuel_effect=0.030,
        noise_sigma=0.35,
    )

    candidates = [
        one_stop(params, pit_lap=18, first=Compound.SOFT, second=Compound.MEDIUM),
        one_stop(params, pit_lap=24, first=Compound.MEDIUM, second=Compound.HARD),
        two_stop(params, pit1=14, pit2=36, c1=Compound.SOFT, c2=Compound.MEDIUM, c3=Compound.MEDIUM),
    ]

    print(f"Track: {params.track} | Laps: {params.laps}")
    for strat in candidates:
        mean, std = monte_carlo(params, strat, n=3000, seed=7)
        print(f"{strat.name:35s} mean={mean:9.2f}s  std={std:5.2f}s")


if __name__ == "__main__":
    main()
