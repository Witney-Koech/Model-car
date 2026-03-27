from launch import LaunchDescription
from launch.actions import ExecuteProcess, IncludeLaunchDescription, DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory
import os

def generate_launch_description():

    package_name = 'my_rover'
    pkg_path = get_package_share_directory(package_name)


    default_world = os.path.join(pkg_path, 'world', 'world.sdf')

    
    world_arg = DeclareLaunchArgument(
        'world',
        default_value=default_world,
        description='Path to world file'
    )

    world = LaunchConfiguration('world')

    # Include RSP
    rsp_launch = os.path.join(pkg_path, 'launch', 'rsp.launch.py')

    return LaunchDescription([

        world_arg,

        # Start Gazebo with world
        ExecuteProcess(
            cmd=['gz', 'sim', '-r', world],
            output='screen'
        ),

        # Include robot_state_publisher
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(rsp_launch)
        ),

        # Spawn robot
        Node(
            package='ros_gz_sim',
            executable='create',
            arguments=[
                '-name', 'my_rover',
                '-topic', 'robot_description'
            ],
            output='screen'
        ),
    ])