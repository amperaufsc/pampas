from launch import LaunchDescription
from launch.actions import (
    DeclareLaunchArgument as LaunchArg
)
from launch.substitutions import LaunchConfiguration as LaunchConfig
from launch_ros.actions import Node


def generate_launch_description():

    return LaunchDescription([
        LaunchArg('pampas_params_path', default_value=['pampas_params_path'], description='Path for pampas yaml parameters file'),
        LaunchArg('namespace',default_value=[''],description='namespace for Node'),
        LaunchArg('odom',default_value=['odom'],description='odometry msg publisher'),
        LaunchArg('track',default_value=['track'],description='pose msg subscriber'),
        LaunchArg('track_pub',default_value=['track_pub'],description='pose msg subscriber'),


    Node(
        package='mapper',
        executable='mapper_node_life.py',
        name='mapper_node',
        namespace=LaunchConfig('namespace'),
        output='screen',
        remappings=[
            ('track', LaunchConfig('track')),
            ('odom', LaunchConfig('odom')),
            ('track_pub', LaunchConfig('track_pub')),],
        parameters=[LaunchConfig('pampas_params_path')]
        )
    ])