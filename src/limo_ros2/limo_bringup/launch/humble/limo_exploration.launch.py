# src/limo_ros2/limo_bringup/launch/humble/limo_exploration.launch.py

import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, DeclareLaunchArgument, TimerAction, ExecuteProcess
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node

def generate_launch_description():

    bringup_dir   = get_package_share_directory('limo_bringup')
    limo_base_dir = get_package_share_directory('limo_base')
    ydlidar_dir   = get_package_share_directory('ydlidar_ros2_driver')
    rf2o_dir      = get_package_share_directory('rf2o_laser_odometry')
    nav2_dir      = get_package_share_directory('nav2_bringup')

    param_dir = os.path.join(bringup_dir, 'param')

    declare_use_sim_time = DeclareLaunchArgument(
        'use_sim_time', default_value='false')
    declare_nav2_params = DeclareLaunchArgument(
        'nav2_params_file',
        default_value=os.path.join(param_dir, 'limo_slam_nav2_params.yaml'))
    declare_slam_params = DeclareLaunchArgument(
        'slam_params',
        default_value=os.path.join(param_dir, 'slam_box.yaml'))

    use_sim_time = LaunchConfiguration('use_sim_time')
    nav2_params  = LaunchConfiguration('nav2_params_file')
    slam_params  = LaunchConfiguration('slam_params')

    base_link_to_laser_tf_node = Node(
            package='tf2_ros',
            executable='static_transform_publisher',
            name='base_link_to_base_laser_ydlidar',
            arguments=['0.1','0','0.18','0','0','0','1','base_link','laser_link'])


    # 1. Base driver
    limo_base = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(limo_base_dir, 'launch', 'limo_base.launch.py')),
    )

    # 2. YDLidar driver (LifecycleNode)
    ydlidar = IncludeLaunchDescription(
            PythonLaunchDescriptionSource([ydlidar_dir, '/launch', '/ydlidar.launch.py']))
    # 4. rf2o odometry (scan → /odom + TF odom→base_link)
    rf2o = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(rf2o_dir, 'launch', 'rf2o_laser_odometry.launch.py')),
    )

    # 5. SLAM Toolbox async
    '''slam = Node(
        parameters=[slam_params, {'use_sim_time': use_sim_time}],
        package='slam_toolbox',
        executable='async_slam_toolbox_node',
        name='slam_toolbox',
        output='screen',
    )'''
    slam = IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                os.path.join(bringup_dir, 'launch','humble', 'limo_slam_box.launch.py')),)
    

    # 6. Nav2 (démarré après 8s pour laisser le temps au scan et à l'odom)
    nav2 = TimerAction(period=5.0, actions=[IncludeLaunchDescription(
                PythonLaunchDescriptionSource(
                    os.path.join(nav2_dir, 'launch', 'navigation_launch.py')),
                launch_arguments={
                    'use_sim_time': use_sim_time#,
                    #'params_file':  nav2_params,
                }.items(),
            )])

    # 7. Explorateur (démarré après 12s pour laisser Nav2 s'activer)
    explorer = TimerAction(period=8.0, actions=[Node(
                package='custom_explorer',
                executable='explorer',
                name='explorer_node',
                output='screen',
            )])

    return LaunchDescription([
        declare_use_sim_time,
        declare_nav2_params,
        declare_slam_params,
        limo_base,
        ydlidar,
        rf2o,
        slam,
        base_link_to_laser_tf_node,
        nav2,
        explorer,
    ])
