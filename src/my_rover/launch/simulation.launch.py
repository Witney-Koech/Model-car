import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, TimerAction
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node


def generate_launch_description():

    package_name = 'my_rover'

    # World file path
    world_file = os.path.join(
        get_package_share_directory(package_name),
        'world',
        'world.sdf'
    )

    # Controller YAML path
    controller_yaml = os.path.join(
        get_package_share_directory(package_name),
        'config',
        'controller.yaml'
    )

    # Robot State Publisher launch
    rsp = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(
                get_package_share_directory(package_name),
                'launch',
                'rsp.launch.py'
            )
        ),
        launch_arguments={'use_sim_time': 'true'}.items()
    )

    # Gazebo launch
    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(
                get_package_share_directory('ros_gz_sim'),
                'launch',
                'gz_sim.launch.py'
            )
        ),
        launch_arguments={'gz_args': f'-r -v 4 {world_file}'}.items()
    )

    # Spawn robot in Gazebo
    spawn_entity = Node(
        package='ros_gz_sim',
        executable='create',
        arguments=[
            '-topic', 'robot_description',
            '-name', 'my_rover',
            '-z', '0.3'
        ],
        output='screen'
    )

    # Bridge node (sensors)
    bridge = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        arguments=[
            '/camera/image_raw@sensor_msgs/msg/Image@gz.msgs.Image',
            '/scan@sensor_msgs/msg/LaserScan@gz.msgs.LaserScan',
            '/imu@sensor_msgs/msg/Imu@gz.msgs.IMU',
        ],
        output='screen'
    )

    # Controller spawners
    joint_state_broadcaster_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["joint_state_broadcaster"],
        output="screen",
    )

    diff_drive_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["diff_cont"],
        output="screen",
    )

    #Delay controllers (VERY IMPORTANT)
    delayed_joint_state = TimerAction(
        period=3.0,
        actions=[joint_state_broadcaster_spawner],
    )

    delayed_diff_drive = TimerAction(
        period=5.0,
        actions=[diff_drive_spawner],
    )

    return LaunchDescription([
        rsp,
        gazebo,
        spawn_entity,
        bridge,

        # Controllers (after spawn)
        delayed_joint_state,
        delayed_diff_drive,
    ])