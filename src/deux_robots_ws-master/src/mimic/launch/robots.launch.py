from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node

# Launch file pour la simulation Gazebo
def generate_launch_description():
    leader_id = LaunchConfiguration('leader_id', default='tb3_1')
    follower_id =  LaunchConfiguration('follower_id', default='tb3_2')
    return LaunchDescription([
        DeclareLaunchArgument(
            'leader_id',
            default_value=leader_id,
            description="Namespace du robot qui prend la décision du nombre d'aller-retour"),
        DeclareLaunchArgument(
            'follower_id',
            default_value=follower_id,
            description="Namespace du robot qui copie les mouvements du leader"),
        Node(
            package='mimic',
            namespace=leader_id,
            executable='tb3_leader',
            parameters=[{"other_robot_id": follower_id}]
        ),
        Node(
            package='mimic',
            namespace=leader_id,
            executable='tb3_movement'
        ),
        Node(
            package='mimic',
            namespace=follower_id,
            executable='tb3_movement'
        )
    ])