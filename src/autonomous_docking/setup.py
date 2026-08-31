import os
from glob import glob
from setuptools import setup

package_name = 'autonomous_docking'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        # Include configuration files, launch files, and rviz templates
        (os.path.join('share', package_name, 'config'), glob('config/*.yaml')),
        (os.path.join('share', package_name, 'launch'), glob('launch/*.py')),
        (os.path.join('share', package_name, 'rviz'), glob('rviz/*.rviz')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='ivanovaml',
    maintainer_email='ivanovaml@todo.todo',
    description='Autonomous docking package with EKF integration',
    license='Apache-2.0',
    tests_require=['pytest'],
    entry_points={
            'console_scripts': [
                'docking_node = autonomous_docking.docking_node:main',
                'thruster_pid_node = autonomous_docking.thruster_pid_node:main',
                'dvl_fusion_node = autonomous_docking.dvl_fusion_node:main',
                'acoustic_telemetry = autonomous_docking.acoustic_telemetry_node:main',
                'behavior_tree_node = autonomous_docking.behavior_tree_node:main',
            ],
    },
)