import os
from launch import LaunchDescription
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node

def generate_launch_description():
    robot_id = os.environ['ROBOT_NAMESPACE']
    other_robot_id =  LaunchConfiguration('other_robot_id', default='tb3_2')
    return LaunchDescription([
        Node(
            package='rendez_vous',
            parameters=[{"other_robot_id": other_robot_id}],
            namespace=f'/{robot_id}',
            executable='tb3_follower',
        )
    ])

