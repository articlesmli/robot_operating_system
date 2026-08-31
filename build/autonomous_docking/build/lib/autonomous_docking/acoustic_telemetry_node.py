import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class AcousticTelemetry(Node):
    def __init__(self):
        super().__init__('acoustic_telemetry')
        self.get_logger().info("Acoustic Telemetry Initialized.")

def main(args=None):
    rclpy.init(args=args)
    node = AcousticTelemetry()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
