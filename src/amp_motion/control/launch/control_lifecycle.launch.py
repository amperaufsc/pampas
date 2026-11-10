from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument as LaunchArg
from launch.substitutions import LaunchConfiguration 
from launch_ros.actions import LifecycleNode


def generate_launch_description():
    return LaunchDescription([
        LaunchArg('pampas_params_path', default_value='pampas_params_path', description='Path of Pampas yaml parameters file'), 
        LaunchArg('namespace',default_value='',description='Namespace for node'),
        LaunchArg('path',default_value='/path_concatenated',description='Path message topic'),
        LaunchArg('odom',default_value='/orbslam/odom',description='Odom message topic'),
        LaunchArg('control',default_value='control',description='Control message topic'),
        LifecycleNode(
            package='control',
            executable='control_node_life.py',
            name='control_node',
            namespace=LaunchConfiguration('namespace'),
            output='screen',
            remappings=[
                ('path', LaunchConfiguration('path')),
                ('odom', LaunchConfiguration('odom')),
                ('control', LaunchConfiguration('control'))
            ],
            parameters=[
              LaunchConfiguration('pampas_params_path')  
            ],
        )
    ])