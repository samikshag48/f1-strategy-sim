#include "sim_core.hpp"
#include <cmath>

static TireModel tire_model(Compound c) {
  switch (c) {
    case Compound::Soft:   return {0.00, 0.060, 0.0020};
    case Compound::Medium: return {0.18, 0.045, 0.0012};
    case Compound::Hard:   return {0.35, 0.030, 0.0008};
  }
  return {0.18, 0.045, 0.0012};
}

static inline double lap_time(
    const RaceParams& p,
    const TireModel& t,
    int lap_idx,
    int tire_age,
    std::normal_distribution<double>& noise,
    std::mt19937& gen
) {
  double fuel_term = -p.fuel_effect * (lap_idx - 1);
  double deg = t.base + t.lin * tire_age + t.quad * (double)(tire_age * tire_age);
  return p.base_lap_time + fuel_term + deg + noise(gen);
}

double simulate_race_1stop(const RaceParams& p, const Strategy1Stop& s, std::mt19937& gen) {
  if (s.pit_lap < 1 || s.pit_lap >= p.laps) return 1e18;

  TireModel t1 = tire_model(s.first);
  TireModel t2 = tire_model(s.second);

  std::normal_distribution<double> noise(0.0, p.noise_sigma);

  double total = 0.0;
  // Pit stop time variance: pit_time ~ N(pit_loss, pit_sigma), clamped >= 0
  std::normal_distribution<double> pit_noise(0.0, p.pit_sigma);
  double pit_time = p.pit_loss + pit_noise(gen);
  if (pit_time < 0.0) pit_time = 0.0;
  total += pit_time;

  // stint 1: laps 1..pit_lap
  int age = 0;
  for (int lap = 1; lap <= s.pit_lap; ++lap) {
    total += lap_time(p, t1, lap, age, noise, gen);
    age++;
  }

  // stint 2: laps pit_lap+1..laps
  age = 0;
  for (int lap = s.pit_lap + 1; lap <= p.laps; ++lap) {
    total += lap_time(p, t2, lap, age, noise, gen);
    age++;
  }

  return total;
}
