from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from launch.actions import TimerAction

def generate_launch_description():
    # Déclarer l'argument
    robot_id_arg = DeclareLaunchArgument(
        'robot_id',
        default_value='tb3_2',
        description="Namespace du robot follower"
    )
    
    robot_id = LaunchConfiguration('robot_id')
    
    return LaunchDescription([
        robot_id_arg,
        TimerAction(period=5.0, actions=[
            Node(
                package='mimic',
                namespace=robot_id,
                executable='tb3_movement'
            )
        ])
    ])
