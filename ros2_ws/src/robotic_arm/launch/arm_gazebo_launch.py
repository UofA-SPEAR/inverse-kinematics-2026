import os
from launch import LaunchDescription
from launch.actions import LogInfo, DeclareLaunchArgument, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.conditions import IfCondition
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare
from launch.substitutions import Command, LaunchConfiguration, PathJoinSubstitution, PythonExpression
from launch_ros.parameter_descriptions import ParameterValue
from launch.actions import SetEnvironmentVariable

def generate_launch_description():
    # Define constants
    package_name = 'robotic_arm'
    
    # Relative file paths
    urdf_file =  'urdf/arm_assembly.urdf.xacro'
    config_file = 'config/ros_gz_bridge.yaml'
    world_file = 'worlds/empty_world.sdf'
    
    # Get package installation path
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

    declare_robot_name = DeclareLaunchArgument(
        name='robot_name',
        default_value='my_robot',
        description='Name of the robot in Gazebo'
    )

    declare_use_sim_time = DeclareLaunchArgument(
        name='use_sim_time',
        default_value='True',
        description='Use simulation clock if true'
    )

    declare_use_robot_state_pub = DeclareLaunchArgument(
        name='use_robot_state_pub',
        default_value='True',
        description='Whether to start the robot state publisher'
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
    robot_name = LaunchConfiguration('robot_name')
    use_sim_time = LaunchConfiguration('use_sim_time')
    use_robot_state_pub = LaunchConfiguration('use_robot_state_pub')

    robot_description_content = ParameterValue(
        Command(['xacro ', urdf_full_path]),
        value_type=str
    )

    robot_state_publisher = Node(
        condition=IfCondition(use_robot_state_pub),
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        output='screen',
        parameters=[{'use_sim_time': use_sim_time,
                     'robot_description': robot_description_content
                     }] 
    )

    # === Set Gazebo Resource Path === #


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

    # === TIME TO SPAWN THE DAMN ROBOT === #
    spawn_robot = Node(
        package='ros_gz_sim',
        executable='create',
        arguments=[
            '-name', robot_name,
            '-topic', 'robot_description',
            '-x', x,
            '-y', y,
            '-z', z,
            '-R', roll,
            '-P', pitch,
            '-Y', yaw   
        ],
        output='screen'
    )

    # === Build the Launch Description === #

    ld = LaunchDescription()

    """Commenting out because logging kept giving errors"""
    # Add info messages
    # ld.add_action(LogInfo(msg=['='*50]))
    # ld.add_action(LogInfo(msg=['Starting Gazebo...']))
    # ld.add_action(LogInfo(msg=['simulator: ',use_simulator]))
    # ld.add_action(LogInfo(msg=['x: ',x]))
    # ld.add_action(LogInfo(msg=['headless: ',headless]))
    # ld.add_action(LogInfo(msg=['world: ',world]))
    # ld.add_action(LogInfo(msg=['='*50]))

    # Add argument declarations
    ld.add_action(declare_use_simulator)
    ld.add_action(declare_headless)
    ld.add_action(declare_world)
    ld.add_action(declare_robot_name)
    ld.add_action(declare_use_sim_time)
    ld.add_action(declare_use_robot_state_pub)
    ld.add_action(declare_x)
    ld.add_action(declare_y)
    ld.add_action(declare_z)
    ld.add_action(declare_roll)
    ld.add_action(declare_pitch)
    ld.add_action(declare_yaw)
    
    # Add Gazebo nodes
    ld.add_action(start_gazebo_server)
    ld.add_action(start_gazebo_client)
    ld.add_action(robot_state_publisher)
    ld.add_action(spawn_robot)
    
    return ld
    
"""Commenting out logging for cleaner, more complete launch output"""

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