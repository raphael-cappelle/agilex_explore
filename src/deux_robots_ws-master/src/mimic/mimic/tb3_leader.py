import rclpy
import rclpy.duration
from rclpy.node import Node
from geometry_msgs.msg import Twist
from mimic_interfaces.action import BackAndForth
from rclpy.action import ActionClient
import rclpy.time
from random import randint
from threading import Thread
from time import sleep

SPEED = 0.1
FORWARD_DURATION = 2

class Tb3Leader(Node):

    def __init__(self):
        super().__init__('tb3_leader')
        self.declare_parameter('other_robot_id', 'tb3_1')
        self.cmd = Twist()
        self.rate = self.create_rate(10)

    def go_back_and_forth(self, speed, duration, repeat, robot_id = None):
        action_name = "back_and_forth" if robot_id == None else f"/{robot_id}/back_and_forth"
        self.action_client = ActionClient(self, BackAndForth, action_name)

        goal_msg = BackAndForth.Goal()
        goal_msg.speed = speed
        goal_msg.duration = duration
        goal_msg.repeat = repeat

        self.action_client.wait_for_server()
        self.action_client.send_goal(goal_msg)

def main(args=None):
    rclpy.init(args=args)

    tb3_leader = Tb3Leader()

    spin_thread = Thread(target=rclpy.spin, args=(tb3_leader,))
    spin_thread.start()

    sleep(1)
    rand = randint(1, 3)
    tb3_leader.get_logger().info(f"Nombre choisi: {rand}")
    tb3_leader.go_back_and_forth(SPEED, FORWARD_DURATION, rand)
    other_robot_id = tb3_leader.get_parameter('other_robot_id').get_parameter_value().string_value
    tb3_leader.get_logger().info(f"Envoi d'un message à: {other_robot_id}")
    tb3_leader.go_back_and_forth(SPEED, FORWARD_DURATION, rand, other_robot_id)

if __name__ == '__main__':
    main()