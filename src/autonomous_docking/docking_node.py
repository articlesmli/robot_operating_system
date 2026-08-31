import rclpy
from rclpy.node import Node
from visualization_msgs.msg import Marker
from nav_msgs.msg import Path
from geometry_msgs.msg import PoseStamped
import math

class AUVController(Node):
    def __init__(self):
        super().__init__('auv_controller')
        
        # Publishers
        self.auv_pub = self.create_publisher(Marker, '/auv_visual', 10)
        self.dock_pub = self.create_publisher(Marker, '/dock_station_marker', 10)
        self.path_pub = self.create_publisher(Path, '/auv_path', 10)
        
        # Timer (10 Hz)
        self.timer = self.create_timer(0.1, self.control_loop)
        
        # State variables
        self.x_current = 0.0
        self.y_current = 0.0
        self.x_target = 10.0
        self.y_target = 0.0
        
        # Ocean current drift parameters
        self.current_x_drift = 0.01
        self.current_y_drift = 0.4
        
        # PID control variables for lateral drift correction
        self.integral_y = 0.0
        self.prev_error_y = 0.0
        
        self.path_msg = Path()
        self.path_msg.header.frame_id = 'imu_link'

    def control_loop(self):
        dt = 0.1
        
        # Stop once the AUV reaches or passes the target X position
        if self.x_current < self.x_target:
            v_cmd = 0.5
        else:
            v_cmd = 0.0
            self.current_x_drift = 0.0
            self.current_y_drift = 0.0
            self.x_current = self.x_target
            self.y_current = self.y_target

        # Cross-track error for lateral drift correction
        error_y = self.y_target - self.y_current
        self.integral_y += error_y * dt
        derivative_y = (error_y - self.prev_error_y) / dt
        self.prev_error_y = error_y

        # PID gains for lateral drift
        kp_y, kd_y = 0.3, 0.2
        lateral_correction = (kp_y * error_y) + (kd_y * derivative_y)

        # Update position incorporating forward command and ocean drift (only when moving)
        if v_cmd > 0.0:
            self.x_current += (v_cmd + self.current_x_drift) * dt
            self.y_current += (lateral_correction + self.current_y_drift) * dt

        # Calculate distance for marker color change state
        distance = math.sqrt((self.x_target - self.x_current)**2 + (self.y_target - self.y_current)**2)

        # Publish AUV Marker (Turns green when docked)
        auv_marker = Marker()
        auv_marker.header.frame_id = 'imu_link'
        auv_marker.header.stamp = self.get_clock().now().to_msg()
        auv_marker.ns = 'auv_visual'
        auv_marker.id = 0
        auv_marker.type = Marker.SPHERE
        auv_marker.action = Marker.ADD
        auv_marker.pose.position.x = self.x_current
        auv_marker.pose.position.y = self.y_current
        auv_marker.pose.position.z = 0.0
        auv_marker.scale.x = 0.6
        auv_marker.scale.y = 0.6
        auv_marker.scale.z = 0.6
        
        if distance <= 0.1:
            auv_marker.color.r = 0.0
            auv_marker.color.g = 1.0
            auv_marker.color.b = 0.0
            auv_marker.color.a = 1.0
        else:
            auv_marker.color.r = 0.0
            auv_marker.color.g = 0.0
            auv_marker.color.b = 1.0
            auv_marker.color.a = 1.0
            
        self.auv_pub.publish(auv_marker)

        # Publish Dock Station Marker (Red Cylinder at x=10.0)
        dock_marker = Marker()
        dock_marker.header.frame_id = 'imu_link'
        dock_marker.header.stamp = self.get_clock().now().to_msg()
        dock_marker.ns = 'dock_station'
        dock_marker.id = 1
        dock_marker.type = Marker.CYLINDER
        dock_marker.action = Marker.ADD
        dock_marker.pose.position.x = self.x_target
        dock_marker.pose.position.y = self.y_target
        dock_marker.pose.position.z = 0.0
        dock_marker.scale.x = 0.8
        dock_marker.scale.y = 0.8
        dock_marker.scale.z = 1.5
        dock_marker.color.r = 1.0
        dock_marker.color.g = 0.0
        dock_marker.color.b = 0.0
        dock_marker.color.a = 1.0
        self.dock_pub.publish(dock_marker)

        # Append and publish trajectory path
        pose = PoseStamped()
        pose.header.frame_id = 'imu_link'
        pose.header.stamp = self.get_clock().now().to_msg()
        pose.pose.position.x = self.x_current
        pose.pose.position.y = self.y_current
        pose.pose.orientation.w = 1.0
        self.path_msg.header.stamp = self.get_clock().now().to_msg()
        self.path_msg.poses.append(pose)
        self.path_pub.publish(self.path_msg)

def main(args=None):
    rclpy.init(args=args)
    node = AUVController()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()