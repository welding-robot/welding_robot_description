from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.conditions import IfCondition
from launch.substitutions import Command, FindExecutable, LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
    description_file = PathJoinSubstitution(
        [FindPackageShare('weldingscene_description'), 'urdf', 'weldingrobot.urdf.xacro']
    )
    rviz_config = PathJoinSubstitution(
        [FindPackageShare('weldingscene_description'), 'rviz', 'welding_support.rviz']
    )
    robot_description = ParameterValue(
        Command([FindExecutable(name='xacro'), ' ', description_file]), value_type=str
    )
    use_sim_time = LaunchConfiguration('use_sim_time')

    return LaunchDescription(
        [
            DeclareLaunchArgument(
                'use_sim_time', default_value='false', description='Use simulation clock'
            ),
            DeclareLaunchArgument(
                'use_rviz', default_value='true', description='Start RViz2'
            ),
            Node(
                package='robot_state_publisher',
                executable='robot_state_publisher',
                name='robot_state_publisher',
                output='screen',
                parameters=[
                    {'robot_description': robot_description},
                    {'use_sim_time': use_sim_time},
                ],
            ),
            Node(
                package='joint_state_publisher_gui',
                executable='joint_state_publisher_gui',
                name='joint_state_publisher_gui',
                output='screen',
                parameters=[{'use_sim_time': use_sim_time}],
            ),
            Node(
                package='rviz2',
                executable='rviz2',
                name='rviz2',
                output='screen',
                arguments=['-d', rviz_config],
                parameters=[{'use_sim_time': use_sim_time}],
                condition=IfCondition(LaunchConfiguration('use_rviz')),
            ),
        ]
    )
