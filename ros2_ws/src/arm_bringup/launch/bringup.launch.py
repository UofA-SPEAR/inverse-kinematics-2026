import os
from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from moveit_configs_utils import MoveItConfigsBuilder
from ament_index_python.packages import get_package_share_directory
from launch_ros.parameter_descriptions import ParameterFile


def generate_launch_description():
    moveit_config = (
        MoveItConfigsBuilder("kipp", package_name="robot_moveit_config")
        .robot_description_kinematics()
        .to_moveit_configs()
    )

    servo_params_path = os.path.join(
        get_package_share_directory("robot_moveit_config"),
        "config", "servo_params.yaml"
    )

    robot_state_publisher = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        output="screen",
        parameters=[moveit_config.robot_description],
    )

    ros2_control_node = Node(
        package="controller_manager",
        executable="ros2_control_node",
        output="screen",
        parameters=[
            moveit_config.robot_description,
            os.path.join(
                get_package_share_directory("robot_moveit_config"),
                "config", "ros2_controllers.yaml"
            ),
        ],
    )

    joint_state_broadcaster_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["joint_state_broadcaster"],
    )

    arm_controller_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["arm_controller"],
    )

    joy_node = Node(
        package="joy",
        executable="joy_node",
        name="joy_node",
    )

    import yaml

    # In generate_launch_description():
    with open(servo_params_path, 'r') as f:
        servo_yaml = yaml.safe_load(f)

    # Extract just the ros__parameters dict, already nested under moveit_servo
    servo_params = servo_yaml['servo_node']['ros__parameters']

    servo_node = Node(
        package="moveit_servo",
        executable="servo_node_main",
        name="servo_node",
        output="screen",
        parameters=[
            moveit_config.robot_description,
            moveit_config.robot_description_semantic,
            moveit_config.robot_description_kinematics,
            servo_params,
        ],
    )

    move_group = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(
                get_package_share_directory("robot_moveit_config"),
                "launch", "move_group.launch.py"
            )
        )
    )

    rviz_config = os.path.join(
        get_package_share_directory("arm_bringup"),
        "config", "arm_moveit.rviz"
    )

    rviz_node = Node(
        package="rviz2",
        executable="rviz2",
        output="screen",
        arguments=["-d", rviz_config],
        parameters=[
            moveit_config.robot_description,
            moveit_config.robot_description_semantic,
            moveit_config.robot_description_kinematics,
        ],
    )

    return LaunchDescription([
        robot_state_publisher,
        ros2_control_node,
        joint_state_broadcaster_spawner,
        arm_controller_spawner,
        joy_node,
        servo_node,
        move_group,
        rviz_node,
    ])