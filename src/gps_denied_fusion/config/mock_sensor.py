import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Imu
from nav_msgs.msg import Odometry

class MockSensorPublisher(Node):
    def __init__(self):
        super().__init__('mock_sensor_publisher')
        self.imu_pub = self.create_publisher(Imu, '/imu/data', 10)
        self.depth_pub = self.create_publisher(Odometry, '/depth/pose', 10)
        self.timer = self.create_timer(0.033, self.publish_data) # ~30 Hz
        self.z = 0.0

    def publish_data(self):
        stamp = self.get_clock().now().to_msg()

        # Publish IMU message with non-zero covariances
        imu_msg = Imu()
        imu_msg.header.stamp = stamp
        imu_msg.header.frame_id = 'imu_link'
        imu_msg.orientation.w = 1.0
        # Set orientation covariance (diagonal elements must be non-zero)
        imu_msg.orientation_covariance = [0.01, 0.0, 0.0,
                                          0.0, 0.01, 0.0,
                                          0.0, 0.0, 0.01]
        self.imu_pub.publish(imu_msg)

        # Publish Depth message with non-zero covariances
        odom_msg = Odometry()
        odom_msg.header.stamp = stamp
        odom_msg.header.frame_id = 'odom'
        odom_msg.child_frame_id = 'base_link'
        self.z -= 0.01
        odom_msg.pose.pose.position.z = self.z
        # Set pose covariance for z position (index 14 for z-z in a 6x6 matrix)
        odom_msg.pose.covariance[14] = 0.01
        self.depth_pub.publish(odom_msg)

def main(args=None):
    rclpy.init(args=args)
    node = MockSensorPublisher()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()