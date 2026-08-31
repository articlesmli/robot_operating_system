import rclpy
from rclpy.node import Node
from nav_msgs.msg import Odometry
from std_msgs.msg import Float32
from geometry_msgs.msg import Twist

class AutonomousDocking(Node):
    def __init__(self):
        super().__init__('autonomous_docking_node')
        
        # State machine and sensor variables
        self.state = 'SEARCHING'
        self.sonar_range = None
        
        # Subscriptions
        self.odom_sub = self.create_subscription(
            Odometry,
            '/odometry/filtered',
            self.odom_callback,
            10)
            
        self.sonar_sub = self.create_subscription(
            Float32,
            '/sonar/range',
            self.sonar_callback,
            10)
            
        # Thruster command publisher
        self.cmd_pub = self.create_publisher(Twist, '/cmd_vel', 10)
            
    def sonar_callback(self, msg):
        self.sonar_range = msg.data
        
    def odom_callback(self, msg):
        x = msg.pose.pose.position.x
        y = msg.pose.pose.position.y
        z = msg.pose.pose.position.z
        
        twist = Twist()
        
        # State Machine & PID-style Velocity Logic
        if self.state == 'SEARCHING':
            self.get_logger().info(f'[SEARCHING] Scanning workspace. Position X: {x:.2f}')
            twist.linear.x = 0.2  # Slow search crawl
            if x > 3.0:
                self.state = 'APPROACHING'
                self.get_logger().info('Target detected via Odometry. Switching to APPROACHING.')
                
        elif self.state == 'APPROACHING':
            self.get_logger().info(f'[APPROACHING] Moving closer. Position X: {x:.2f}')
            # Proportional control for surge toward X = 10.0
            error_x = 10.0 - x
            twist.linear.x = max(0.1, min(0.5, 0.1 * error_x))
            if x >= 10.0:
                self.state = 'ALIGNED'
                self.get_logger().warn('Close range reached. Engaging Sonar for ALIGNED phase.')
                
        elif self.state == 'ALIGNED':
            if self.sonar_range is not None:
                self.get_logger().info(f'[ALIGNED] Sonar tracking range: {self.sonar_range:.2f}m')
                # Sonar proportional control for final docking approach
                error_sonar = self.sonar_range - 1.5
                twist.linear.x = max(0.05, min(0.3, 0.1 * error_sonar))
                if self.sonar_range <= 2.0:
                    self.state = 'DOCKED'
                    self.get_logger().warn('Final approach threshold met! State: DOCKED.')
            else:
                self.get_logger().warn('Waiting for /sonar/range feed...')
                twist.linear.x = 0.0
                
        elif self.state == 'DOCKED':
            self.get_logger().info('[DOCKED] Subsea vehicle successfully secured at dock.')
            twist.linear.x = 0.0
            twist.linear.y = 0.0
            twist.angular.z = 0.0
            
        # Publish velocity commands to simulation/hardware
        self.cmd_pub.publish(twist)

def main(args=None):
    rclpy.init(args=args)
    node = AutonomousDocking()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
