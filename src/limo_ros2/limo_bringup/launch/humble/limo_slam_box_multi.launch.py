import os

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, OpaqueFunction
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory


def launch_setup(context, *args, **kwargs):
    use_sim_time = LaunchConfiguration('use_sim_time').perform(context)
    slam_params_file = LaunchConfiguration('slam_params_file').perform(context)
    init_x = float(LaunchConfiguration('init_x').perform(context))
    init_y = float(LaunchConfiguration('init_y').perform(context))
    init_yaw = float(LaunchConfiguration('init_yaw').perform(context))

    start_sync_slam_toolbox_node = Node(
        parameters=[
          slam_params_file,
          {'use_sim_time': use_sim_time == 'true',
           'map_start_pose': [init_x, init_y, init_yaw]}
        ],
        package='slam_toolbox',
        executable='sync_slam_toolbox_node',
        name='slam_toolbox',
        output='screen')

    return [start_sync_slam_toolbox_node]


def generate_launch_description():
    declare_init_x_argument = DeclareLaunchArgument(
        'init_x',
        default_value='0.0', description='init x')
    declare_init_y_argument = DeclareLaunchArgument(
        'init_y',
        default_value='0.0', description='init y')
    declare_init_yaw_argument = DeclareLaunchArgument(
        'init_yaw',
        default_value='0.0', description='init yaw')

    declare_use_sim_time_argument = DeclareLaunchArgument(
        'use_sim_time',
        default_value='false',
        description='Use simulation/Gazebo clock')
    declare_slam_params_file_cmd = DeclareLaunchArgument(
        'slam_params_file',
        default_value=os.path.join(get_package_share_directory("limo_bringup"),
                                   'param', 'slam_box.yaml'),
        description='Full path to the ROS2 parameters file to use for the slam_toolbox node')

    ld = LaunchDescription()

    ld.add_action(declare_init_x_argument)
    ld.add_action(declare_init_y_argument)
    ld.add_action(declare_init_yaw_argument)
    ld.add_action(declare_use_sim_time_argument)
    ld.add_action(declare_slam_params_file_cmd)
    ld.add_action(OpaqueFunction(function=launch_setup))

    return ld
