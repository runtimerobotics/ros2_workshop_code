// A small library: the same Robot as the Python classes example.
#pragma once
#include <functional>
#include <string>

namespace robot {

double clamp(double value, double low, double high);

class Robot {
public:
  using BatteryCallback = std::function<void(int)>;

  explicit Robot(std::string name, BatteryCallback on_change = nullptr);

  // Drive one step: uses 10% battery, refuses when the battery is at 20% or below.
  bool drive(double speed);

  const std::string & name() const { return name_; }
  double speed() const { return speed_; }
  int battery() const { return battery_; }

private:
  std::string name_;
  double speed_ = 0.0;
  int battery_ = 100;
  BatteryCallback on_change_;
};

}  // namespace robot
