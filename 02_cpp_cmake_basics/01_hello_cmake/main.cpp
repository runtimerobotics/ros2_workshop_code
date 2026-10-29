// The smallest C++ program built with CMake.
#include <iostream>
#include <string>
#include <vector>

int main() {
  const double speed = 0.5;                       // like a Python float
  const std::string name = "turtle1";             // like a Python str
  const std::vector<std::string> joints = {"joint1", "joint2"};   // like a list

  std::cout << name << " moves at " << speed << " m/s\n";
  for (const auto & joint : joints) {
    std::cout << joint << "\n";
  }
  return 0;
}
