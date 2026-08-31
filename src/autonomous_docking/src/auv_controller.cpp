#include "rclcpp/rclcpp.hpp"
#include "visualization_msgs/msg/marker.hpp"
#include "nav_msgs/msg/path.hpp"
#include "geometry_msgs/msg/pose_stamped.hpp"
#include <cmath>

class AUVController : public rclcpp::Node {
public:
    AUVController() : Node("auv_controller") {
        // Publishers
        auv_pub_ = this->create_publisher<visualization_msgs::msg::Marker>("/auv_visual", 10);
        dock_pub_ = this->create_publisher<visualization_msgs::msg::Marker>("/dock_station_marker", 10);
        path_pub_ = this->create_publisher<nav_msgs::msg::Path>("/auv_path", 10);

        // Timer (10 Hz)
        timer_ = this->create_wall_timer(
            std::chrono::milliseconds(100),
            std::bind(&AUVController::control_loop, this));

        // State variables
        x_current_ = 0.0;
        y_current_ = 0.0;
        x_target_ = 10.0;
        y_target_ = 0.0;

        // Ocean current drift parameters
        current_x_drift_ = 0.01;
        current_y_drift_ = 0.4;

        // PID control variables for lateral drift correction
        integral_y_ = 0.0;
        prev_error_y_ = 0.0;

        path_msg_.header.frame_id = "imu_link";
    }

private:
    void control_loop() {
        double dt = 0.1;
        double v_cmd = 0.0;

        // Stop once the AUV reaches or passes the target X position
        if (x_current_ < x_target_) {
            v_cmd = 0.5;
        } else {
            v_cmd = 0.0;
            current_x_drift_ = 0.0;
            current_y_drift_ = 0.0;
            x_current_ = x_target_;
            y_current_ = y_target_;
        }

        // Cross-track error for lateral drift correction
        double error_y = y_target_ - y_current_;
        integral_y_ += error_y * dt;
        double derivative_y = (error_y - prev_error_y_) / dt;
        prev_error_y_ = error_y;

        // PID gains for lateral drift
        double kp_y = 0.3;
        double kd_y = 0.2;
        double lateral_correction = (kp_y * error_y) + (kd_y * derivative_y);

        // Update position incorporating forward command and ocean drift (only when moving)
        if (v_cmd > 0.0) {
            x_current_ += (v_cmd + current_x_drift_) * dt;
            y_current_ += (lateral_correction + current_y_drift_) * dt;
        }

        // Calculate distance for marker color change state
        double distance = std::sqrt(std::pow(x_target_ - x_current_, 2) + std::pow(y_target_ - y_current_, 2));

        // Publish AUV Marker (Turns green when docked)
        visualization_msgs::msg::Marker auv_marker;
        auv_marker.header.frame_id = "imu_link";
        auv_marker.header.stamp = this->now();
        auv_marker.ns = "auv_visual";
        auv_marker.id = 0;
        auv_marker.type = visualization_msgs::msg::Marker::SPHERE;
        auv_marker.action = visualization_msgs::msg::Marker::ADD;
        auv_marker.pose.position.x = x_current_;
        auv_marker.pose.position.y = y_current_;
        auv_marker.pose.position.z = 0.0;
        auv_marker.scale.x = 0.6;
        auv_marker.scale.y = 0.6;
        auv_marker.scale.z = 0.6;

        if (distance <= 0.1) {
            auv_marker.color.r = 0.0;
            auv_marker.color.g = 1.0;
            auv_marker.color.b = 0.0;
            auv_marker.color.a = 1.0;
        } else {
            auv_marker.color.r = 0.0;
            auv_marker.color.g = 0.0;
            auv_marker.color.b = 1.0;
            auv_marker.color.a = 1.0;
        }
        auv_pub_->publish(auv_marker);

        // Publish Dock Station Marker (Red Cylinder at x=10.0)
        visualization_msgs::msg::Marker dock_marker;
        dock_marker.header.frame_id = "imu_link";
        dock_marker.header.stamp = this->now();
        dock_marker.ns = "dock_station";
        dock_marker.id = 1;
        dock_marker.type = visualization_msgs::msg::Marker::CYLINDER;
        dock_marker.action = visualization_msgs::msg::Marker::ADD;
        dock_marker.pose.position.x = x_target_;
        dock_marker.pose.position.y = y_target_;
        dock_marker.pose.position.z = 0.0;
        dock_marker.scale.x = 0.8;
        dock_marker.scale.y = 0.8;
        dock_marker.scale.z = 1.5;
        dock_marker.color.r = 1.0;
        dock_marker.color.g = 0.0;
        dock_marker.color.b = 0.0;
        dock_marker.color.a = 1.0;
        dock_pub_->publish(dock_marker);

        // Append and publish trajectory path
        geometry_msgs::msg::PoseStamped pose;
        pose.header.frame_id = "imu_link";
        pose.header.stamp = this->now();
        pose.pose.position.x = x_current_;
        pose.pose.position.y = y_current_;
        pose.pose.orientation.w = 1.0;
        path_msg_.header.stamp = this->now();
        path_msg_.poses.push_back(pose);
        path_pub_->publish(path_msg_);
    }

    rclcpp::Publisher<visualization_msgs::msg::Marker>::SharedPtr auv_pub_;
    rclcpp::Publisher<visualization_msgs::msg::Marker>::SharedPtr dock_pub_;
    rclcpp::Publisher<nav_msgs::msg::Path>::SharedPtr path_pub_;
    rclcpp::TimerBase::SharedPtr timer_;

    double x_current_;
    double y_current_;
    double x_target_;
    double y_target_;
    double current_x_drift_;
    double current_y_drift_;
    double integral_y_;
    double prev_error_y_;
    nav_msgs::msg::Path path_msg_;
};

int main(int argc, char * argv[]) {
    rclcpp::init(argc, argv);
    auto node = std::make_shared<AUVController>();
    rclcpp::spin(node);
    rclcpp::shutdown();
    return 0;
}
