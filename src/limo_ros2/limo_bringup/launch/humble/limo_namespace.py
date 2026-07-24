import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, GroupAction
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node, PushRosNamespace, SetRemap

def generate_launch_description():
    # Déclarer le namespace en argument (par défaut tb3_1)
    namespace_arg = DeclareLaunchArgument(
        'namespace',
        default_value='tb3_2',
        description='Robot namespace'
    )
    namespace = LaunchConfiguration('namespace')
    
    rf2o_dir = get_package_share_directory('rf2o_laser_odometry')
    ydlidar_ros_dir = get_package_share_directory("ydlidar_ros2_driver")
    limo_base_dir = get_package_share_directory('limo_base')
    limo_bringup_dir = get_package_share_directory('limo_bringup')
    #limo_gazebo = get_package_share_directory('limo_car')
    orbbec_dir = get_package_share_directory('orbbec_camera')

    base_link_to_laser_tf_node = Node(
        package='tf2_ros',
        executable='static_transform_publisher',
        name='base_link_to_base_laser_ydlidar',
        arguments=['0.1','0','0.18','0','0','0','1','base_link','laser_link']
    )

    # Grouper tous les nœuds avec le namespace
    nodes = GroupAction(
        actions=[
            PushRosNamespace(namespace),
            
            SetRemap(src='/tf', dst='tf'),
            SetRemap(src='/tf_static', dst='tf_static'),

            IncludeLaunchDescription(
                PythonLaunchDescriptionSource([limo_base_dir,'/launch','/limo_base.launch.py']),
            ),  
            IncludeLaunchDescription(
                PythonLaunchDescriptionSource([rf2o_dir,'/launch','/rf2o_laser_odometry.launch.py']),
            ),
            IncludeLaunchDescription(
                PythonLaunchDescriptionSource([orbbec_dir, '/launch', '/dabai.launch.py']),
            ),
            IncludeLaunchDescription(
                PythonLaunchDescriptionSource([ydlidar_ros_dir,'/launch','/ydlidar.launch.py']),
            ),
            Node(
                package='tf2_ros',
                executable='static_transform_publisher',
                name='base_link_to_camera',
                arguments=['0.1','0','0.2','0','0','0','1','base_link','camera_link'],
            ),
           base_link_to_laser_tf_node
        ]
    )

    return LaunchDescription([
        namespace_arg,
        nodes
    ])
