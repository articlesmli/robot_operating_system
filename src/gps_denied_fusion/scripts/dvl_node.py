#!/usr/bin/python3
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist, TwistWithCovarianceStamped

class DvlSensorSimulator(Node):
    def __init__(self):
        super().__init__('dvl_sensor_simulator')
        self.cmd_sub = self.create_subscription(
            Twist,
            '/cmd_vel',
            self.cmd_callback,
            10)
        self.dvl_pub = self.create_publisher(
            TwistWithCovarianceStamped,
            '/dvl/velocity',
            10)
        self.current_speed = 0.0
        self.get_logger().info('DVL Sensor Simulator Initialized.')

    def cmd_callback(self, msg):
        self.current_speed = msg.linear.x
        dvl_msg = TwistWithCovarianceStamped()
        dvl_msg.header.stamp = self.get_clock().now().to_msg()
        dvl_msg.header.frame_id = 'dvl_link'
        dvl_msg.twist.twist.linear.x = self.current_speed + 0.01
        dvl_msg.twist.twist.linear.y = 0.0
        dvl_msg.twist.twist.linear.z = -0.02
        self.dvl_pub.publish(dvl_msg)
        self.get_logger().info(f'[DVL] Measured Surge Velocity: {dvl_msg.twist.twist.linear.x:.2f} m/s')

def main(args=None):
    rclpy.init(args=args)
    node = DvlSensorSimulator()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()