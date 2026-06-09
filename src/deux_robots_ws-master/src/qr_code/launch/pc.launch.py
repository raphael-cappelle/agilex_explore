from launch import LaunchDescription
from launch_ros.actions import Node

# Launch file pour la simulation Gazebo
def generate_launch_description():
    return LaunchDescription([
        Node(
            package='zbar_ros',
            executable='barcode_reader'
        ),
        Node(
            package='image_tools',
            executable='cam2image',
            arguments=['--ros-args', '--log-level', "ERROR"]
        ),
        Node(
            package='qr_code',
            namespace="tb0_0",
            executable='tb3_movement'
        )
    ])