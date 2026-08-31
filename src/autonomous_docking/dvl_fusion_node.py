import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist

class DVLFusionNode(Node):
    def __init__(self):
        super().__init__('dvl_fusion_node')
        self.get_logger().info("DVL Fusion Node Initialized.")

def main(args=None):
    rclpy.init(args=args)
    node = DVLFusionNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
