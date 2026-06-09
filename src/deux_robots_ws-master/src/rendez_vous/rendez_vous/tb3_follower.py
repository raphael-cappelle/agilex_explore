import rclpy
import rclpy.context
import rclpy.duration
from rclpy.node import Node
from geometry_msgs.msg import Twist
from geometry_msgs.msg import Point, Quaternion
import rclpy.time
from rendez_vous import euler_from_quaternion
from rendez_vous_interfaces.action import GoToPoint
from geometry_msgs.msg import PoseStamped
from rclpy.executors import MultiThreadedExecutor
from rclpy.action import ActionServer
from math import pow, atan2, sqrt
from angles import shortest_angular_distance

SPEED = 0.2

class Tb3Follower(Node):

    def __init__(self):
        super().__init__('tb3_follower')
        
        self.robot_id = self.get_namespace().split("/")[1]

        self.declare_parameter('other_robot_id', 'tb3_2')
        self.other_robot_id = self.get_parameter('other_robot_id').get_parameter_value().string_value

        self.publisher = self.create_publisher(Twist, 'cmd_vel', 10)
        self.position = Point()
        self.orientation = Quaternion()
        self.goal_pose = None
        #self.odom_subscriber = self.create_subscription(Odometry, 'odom', self.odom_callback, 10)
        self.my_pos_subscriber = self.create_subscription(PoseStamped, f"/vrpn_mocap/{self.robot_id}/pose", self.my_pos_callback, 50)
        self.other_pos_subscriber = self.create_subscription(PoseStamped, f"/vrpn_mocap/{self.other_robot_id}/pose", self.other_pos_callback, 50)
        self.rate = self.create_rate(10, clock=self.get_clock())
        self.action_server = ActionServer(
            self,
            GoToPoint,
            'go_to_point',
            self.go_to
        )

    def my_pos_callback(self, msg):
        self.position = msg.pose.position

        old_y = self.position.y
        self.position.x = -self.position.x
        self.position.y = self.position.z
        self.position.z = old_y

        self.orientation = msg.pose.orientation
        old_y = self.orientation.y
        self.orientation.y = self.orientation.z
        self.orientation.z = old_y

    def other_pos_callback(self, msg):
        self.goal_pose = msg.pose.position

        old_y = self.goal_pose.y
        self.goal_pose.x = -self.goal_pose.x
        self.goal_pose.y = self.goal_pose.z
        self.goal_pose.z = old_y

    def odom_callback(self, msg):
        #self.position = msg.pose.pose.position
        #self.orientation = msg.pose.pose.orientation
        return

    def euclidean_distance(self):
        return sqrt(pow((self.goal_pose.x - self.position.x), 2) +
                    pow((self.goal_pose.y - self.position.y), 2))
 
    def steering_angle(self):
        return atan2(self.goal_pose.y - self.position.y, self.goal_pose.x - self.position.x)

    def angular_vel(self, constant=1):
        (_, _, yaw) = euler_from_quaternion(self.orientation)
        goal_angle = self.steering_angle()
        return constant * shortest_angular_distance(yaw, goal_angle)

    def go_to(self, goal_handle):
        if self.goal_pose is None:
            goal_handle.abort()
            return GoToPoint.Result()
        distance_tolerance = goal_handle.request.distance_tolerance
        feedback_msg = GoToPoint.Feedback()
        while self.euclidean_distance() >= distance_tolerance:
            msg = Twist()
            msg.linear.x = SPEED
            msg.angular.z = self.angular_vel()
            self.publisher.publish(msg)
            self.rate.sleep()

            feedback_msg.current = self.position
            goal_handle.publish_feedback(feedback_msg)

        self.publisher.publish(Twist())
        self.rate.sleep()
        
        result = GoToPoint.Result()
        result.final = self.position
        goal_handle.succeed()
        return result

def main(args=None):
    rclpy.init(args=args)

    executor = MultiThreadedExecutor()
    node = Tb3Follower()

    rclpy.spin(node, executor=executor)

if __name__ == '__main__':
    main()