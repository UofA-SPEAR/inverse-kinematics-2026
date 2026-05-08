from launch import LaunchDescription
from launch_ros.actions import Node
from moveit_configs_utils import MoveItConfigsBuilder
from ament_index_python.packages import get_package_share_directory
import os

def generate_launch_description():
    urdf_file = os.path.join(
        get_package_share_directory('plex_arm_urdf'),
        'urdf', 'plex_arm_urdf.urdf'
    )
    with open(urdf_file, 'r') as f:
        robot_description = f.read()
        
    # moveit_config = (
    #     MoveItConfigsBuilder("plex_arm_urdf", package_name="plex_arm_urdf")
    #     .to_moveit_configs()
    # )

    robot_state_publisher = Node(
                package = robot_state_publisher,
                executable = robot_state_publisher,
                name = robot_state_publisher,
                parameters = [{
                    'use_sim_time': True,
                    'robot_description': [robot_description]
                }],
                output = 'screen',
            )

    return LaunchDescription([
        robot_state_publisher,
    ])