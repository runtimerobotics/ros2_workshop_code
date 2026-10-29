// Publish a String on /chatter every 500 ms.
//   ros2 run demo_cpp talker
#include "rclcpp/rclcpp.hpp"
#include "std_msgs/msg/string.hpp"

using namespace std::chrono_literals;

class Talker : public rclcpp::Node {
public:
  Talker() : Node("talker") {
    pub_ = create_publisher<std_msgs::msg::String>("chatter", 10);
    timer_ = create_wall_timer(500ms, [this]() {
      std_msgs::msg::String msg;
      msg.data = "Hello " + std::to_string(count_++);
      RCLCPP_INFO(get_logger(), "Publishing: '%s'", msg.data.c_str());
      pub_->publish(msg);
    });
  }

private:
  rclcpp::Publisher<std_msgs::msg::String>::SharedPtr pub_;
  rclcpp::TimerBase::SharedPtr timer_;
  size_t count_ = 0;
};

int main(int argc, char * argv[]) {
  rclcpp::init(argc, argv);
  rclcpp::spin(std::make_shared<Talker>());
  rclcpp::shutdown();
  return 0;
}
