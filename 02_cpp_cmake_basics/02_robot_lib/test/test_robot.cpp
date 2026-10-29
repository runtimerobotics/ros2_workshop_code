// A plain test without a framework: returns non-zero if a check fails.
#include <cstdlib>
#include <iostream>

#include "robot/robot.hpp"

#define CHECK(cond) do { if (!(cond)) { std::cerr << "FAILED: " #cond "\n"; return EXIT_FAILURE; } } while (0)

int main() {
  CHECK(robot::clamp(5, 0, 1) == 1);
  CHECK(robot::clamp(-1, 0, 1) == 0);
  CHECK(robot::clamp(0.5, 0, 1) == 0.5);

  int calls = 0;
  robot::Robot r("rover", [&calls](int) { ++calls; });
  for (int i = 0; i < 10; ++i) r.drive(2.0);
  CHECK(calls == 8);            // 100 → 20 in steps of 10
  CHECK(r.battery() == 20);
  CHECK(r.speed() == 1.0);      // clamped
  std::cout << "all checks passed\n";
  return EXIT_SUCCESS;
}
