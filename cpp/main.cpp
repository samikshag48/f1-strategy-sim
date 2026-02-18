#include "sim_core.hpp"
#include <chrono>
#include <iostream>
#include <numeric>
#include <vector>
#include <cmath>
#include <string>

static std::string comp_name(Compound c) {
  switch (c) {
    case Compound::Soft: return "S";
    case Compound::Medium: return "M";
    case Compound::Hard: return "H";
  }
  return "?";
}

static void mean_std(const std::vector<double>& xs, double& mean, double& sd) {
  mean = std::accumulate(xs.begin(), xs.end(), 0.0) / xs.size();
  double var = 0.0;
  for (double x : xs) var += (x - mean) * (x - mean);
  var /= (xs.size() > 1 ? (xs.size() - 1) : 1);
  sd = std::sqrt(var);
}

static void eval_strategy(
    const RaceParams& p,
    const Strategy1Stop& s,
    int N,
    unsigned seed,
    double& mean,
    double& sd,
    double& seconds_taken
) {
  std::mt19937 gen(seed);
  std::vector<double> times;
  times.reserve(N);

  auto t0 = std::chrono::high_resolution_clock::now();
  for (int i = 0; i < N; ++i) {
    times.push_back(simulate_race_1stop(p, s, gen));
  }
  auto t1 = std::chrono::high_resolution_clock::now();

  std::chrono::duration<double> dt = t1 - t0;
  seconds_taken = dt.count();

  mean_std(times, mean, sd);
}

int main() {
  RaceParams p;
  p.track = "Silverstone";
  p.laps = 52;
  p.base_lap_time = 90.0;
  p.pit_loss = 22.0;
  p.fuel_effect = 0.030;
  p.noise_sigma = 0.35;

  const int N = 50000;          // sims per candidate (increase later)
  std::vector<double> lambdas = {0.0, 0.5, 1.0, 2.0};

  // Candidate compound orders (same idea as your Python)
  struct Pair { Compound a; Compound b; };
  std::vector<Pair> pairs = {
    {Compound::Soft, Compound::Medium},
    {Compound::Soft, Compound::Hard},
    {Compound::Medium, Compound::Hard},
    {Compound::Hard, Compound::Medium},
    {Compound::Medium, Compound::Medium}, // remove if you want "must use 2 compounds"
  };

  int lap_min = 10, lap_max = 40;

  double best_score = 1e18;
  std::string best_name;
  double best_mean = 0.0, best_sd = 0.0;

  for (double lambda : lambdas) {
      double best_score = 1e18;
      std::string best_name;
      double best_mean = 0.0, best_sd = 0.0;

      std::cout << "\n=== Risk-adjusted search (lambda=" << lambda << ") ===\n";
      std::cout << "score = mean + λ·std | N=" << N << " sims/candidate\n";

      for (auto pr : pairs) {
        for (int pit = lap_min; pit <= lap_max; ++pit) {
          Strategy1Stop s{pit, pr.a, pr.b};

          double mean = 0.0, sd = 0.0, seconds = 0.0;
          eval_strategy(p, s, N, 123, mean, sd, seconds);

          double score = mean + lambda * sd;

          if (score < best_score) {
            best_score = score;
            best_mean = mean;
            best_sd = sd;
            best_name = "1-stop " + comp_name(pr.a) + "->" + comp_name(pr.b) + " @L" + std::to_string(pit);

            std::cout << "NEW BEST: " << best_name
                      << "  score=" << score
                      << " mean=" << mean
                      << " sd=" << sd
                      << " (eval " << seconds << "s)\n";
          }
        }
      }

      std::cout << "\nBEST (lambda=" << lambda << "): " << best_name
                << "\nscore=" << best_score << " mean=" << best_mean << " sd=" << best_sd << "\n";
    }

  return 0;
}
