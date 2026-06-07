from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, LogInfo
from launch.launch_description_sources import PythonLaunchDescriptionSource
from ament_index_python.packages import get_package_share_directory
import os

def generate_launch_description():

    ov_msckf_share = get_package_share_directory('ov_msckf')

    subscribe_launch = os.path.join(
        ov_msckf_share,
        'launch',
        'subscribe.launch.py'
    )

    return LaunchDescription([

        LogInfo(msg="Starting OpenVINS for SJTU Drone"),

        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(subscribe_launch),
            launch_arguments={
                'config': 'sjtu_drone',
                'rviz_enable': 'true',
                'use_stereo': 'true',
                'max_cameras': '2',
            }.items()
        )
    ])