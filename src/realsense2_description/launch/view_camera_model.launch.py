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


PACKAGE_NAME = 'realsense2_description'
SUPPORTED_MODELS = ('d415', 'd435', 'r410', 'r430')


def _launch_camera_nodes(context):
    camera_model = LaunchConfiguration('camera_model').perform(context)
    if camera_model not in SUPPORTED_MODELS:
        supported = ', '.join(SUPPORTED_MODELS)
        raise RuntimeError(
            f"Unsupported camera_model '{camera_model}'. Choose one of: {supported}."
        )

    description_file = PathJoinSubstitution(
        [
            FindPackageShare(PACKAGE_NAME),
            'urdf',
            f'test_{camera_model}_camera.urdf.xacro',
        ]
    )
    rviz_config = PathJoinSubstitution(
        [FindPackageShare(PACKAGE_NAME), 'rviz', 'urdf.rviz']
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
                'camera_model',
                default_value='d435',
                description='Camera model: d415, d435, r410, or r430',
            ),
            DeclareLaunchArgument(
                'use_rviz',
                default_value='true',
                description='Start RViz2 to visualize the camera model',
            ),
            DeclareLaunchArgument(
                'use_sim_time',
                default_value='false',
                description='Use the simulation clock',
            ),
            OpaqueFunction(function=_launch_camera_nodes),
        ]
    )
