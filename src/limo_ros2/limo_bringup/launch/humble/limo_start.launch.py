import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node

def generate_launch_description():
    rf2o_dir = get_package_share_directory('rf2o_laser_odometry')
    ydlidar_ros_dir = get_package_share_directory("ydlidar_ros2_driver")
    limo_base_dir = get_package_share_directory('limo_base')
    limo_bringup_dir = get_package_share_directory('limo_bringup')
    limo_gazebo = get_package_share_directory('limo_car')
    orbbec_dir = get_package_share_directory('orbbec_camera')
    merger_dir = get_package_share_directory('ros2_laser_scan_merger')

    pub_tf=Node(
        package="limo_base",
        executable="tf_pub",   
        output='screen',
        name='tf_pub_node',
    )
    base_link_to_laser_tf_node = Node(
        package='tf2_ros',
        executable='static_transform_publisher',
        name='base_link_to_base_laser_ydlidar',
        arguments=['0.1','0','0.18','0','0','0','1','base_link','laser_link']
    )

    return LaunchDescription([
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource([limo_base_dir,'/launch','/limo_base.launch.py']),
        ),  
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource([rf2o_dir,'/launch','/rf2o_laser_odometry.launch.py']),
        ),
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource([orbbec_dir, '/launch', '/dabai.launch.py']),),
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource([ydlidar_ros_dir,'/launch','/ydlidar.launch.py']),
        ),
        Node(
            package='tf2_ros',
            executable='static_transform_publisher',
            name='base_link_to_camera',
            arguments=['0.1','0','0.2','0','0','0','1','base_link','camera_link'],),
        Node(
            package='depthimage_to_laserscan',
            executable='depthimage_to_laserscan_node',
            name='depthimage_to_laserscan',
            parameters=[{
                'output_frame':'camera_link',
                'range_min': 0.01,
                'range_max': 3.0,
                'scan_height': 1,
            }],
            remappings=[
                ('depth', '/camera/depth/image_raw'),
                ('depth_camera_info', '/camera/depth/camera_info'),
                ('scan','/scan_depth'),
            ],
        ),
        Node(
            package='pointcloud_to_laserscan',
            executable='pointcloud_to_laserscan_node',
            name='pointcloud_to_laserscan',
            parameters=[{
                'target_frame': 'base_link',
                'min_height': -0.15,
                'max_height': 0.5,
                'angle_min': -3.14159,
                'angle_max': 3.14159,
                'angle_increment': 0.0087,
                'range_min': 0.1,
                'range_max': 5.0,
                'use_inf': True
            }],
            remappings=[
                ('cloud_in', 'cloud_in'),
                ('scan', '/scan_merged'),
            ],
        ),
	Node(
            package='ros2_laser_scan_merger',
            executable='ros2_laser_scan_merger',
            name='ros2_laser_scan_merger',
            parameters=[
                os.path.join(merger_dir, 'config', 'params.yaml')
            ],
        ),
        # IncludeLaunchDescription(
        #     PythonLaunchDescriptionSource([limo_bringup_dir,'/launch/humble','/ekf_odom.launch.py']),
        # ), 
        # pub_tf
        base_link_to_laser_tf_node
    ])
