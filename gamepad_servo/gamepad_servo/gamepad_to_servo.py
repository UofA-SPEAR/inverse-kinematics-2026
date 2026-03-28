import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Joy
from geometry_msgs.msg import TwistStamped

class gamepad_to_servo(Node):
    def __init__(self):
        super().__init__('gamepad_to_servo')
        self.joy_sub = self.create_subscription(Joy, '/joy', self.joy_cb, 10)
        self.twist_pub = self.create_publisher(TwistStamped, '/servo_node/delta_twist_cmds', 10)

    def joy_cb(self, msg):
        twist = TwistStamped()
        twist.header.stamp = self.get_clock().now().to_msg()
        twist.header.frame_id = "base_link"

        twist.twist.linear.x = msg.axes[0] # left-right
        twist.twist.linear.y = msg.axes[1] # up-down
        twist.twist.linear.z = msg.axes[4] #forward-backward
        twist.twist.angular.z = msg.axes[2] #rotation

        self.twist_pub.publish(twist)

def main():
    rclpy.init()
    rclpy.spin(gamepad_to_servo())