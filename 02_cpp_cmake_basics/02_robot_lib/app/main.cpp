#include <iostream>

#include "robot/robot.hpp"

int main() {
  robot::Robot r("rover", [](int b) { std::cout << "battery " << b << "%\n"; });
  for (int i = 0; i < 10; ++i) {
    if (!r.drive(0.3)) {
      std::cout << "battery low\n";
    }
  }
  std::cout << r.name() << " last speed " << r.speed() << " m/s\n";
  return 0;
}
