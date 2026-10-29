// Service server in C++: the same /add_two_ints as demo_py, so either client works.
//   ros2 run demo_cpp add_two_ints_server
//   ros2 run demo_py add_two_ints_client          # sum: 5
#include <memory>

#include "example_interfaces/srv/add_two_ints.hpp"
#include "rclcpp/rclcpp.hpp"

using AddTwoInts = example_interfaces::srv::AddTwoInts;

class AddTwoIntsServer : public rclcpp::Node {
public:
  AddTwoIntsServer() : Node("minimal_service") {
    srv_ = create_service<AddTwoInts>(
      "add_two_ints",
      [this](const std::shared_ptr<AddTwoInts::Request> request,
             std::shared_ptr<AddTwoInts::Response> response) {
        response->sum = request->a + request->b;
        RCLCPP_INFO(get_logger(), "a: %ld b: %ld", request->a, request->b);
      });
  }

private:
  rclcpp::Service<AddTwoInts>::SharedPtr srv_;
};

int main(int argc, char * argv[]) {
  rclcpp::init(argc, argv);
  rclcpp::spin(std::make_shared<AddTwoIntsServer>());
  rclcpp::shutdown();
  return 0;
}
