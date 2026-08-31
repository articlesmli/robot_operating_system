#include "rclcpp/rclcpp.hpp"
#include "std_msgs/msg/string.hpp"

class SonarSubscriber : public rclcpp::Node {
public:
    SonarSubscriber() : Node("sonar_subscriber") {
        subscription_ = this->create_subscription<std_msgs::msg::String>(
            "sonar_data", 10,
            std::bind(&SonarSubscriber::topic_callback, this, std::placeholders::_1));
    }

private:
    void topic_callback(const std_msgs::msg::String & msg) const {
        RCLCPP_INFO(this->get_logger(), "Received: '%s'", msg.data.c_str());
    }
    
    rclcpp::Subscription<std_msgs::msg::String>::SharedPtr subscription_;
};

int main(int argc, char * argv[]) {
    rclcpp::init(argc, argv);
    rclcpp::spin(std::make_shared<SonarSubscriber>());
    rclcpp::shutdown();
    return 0;
}
