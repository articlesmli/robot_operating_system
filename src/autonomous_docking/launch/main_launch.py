from launch import LaunchDescription
from launch_ros.actions import Node
import os
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():
    pkg_dir = get_package_share_directory('autonomous_docking')
    rviz_config_file = os.path.join(pkg_dir, 'rviz', 'auv_docking.rviz')

    return LaunchDescription([
        Node(
            package='autonomous_docking',
            executable='thruster_pid_node',
            name='pid_controller',
            output='screen'
        ),
        Node(
            package='autonomous_docking',
            executable='dvl_fusion_node',
            name='dvl_fusion',
            output='screen'
        ),
        Node(
            package='rviz2',
            executable='rviz2',
            name='rviz2',
            arguments=['-d', rviz_config_file],
            output='screen'
        ),
        Node(
            package='autonomous_docking',
            executable='acoustic_telemetry',
            name='acoustic_telemetry',
            output='screen'
        )
    ])
