import os
from launch import LaunchDescription
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue
from launch.substitutions import Command
from launch_ros.substitutions import FindPackageShare

pkg_share = FindPackageShare(package='arm_description').find('arm_description')
urdf_file = os.path.join(pkg_share, 'urdf', 'robot.urdf.xacro')
controller_config = os.path.join(pkg_share, 'config', 'ros_controllers.yaml')

def generate_launch_description():
    robot_description = ParameterValue(
        Command(['xacro ', '/inverse-kinematics-2026/ros2_ws/src/arm_description/urdf/robot.urdf.xacro']),
        value_type=str
    )

    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        parameters=[{'robot_description': robot_description}]
    )

    controller_manager = Node(
        package='controller_manager',
        executable='ros2_control_node',
        parameters=[
            {'robot_description': robot_description},
            '~/inverse-kinematics-2026/src/arm_bringup/config//ros2_controllers.yaml'
        ]
    )

    return LaunchDescription([robot_state_publisher, controller_manager])