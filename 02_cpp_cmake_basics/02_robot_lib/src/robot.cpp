#include "robot/robot.hpp"

#include <algorithm>
#include <utility>

namespace robot {

double clamp(double value, double low, double high) {
  return std::max(low, std::min(value, high));
}

Robot::Robot(std::string name, BatteryCallback on_change)
: name_(std::move(name)), on_change_(std::move(on_change)) {}

bool Robot::drive(double speed) {
  if (battery_ <= 20) {
    return false;
  }
  speed_ = clamp(speed, 0.0, 1.0);
  battery_ -= 10;
  if (on_change_) {
    on_change_(battery_);   // a callback, like a ROS subscription
  }
  return true;
}

}  // namespace robot
