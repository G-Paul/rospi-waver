from launch import LaunchDescription
from launch_ros.actions import Node
import os

def generate_launch_description():
    urdf_file = os.path.join(
        os.getenv('HOME'),
        'ros2_ws', 'src', 'my_robot_description', 'urdf', 'my_robot.urdf'
    )
    
    return LaunchDescription([
        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            name='robot_state_publisher',
            output='screen',
            parameters=[{'use_sim_time': False}],
            arguments=[urdf_file],
        ),
        Node(
            package='rviz2',
            executable='rviz2',
            name='rviz2',
            output='screen',
            arguments=['-d', '$(find-pkg-share my_robot_description)/rviz/my_robot.rviz'],
        )
    ])