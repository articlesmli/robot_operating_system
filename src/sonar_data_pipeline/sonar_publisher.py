import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32

class SonarPublisher(Node):
    def __init__(self):
        super().__init__('sonar_publisher')
        self.publisher_ = self.create_publisher(Float32, 'sonar/range', 10)
        self.timer = self.create_timer(1.0, self.timer_callback)

    def timer_callback(self):
        msg = Float32()
        msg.data = 15.5  # Mock distance to target in meters
        self.publisher_.publish(msg)
        self.get_logger().info(f'Publishing Sonar Range: {msg.data} m')

def main(args=None):
    rclpy.init(args=args)
    node = SonarPublisher()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
