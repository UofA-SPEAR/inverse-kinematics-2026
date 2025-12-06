from launch import launch_description
from launch.actions import node
from launch_ros.substitutions import FindPackageShare
from launch.substitutions import Command, LaunchConfiguration, PathJoinSubstitution




def generate_launch_description():
 
    # Define filenames
    urdf_package = 'robotic_arm'
    urdf_filename = 'arm_assembly.urdf'
    # We don't have an rviz file yet so the line below is not useful"
    rviz_config_filename = '.......'

    pkg_share_description = FindPackageShare(urdf_package)
    pkg_file_path_merge = PathJoinSubstitution(pkg_share_description, 'urdf', urdf_filename)

