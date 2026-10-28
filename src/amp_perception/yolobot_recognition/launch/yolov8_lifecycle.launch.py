from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import DeclareLaunchArgument as LaunchArg
from launch.substitutions import LaunchConfiguration
import os
from ament_index_python.packages import get_package_share_directory
from pathlib import Path

def generate_launch_description():
    from_home_config_path = str(Path.home() / "pampas" / "config" / 'system_params.yaml')

    return LaunchDescription([
        LaunchArg('system_config_path', default_value=[from_home_config_path], description='System parameter yaml path'), 
        LaunchArg('namespace', default_value=['perception'], description='Namespace for node'),
        LaunchArg('image',default_value=['/oak/left/image_raw'],description='img topic'),
        LaunchArg('inference',default_value=['inference'],description='bounding box coordenates on image'),
        LaunchArg('inferenceimg',default_value=['inferenceimg'],description='img with boundingbox'),
        Node(
            package='yolobot_recognition',
            executable='yolov8_node_lifecycle.py',
            name='yolo_node',
            namespace=LaunchConfiguration('namespace'),
            output='screen',
            remappings=[
                ('image',LaunchConfiguration('image')), 
                ('inference',LaunchConfiguration('inference')),
                ('inferenceimg',LaunchConfiguration('inferenceimg'))
                ],
            parameters=[
                LaunchConfiguration('system_config_path')
            ]
    )
    ])
