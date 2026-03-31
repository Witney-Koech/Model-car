import os
from launch import LaunchDescription
from launch.substitutions import LaunchConfiguration, Command
from launch_ros.parameter_descriptions import ParameterValue
from launch.actions import DeclareLaunchArgument
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory


def generate_launch_description():

    # Get package path
    pkg_share = get_package_share_directory('my_rover')
    urdf_file = os.path.join(pkg_share, 'urdf', 'ref.urdf')

    # Read URDF using XACRO
    robot_description = ParameterValue(
        Command(['xacro ', urdf_file]),
        value_type=str
    )

    use_sim_time = LaunchConfiguration('use_sim_time')

    declare_use_sim_time_cmd = DeclareLaunchArgument(
        'use_sim_time',
        default_value='false',
        description='Use simulation clock if true'
    )

    # Robot State Publisher node
    robot_state_publisher_node = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        parameters=[
            {
                'use_sim_time': use_sim_time,
                'robot_description': robot_description
            }
        ],
        output='screen'
    )

    return LaunchDescription([
        declare_use_sim_time_cmd,
        robot_state_publisher_node
    ])