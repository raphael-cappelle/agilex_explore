from launch import LaunchDescription
from launch_ros.actions import Node
import os

def generate_launch_description():
    bridge_dir = '/path/to/your/config'  # adapte

    return LaunchDescription([
        Node(
            package='domain_bridge',
            executable='domain_bridge',
            name='bridge_1_to_2',
            arguments=[os.path.join(bridge_dir, 'bridge_1_to_2.yaml')],
            output='screen',
        ),
        Node(
            package='domain_bridge',
            executable='domain_bridge',
            name='bridge_2_to_1',
            arguments=[os.path.join(bridge_dir, 'bridge_2_to_1.yaml')],
            output='screen',
        ),
    ])
