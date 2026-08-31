import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist, TwistWithCovarianceStamped

class DvlSensorSimulator(Node):
    def __init__(self):
        super().__init__('dvl_sensor_simulator')
        
        # Subscribe to command velocities to simulate vehicle response
        self.cmd_sub = self.create_subscription(
            Twist,
            '/cmd_vel',
            self.cmd_callback,
            10)
            
        # Publisher for simulated DVL velocity (Bottom Track)
        self.dvl_pub = self.create_publisher(
            TwistWithCovarianceStamped,
            '/dvl/velocity',
            10)
            
        self.current_speed = 0.0
        self.get_logger().info('DVL Sensor Simulator Initialized.')

    def cmd_callback(self, msg):
        # Simulate slight water resistance / latency on velocity tracking
        self.current_speed = msg.linear.x

        dvl_msg = TwistWithCovarianceStamped()
        dvl_msg.header.stamp = self.get_clock().now().to_msg()
        dvl_msg.header.frame_id = 'dvl_link'
        
        # Populate linear velocities (Surge, Sway, Heave) with small simulated noise
        dvl_msg.twist.twist.linear.x = self.current_speed + 0.01  # Minor sensor drift
        dvl_msg.twist.twist.linear.y = 0.0
        dvl_msg.twist.twist.linear.z = -0.02 # Slight downward drift compensation
        
        # Publish DVL telemetry
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
