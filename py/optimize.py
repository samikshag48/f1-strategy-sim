from .sim import RaceParams, monte_carlo, Compound
from .strategies import one_stop


def find_best_one_stop(
    params: RaceParams,
    first: Compound,
    second: Compound,
    lap_min: int = 10,
    lap_max: int = 40,
    n: int = 2000,
):
    best = None  # (score, mean, std, name)
    for pit_lap in range(lap_min, lap_max + 1):
        strat = one_stop(params, pit_lap, first, second)
        mean, std = monte_carlo(params, strat, n=n, seed=999)
        score = mean  # minimize expected time

        if best is None or score < best[0]:
            best = (score, mean, std, strat.name)
            print(f"NEW BEST: {strat.name}  mean={mean:.2f}s  std={std:.2f}s")

    return best


def main():
    params = RaceParams(track="Silverstone", laps=52, base_lap_time=90.0, pit_loss=22.0, fuel_effect=0.030, noise_sigma=0.35)

    print("Searching best 1-stop S->M ...")
    best_sm = find_best_one_stop(params, Compound.SOFT, Compound.MEDIUM, lap_min=10, lap_max=35, n=1500)
    print("Best:", best_sm)

    print("\nSearching best 1-stop M->H ...")
    best_mh = find_best_one_stop(params, Compound.MEDIUM, Compound.HARD, lap_min=12, lap_max=40, n=1500)
    print("Best:", best_mh)


if __name__ == "__main__":
    main()
