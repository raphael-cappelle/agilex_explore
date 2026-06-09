#!/usr/bin/env python3



import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import RegisterEventHandler
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource

from launch.event_handlers import OnProcessExit
from deux_tb3_sim.create_turtlebot3 import spawn_tb3, create_tb3_state_publisher

from time import sleep

def create_robots_node():
    nodes = []

    nb_robots = 2
    x = 0
    y = -3
    # Spawn turtlebot3 instances in gazebo
    for i in range(1, nb_robots+1):
        # Construct a unique name and namespace
        name = "turtlebot_" + str(i)
        namespace = "/tb3_" + str(i)
        nodes.append((create_tb3_state_publisher(namespace), spawn_tb3(name, namespace, x, y)))
        # Advance by 1 meter in y direction for next robot instantiation
        y -= 1

    return nodes

def generate_launch_description():
    ld = LaunchDescription()

    world = os.path.join(get_package_share_directory("deux_tb3_sim"), "worlds", "empty_world.world")

    gzserver_cmd = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(get_package_share_directory("gazebo_ros"), "launch", "gzserver.launch.py")
        ),
        launch_arguments={"world": world}.items(),
    )

    gzclient_cmd = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(get_package_share_directory("gazebo_ros"), "launch", "gzclient.launch.py")
        ),
    )

    ld.add_action(gzserver_cmd)
    ld.add_action(gzclient_cmd)

    sleep(1)
    
    last_action = None    
    for state_publisher, spawn_robot in create_robots_node():
        if last_action is None:
            # Call add_action directly for the first robot to facilitate chain instantiation via RegisterEventHandler
            ld.add_action(state_publisher)
            ld.add_action(spawn_robot)
        else:
            # Use RegisterEventHandler to ensure next robot creation happens only after the previous one is completed.
            # Simply calling ld.add_action for spawn_entity introduces issues due to parallel run.
            spawn_robot_event = RegisterEventHandler(
                event_handler=OnProcessExit(
                    target_action=last_action,
                    on_exit=[state_publisher,
                             spawn_robot],
                )
            )
            ld.add_action(spawn_robot_event)

        # Save last instance for next RegisterEventHandler
        last_action = spawn_robot
    return ld
