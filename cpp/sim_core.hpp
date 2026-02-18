#pragma once
#include <random>
#include <string>

enum class Compound { Soft, Medium, Hard };

struct TireModel {
  double base;
  double lin;
  double quad;
};

struct RaceParams {
  std::string track = "Silverstone";
  int laps = 52;
  double base_lap_time = 90.0;
  double pit_loss = 22.0;
  double fuel_effect = 0.030;
  double noise_sigma = 0.35;
  double pit_sigma = 0.60;
};


struct Strategy1Stop {
  int pit_lap;      // first stint ends at pit_lap (pit after this lap)
  Compound first;
  Compound second;
};

double simulate_race_1stop(const RaceParams& p, const Strategy1Stop& s, std::mt19937& gen);
