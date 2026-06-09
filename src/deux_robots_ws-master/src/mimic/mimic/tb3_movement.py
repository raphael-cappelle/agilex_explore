import rclpy
import rclpy.context
import rclpy.duration
from rclpy.node import Node
from geometry_msgs.msg import Twist
from mimic_interfaces.action import BackAndForth
from rclpy.executors import MultiThreadedExecutor
from rclpy.action import ActionServer
import rclpy.time

class Tb3Movement(Node):

    def __init__(self):
        super().__init__('tb3_movement')
        self.cmd = Twist()
        self.publisher = self.create_publisher(Twist, 'cmd_vel', 10)
        self.rate = self.create_rate(10, self.get_clock())
        self.action_server = ActionServer(
            self,
            BackAndForth,
            'back_and_forth',
            self.go_back_and_forth
        )

    def go_back_and_forth(self, goal_handle):
        repeat = goal_handle.request.repeat
        speed = goal_handle.request.speed
        duration = goal_handle.request.duration

        feedback_msg = BackAndForth.Feedback()
        self.get_logger().info(f"{repeat} aller-retour programmé")
        for i in range(1, repeat+1):
            self.move_linear_x(speed, duration)
            self.move_linear_x(-speed, duration)
            feedback_msg.nb_iteration = i
            self.get_logger().info(f"{i}/{repeat} aller-retour terminé")
            
            goal_handle.publish_feedback(feedback_msg)
        self.move_linear_x(0.0, 0.5) # on met le robot à l'arrêt pour qu'il ne recule plus
        self.get_logger().info(f"Aller-retour terminé")
        goal_handle.succeed()
        return BackAndForth.Result()

    def move_linear_x(self, speed, duration):
        self.cmd.linear.x = speed
        self.time = self.get_clock().now()
        while self.get_clock().now() - self.time < rclpy.duration.Duration(seconds=duration):
            self.publisher.publish(self.cmd)
            self.rate.sleep()

def main(args=None):
    rclpy.init(args=args)

    executor = MultiThreadedExecutor()
    tb3_movement = Tb3Movement()

    rclpy.spin(tb3_movement, executor=executor)

if __name__ == '__main__':
    main()