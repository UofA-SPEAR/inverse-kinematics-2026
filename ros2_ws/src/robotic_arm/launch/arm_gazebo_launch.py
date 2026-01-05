import os
from launch import LaunchDescription
from launch.actions import LogInfo, DeclareLaunchArgument, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.conditions import IfCondition
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare
from launch.substitutions import Command, LaunchConfiguration, PathJoinSubstitution, PythonExpression

def generate_launch_description():
    # Define package name
    package_name = 'robotic_arm'
    
    # Relative file paths
    urdf_file =  'urdf/arm_assembly.urdf'
    config_file = 'config/ros_gz_bridge.yaml'
    world_file = 'worlds/empty_world.sdf'
    
    # PART 2: Get package installation path
    pkg_share = FindPackageShare(package=package_name).find(package_name)
    pkg_ros_gz_sim = FindPackageShare(package='ros_gz_sim').find('ros_gz_sim')

    # Build full file paths
    urdf_full_path = os.path.join(pkg_share, urdf_file)
    config_full_path = os.path.join(pkg_share, config_file)
    world_full_path = os.path.join(pkg_share, world_file)
    gazebo_launch_file = os.path.join(pkg_ros_gz_sim, 'launch', 'gz_sim.launch.py')
    
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

    declare_world = DeclareLaunchArgument(
        name='world',
        default_value= world_full_path,
        description='Full path to world file to load'
    )

    declare_use_simulator = DeclareLaunchArgument(
        name='use_simulator',
        default_value='True',
        description='Whether to start Gazebo simulator'
    )

    declare_headless = DeclareLaunchArgument(
        name='headless',
        default_value='False',
        description='Run without GUI if true'
    )

    # Obtain the values

    x = LaunchConfiguration('x')    
    y = LaunchConfiguration('y')    
    z = LaunchConfiguration('z')
    roll = LaunchConfiguration('roll')
    pitch = LaunchConfiguration('pitch')
    yaw = LaunchConfiguration('yaw')
    world = LaunchConfiguration('world')
    use_simulator = LaunchConfiguration('use_simulator')
    headless = LaunchConfiguration('headless')

    # === Start Gazebo Server === #
    start_gazebo_server = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(gazebo_launch_file),
        launch_arguments={
            'gz_args': ['-r -s -v4', world],
            #'on_exit_shutdown': 'true'
        }.items()
    )

    # === Start Gazebo Client (GUI ONLY) === #
    start_gazebo_client = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(gazebo_launch_file),
        launch_arguments={
            'gz_args': '-g -v4'
        }.items(),
        condition=IfCondition(
            PythonExpression([use_simulator, ' and not ', headless])
        )
    )

    # === Build the Launch Description === #

    ld = LaunchDescription()

    # Add declarations
    ld.add_action(declare_use_simulator)
    ld.add_action(declare_headless)
    ld.add_action(declare_world)
    
    # Add info messages
    ld.add_action(LogInfo(msg=['='*50]))
    ld.add_action(LogInfo(msg=['Starting Gazebo...']))
    ld.add_action(LogInfo(msg=['Simulator: ', use_simulator]))
    ld.add_action(LogInfo(msg=['Headless: ', headless]))
    ld.add_action(LogInfo(msg=['World: ', world]))
    ld.add_action(LogInfo(msg=['='*50]))
    
    # Add Gazebo nodes
    ld.add_action(start_gazebo_server)
    ld.add_action(start_gazebo_client)
    
    return ld



"""Commenting out logging for cleaner launch output"""

    # return LaunchDescription([
    #     declare_x,
    #     declare_y,
    #     declare_z,
    #     declare_roll,
    #     declare_pitch,
    #     declare_yaw,
    #     declare_world,
        
    #     # Print the spawn values

    #     LogInfo(msg=['Robot spawn position:']),
    #     LogInfo(msg=[' X = ', x, ' meters']),
    #     LogInfo(msg=[' Y = ', y, ' meters']),
    #     LogInfo(msg=[' Z = ', z, ' meters']),
    #     LogInfo(msg=[' Roll = ', roll, ' radians']),
    #     LogInfo(msg=[' Pitch = ', pitch, ' radians']),
    #     LogInfo(msg=[' Yaw = ', yaw, ' radians']),
    #     LogInfo(msg=['='*50]),
    #     LogInfo(msg=['Package_path: ', pkg_share]),
    #     LogInfo(msg=['='*50]),
    #     LogInfo(msg=['URDF path: ', urdf_full_path]),
    #     LogInfo(msg=['Config path: ', config_full_path]),
    #     LogInfo(msg=['World path: ', world_full_path]),