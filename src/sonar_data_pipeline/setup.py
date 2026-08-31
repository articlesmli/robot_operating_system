from setuptools import find_packages, setup

package_name = 'sonar_data_pipeline'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='ivanovaml',
    maintainer_email='ivanovaml@hotmail.co.uk',
    description='TODO: Package description',
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