#include <chrono>
#include <memory>
#include <string>
#include "rclcpp/rclcpp.hpp"
#include "std_msgs/msg/string.hpp"

using namespace std::chrono_literals;

class SonarPublisher : public rclcpp::Node {
public:
    SonarPublisher() : Node("sonar_publisher"), count_(0) {
        publisher_ = this->create_publisher<std_msgs::msg::String>("sonar_data", 10);
        timer_ = this->create_wall_timer(
            1s, std::bind(&SonarPublisher::timer_callback, this));
    }

private:
    void timer_callback() {
        auto message = std_msgs::msg::String();
        message.data = "Sonar Ping Distance: " + std::to_string(count_++) + "m";
        RCLCPP_INFO(this->get_logger(), "Publishing: '%s'", message.data.c_str());
        publisher_->publish(message);
    }
    
    rclcpp::Publisher<std_msgs::msg::String>::SharedPtr publisher_;
    rclcpp::TimerBase::SharedPtr timer_;
    size_t count_;
};

int main(int argc, char * argv[]) {
    rclcpp::init(argc, argv);
    rclcpp::spin(std::make_shared<SonarPublisher>());
    rclcpp::shutdown();
    return 0;
}
