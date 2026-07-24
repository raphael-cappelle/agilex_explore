from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='zbar_ros',
            executable='barcode_reader',
            remappings=[
                ('/image', '/image_raw')
            ]
        ),
#        Node(
#            package='image_publisher',
#            executable='camera'
#        )
    ])
