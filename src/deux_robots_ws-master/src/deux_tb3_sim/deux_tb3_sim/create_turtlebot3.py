import math
import os

from ament_index_python.packages import get_package_share_directory
from launch_ros.actions import Node

# Remapping is required for state publisher otherwise /tf and /tf_static will get be published on root '/' namespace
remappings = [("/tf", "tf"), ("/tf_static", "tf_static")]

TURTLEBOT3_MODEL = "burger"
deux_tb3_sim = get_package_share_directory("deux_tb3_sim")
urdf_file_name = "turtlebot3_" + TURTLEBOT3_MODEL + ".urdf"
tb3_urdf = os.path.join(deux_tb3_sim, "urdf", urdf_file_name)

def create_tb3_state_publisher(namespace):
    return Node(
                package="robot_state_publisher",
                namespace=namespace,
                executable="robot_state_publisher",
                output="screen",
                parameters=[{"use_sim_time": False,
                             "publish_frequency": 10.0}],
                remappings=remappings,
                arguments=[tb3_urdf],
            )

def spawn_tb3(name, namespace, x, y):
    return Node(
                package="gazebo_ros",
                executable="spawn_entity.py",
                arguments=[
                    "-file",
                    os.path.join(deux_tb3_sim,'models', 'turtlebot3_' + TURTLEBOT3_MODEL, 'model.sdf'),
                    "-entity",
                    name,
                    "-robot_namespace",
                    namespace,
                    "-x",
                    str(x),
                    "-y",
                    str(y),
                    "-z",
                    "0.01",
                    "-Y",
                    str(math.pi / 2),
                    "-unpause",
                ],
                output="screen",
            )