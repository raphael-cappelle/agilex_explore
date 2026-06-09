import rclpy
import rclpy.context
import rclpy.duration
from rclpy.node import Node
from geometry_msgs.msg import Twist
from std_msgs.msg import String
import rclpy.time
import threading
from enum import Enum

class Behavior(Enum):
    BACK_AND_FORTH = 0
    CIRCLE = 1
    STOP = 2

SPEED = 0.2

class Tb3Movement(Node):

    def __init__(self):
        super().__init__('tb3_movement')
        self.publisher = self.create_publisher(Twist, 'cmd_vel', 10)
        self.subscriber = self.create_subscription(String, '/barcode', self.subscription_callback, 10)
        self.rate = self.create_rate(10, self.get_clock())
        self.behavior = Behavior.STOP

    def subscription_callback(self, msg):
        data = msg.data
        if data == "back and forth":
            self.time = self.get_clock().now()
            self.direction = 0.2
            self.behavior = Behavior.BACK_AND_FORTH
        elif data == "circle":
            self.behavior = Behavior.CIRCLE
        elif data == "stop":
            self.behavior = Behavior.STOP

    def make_circle(self):
        cmd = Twist()
        cmd.linear.x = SPEED
        cmd.angular.z = 1.0
        self.publisher.publish(cmd)

    def move_linear_x(self):
        cmd = Twist()
        cmd.linear.x = self.direction
        if self.get_clock().now() - self.time < rclpy.duration.Duration(seconds=2):
            self.publisher.publish(cmd)
        else:
            self.time = self.get_clock().now()
            self.direction = -self.direction

def main(args=None):
    rclpy.init(args=args)

    node = Tb3Movement()

    thread = threading.Thread(target=rclpy.spin, args=(node, ), daemon=True)
    thread.start()

    while rclpy.ok():
        if node.behavior == Behavior.CIRCLE:
            node.make_circle()
        elif node.behavior == Behavior.BACK_AND_FORTH:
            node.move_linear_x()
        else:
            node.publisher.publish(Twist())
        node.rate.sleep()

if __name__ == '__main__':
    main()
