from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import DeclareLaunchArgument as LaunchArg
from launch.substitutions import LaunchConfiguration

def generate_launch_description():

    return LaunchDescription([
        LaunchArg('pampas_params_path', default_value=['pampas_params_path'], description='Path of Pampas yaml parameters file'), 
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
                LaunchConfiguration('pampas_params_path')
            ]
    )
    ])
