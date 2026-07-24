import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource

def generate_launch_description():
    robot_id = os.environ['ROBOT_NAMESPACE']
    return LaunchDescription([
        Node(
            package='qr_code',
            namespace='tb3_2',
            executable='tb3_movement'
        )
    ])

