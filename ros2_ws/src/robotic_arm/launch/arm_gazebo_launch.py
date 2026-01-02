import os
from launch import LaunchDescription
from launch.actions import LogInfo, DeclareLaunchArgument
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare
from launch.substitutions import Command, LaunchConfiguration, PathJoinSubstitution

def generate_launch_description():
    # Define package name
    package_name = 'robotic_arm'
    
    # Relative file paths
    urdf_file =  'urdf/arm_assembly.urdf'
    config_file = 'config/ros_gz_bridge.yaml'
    
    # PART 2: Get package installation path
    pkg_share = FindPackageShare(package=package_name).find(package_name)

    # Build full file paths
    urdf_full_path = os.path.join(pkg_share, urdf_file)
    config_full_path = os.path.join(pkg_share, config_file)
    
    # === Position Arguments === #
    declare_x = DeclareLaunchArgument(
        name = 'x',
        default_value = '0.0',
        description = 'X position of arm in meters'
    )

    declare_y = DeclareLaunchArgument(
        name = 'y',
        default_value = '0.0',
        description = 'Y position of arm in meters'
    )

    declare_z = DeclareLaunchArgument(
        name = 'z',
        default_value = '0.5',
        description = 'Z position of arm in meters'
    )

    # === Orientation Arguments === #
    declare_roll = DeclareLaunchArgument(
        name = 'roll',
        default_value = '0.0',
        description = 'Roll orientation of arm in radians (rotation around X axis)'
    )

    declare_pitch = DeclareLaunchArgument(
        name = 'pitch',
        default_value = '0.0',
        description = 'Pitch orientation of arm in radians (rotation around Y axis)'
    )

    declare_yaw = DeclareLaunchArgument(
        name = 'yaw',
        default_value = '0.0',
        description = 'Yaw orientation of arm in radians (rotation around Z axis)'
    )

    # Obtain the values

    x = LaunchConfiguration('x')    
    y = LaunchConfiguration('y')    
    z = LaunchConfiguration('z')
    roll = LaunchConfiguration('roll')
    pitch = LaunchConfiguration('pitch')
    yaw = LaunchConfiguration('yaw')

    return LaunchDescription([
        declare_x,
        declare_y,
        declare_z,
        declare_roll,
        declare_pitch,
        declare_yaw,
        
        # Print the spawn values

        LogInfo(msg=['Robot spawn position:']),
        LogInfo(msg=[' X = ', x, ' meters']),
        LogInfo(msg=[' Y = ', y, ' meters']),
        LogInfo(msg=[' Z = ', z, ' meters']),
        LogInfo(msg=[' Roll = ', roll, ' radians']),
        LogInfo(msg=[' Pitch = ', pitch, ' radians']),
        LogInfo(msg=[' Yaw = ', yaw, ' radians']),
        LogInfo(msg=['='*50]),
        LogInfo(msg=['Package_path: ', pkg_share]),
        LogInfo(msg=['='*50]),
        LogInfo(msg=['URDF path: ', urdf_full_path]),
        LogInfo(msg=['Config path: ', config_full_path]),
    ])