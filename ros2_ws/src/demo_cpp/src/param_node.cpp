// Declare, read, and validate a parameter in C++.
//   ros2 run demo_cpp param_node --ros-args -p my_parameter:=earth
//   ros2 param set /minimal_param_node my_parameter ""     # rejected
#include <string>
#include <vector>

#include "rclcpp/rclcpp.hpp"

using namespace std::chrono_literals;

class ParamNode : public rclcpp::Node {
public:
  ParamNode() : Node("minimal_param_node") {
    declare_parameter("my_parameter", "world");
    on_set_ = add_on_set_parameters_callback(
      [](const std::vector<rclcpp::Parameter> & params) {
        rcl_interfaces::msg::SetParametersResult result;
        result.successful = true;
        for (const auto & p : params) {
          if (p.get_name() == "my_parameter" && p.as_string().empty()) {
            result.successful = false;
            result.reason = "name is empty";
          }
        }
        return result;
      });
    timer_ = create_wall_timer(1s, [this]() {
      RCLCPP_INFO(get_logger(), "Hello %s!", get_parameter("my_parameter").as_string().c_str());
    });
  }

private:
  OnSetParametersCallbackHandle::SharedPtr on_set_;
  rclcpp::TimerBase::SharedPtr timer_;
};

int main(int argc, char * argv[]) {
  rclcpp::init(argc, argv);
  rclcpp::spin(std::make_shared<ParamNode>());
  rclcpp::shutdown();
  return 0;
}
