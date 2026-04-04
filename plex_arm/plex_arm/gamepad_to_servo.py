import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Joy
from geometry_msgs.msg import TwistStamped
from control_msgs.msg import JointJog

class gamepad_to_servo(Node):
    def __init__(self):
        super().__init__('gamepad_to_servo')
        self.joy_sub = self.create_subscription(Joy, '/joy', self.joy_cb, 10)
        self.twist_pub = self.create_publisher(TwistStamped, '/servo_node/delta_twist_cmds', 10)
        self.joint_pub = self.create_publisher(JointJog, '/servo_node/delta_joint_cmds', 10)

    def joy_cb(self, msg):
        # Toggle mode with a button press, e.g. Y button (index 3 on Xbox)
        # Toggles between direct EE manipulation and single joint manipulation
        if msg.buttons[3]:  # <---------------------------  May or may not be mapped to [3]. YOu should check this
            self.joint_mode = not self.joint_mode
            mode = "joint" if self.joint_mode else "cartesian"
            self.get_logger().info(f'Switched to {mode} mode')

        if self.joint_mode:
            self.publish_joint_cmds(msg)
        else:
            self.publish_twist_cmds(msg)

# We use this to move each joint individually

    def publish_joint_cmds(self, msg):
        joint_cmd = JointJog()
        joint_cmd.header.stamp = self.get_clock().now().to_msg()
        joint_cmd.header.frame_id = 'base_link'

        # Map each stick axis to a joint
        joint_cmd.joint_names = ['Amanda', 'Sosuke', 'Nathan', 'Henry', 'Indy']
        joint_cmd.velocities = [
            msg.axes[0] * 0.5,   # left stick left/right → Amanda
            msg.axes[1] * 0.5,   # left stick up/down  → Sosuke
            msg.axes[4] * 0.5,   # right stick up/down → Nathan
            msg.axes[3] * 0.5,   # right stick left/right → Henry
            msg.axes[2] * 0.5,   # left trigger → Indy
        ]

        self.joint_pub.publish(joint_cmd)

# If we want to move the end effector to a point in space, we use this

    def publish_twist_cmds(self, msg):
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