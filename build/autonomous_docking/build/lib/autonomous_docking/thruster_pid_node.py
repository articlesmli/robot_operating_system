import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist, PoseStamped
from visualization_msgs.msg import Marker
from nav_msgs.msg import Path
import math

class SubseaDockingController(Node):
    def __init__(self):
        super().__init__('subsea_docking_controller')
        
        # Parameters for docking target and control
        self.declare_parameter('target_dock_x', 10.0)
        self.target_x = self.get_parameter('target_dock_x').value
        
        # Publishers
        self.cmd_vel_pub = self.create_publisher(Twist, '/cmd_vel', 10)
        self.marker_pub = self.create_publisher(Marker, '/auv_visual', 10)
        self.dock_pub = self.create_publisher(Marker, '/dock_station_marker', 10)
        self.path_pub = self.create_publisher(Path, '/auv_path', 10)
        
        # 10 Hz Control Loop Timer
        self.timer = self.create_timer(0.1, self.control_loop)
        
        # State variables
        self.path = Path()
        self.path.header.frame_id = 'imu_link'
        self.x_pos = 0.0
        self.docked = False
        
        self.get_logger().info("Step 4: Subsea Docking Controller with Proximity Logic Initialized.")

    def control_loop(self):
        twist_msg = Twist()
        
        # Calculate distance remaining to the target dock
        distance_to_dock = self.target_x - self.x_pos

        if distance_to_dock > 0.3 and not self.docked:
            # Proportional speed reduction as AUV nears the target
            twist_msg.linear.x = min(0.5, max(0.05, 0.2 * distance_to_dock))
            twist_msg.angular.z = 0.0
            
            # Update position
            self.x_pos += twist_msg.linear.x * 0.1
        else:
            # Docked state: stop movement
            twist_msg.linear.x = 0.0
            twist_msg.angular.z = 0.0
            if not self.docked:
                self.docked = True
                self.get_logger().info("SUCCESS: AUV has successfully arrived at the docking station!")

        self.cmd_vel_pub.publish(twist_msg)

        # Update and publish trajectory path
        pose = PoseStamped()
        pose.header.stamp = self.get_clock().now().to_msg()
        pose.header.frame_id = 'imu_link'
        pose.pose.position.x = self.x_pos
        pose.pose.orientation.w = 1.0
        
        self.path.header.stamp = pose.header.stamp
        self.path.poses.append(pose)
        if len(self.path.poses) > 200:
            self.path.poses.pop(0)
        self.path_pub.publish(self.path)

        # Publish visualizations
        self.publish_auv_marker()
        self.publish_dock_marker()

    def publish_auv_marker(self):
        marker = Marker()
        marker.header.frame_id = 'imu_link'
        marker.header.stamp = self.get_clock().now().to_msg()
        marker.ns = 'auv_visual'
        marker.id = 0
        marker.type = Marker.SPHERE
        marker.action = Marker.ADD
        marker.pose.position.x = self.x_pos
        marker.pose.orientation.w = 1.0
        marker.scale.x = marker.scale.y = marker.scale.z = 0.4
        # Turn green if docked, blue while cruising
        if self.docked:
            marker.color.r, marker.color.g, marker.color.b, marker.color.a = 0.0, 1.0, 0.0, 1.0
        else:
            marker.color.r, marker.color.g, marker.color.b, marker.color.a = 0.0, 0.7, 1.0, 1.0
        self.marker_pub.publish(marker)

    def publish_dock_marker(self):
        dock = Marker()
        dock.header.frame_id = 'imu_link'
        dock.header.stamp = self.get_clock().now().to_msg()
        dock.ns = 'dock_station'
        dock.id = 1
        dock.type = Marker.CYLINDER
        dock.action = Marker.ADD
        dock.pose.position.x = self.target_x
        dock.pose.position.y = 0.0
        dock.pose.position.z = 0.0
        dock.pose.orientation.w = 1.0
        dock.scale.x = dock.scale.y = 0.8
        dock.scale.z = 2.0
        dock.color.r, dock.color.g, dock.color.b, dock.color.a = 1.0, 0.2, 0.0, 1.0
        self.dock_pub.publish(dock)

def main(args=None):
    rclpy.init(args=args)
    node = SubseaDockingController()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()