from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, OpaqueFunction
from launch.conditions import IfCondition
from launch.substitutions import (
    Command,
    FindExecutable,
    LaunchConfiguration,
    PathJoinSubstitution,
)
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue
from launch_ros.substitutions import FindPackageShare


PACKAGE_NAME = 'ur_description'
SUPPORTED_MODELS = ('ur3', 'ur5', 'ur10')


def _launch_nodes(context):
    model = LaunchConfiguration('model').perform(context).strip().lower()
    if model not in SUPPORTED_MODELS:
        supported = ', '.join(SUPPORTED_MODELS)
        raise RuntimeError(f"Unsupported model '{model}'. Choose one of: {supported}.")

    limited = LaunchConfiguration('limited').perform(context).strip().lower()
    if limited not in ('true', 'false'):
        raise RuntimeError("The 'limited' argument must be 'true' or 'false'.")

    suffix = '_joint_limited_robot' if limited == 'true' else '_robot'
    description_file = PathJoinSubstitution(
        [FindPackageShare(PACKAGE_NAME), 'urdf', f'{model}{suffix}.urdf.xacro']
    )
    rviz_config = PathJoinSubstitution(
        [FindPackageShare(PACKAGE_NAME), 'rviz', 'ur_description.rviz']
    )
    robot_description = ParameterValue(
        Command([FindExecutable(name='xacro'), ' ', description_file]),
        value_type=str,
    )
    use_sim_time = LaunchConfiguration('use_sim_time')

    return [
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


def generate_launch_description():
    return LaunchDescription(
        [
            DeclareLaunchArgument(
                'model',
                default_value='ur5',
                description='Universal Robot model: ur3, ur5, or ur10',
            ),
            DeclareLaunchArgument(
                'limited',
                default_value='true',
                description='Use the joint-limited robot description',
            ),
            DeclareLaunchArgument(
                'use_rviz',
                default_value='true',
                description='Start RViz2',
            ),
            DeclareLaunchArgument(
                'use_sim_time',
                default_value='false',
                description='Use the simulation clock',
            ),
            OpaqueFunction(function=_launch_nodes),
        ]
    )
