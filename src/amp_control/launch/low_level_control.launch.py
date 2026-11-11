from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument as LaunchArg
from launch.substitutions import LaunchConfiguration as LaunchConfig
from launch_ros.actions import Node


def generate_launch_description():
    return LaunchDescription(
        [
            LaunchArg(
                "namespace",
                default_value=["low_level_control"],
                description="Namespace for node",
            ),
            Node(
                package="control",
                executable="low_level_control_node.py",
                name="low_level_control_node",
                namespace=LaunchConfig("namespace"),
            ),
        ]
    )
