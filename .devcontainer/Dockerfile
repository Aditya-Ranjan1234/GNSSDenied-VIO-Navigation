FROM osrf/ros:humble-desktop-full

# Avoid interactive prompts
ENV DEBIAN_FRONTEND=noninteractive
ENV NVIDIA_VISIBLE_DEVICES=all
ENV NVIDIA_DRIVER_CAPABILITIES=all

# GPU / display env
ENV __NV_PRIME_RENDER_OFFLOAD=1
ENV __GLX_VENDOR_LIBRARY_NAME=nvidia

# Install essentials + Gazebo + dev tools
RUN apt-get update && apt-get install -y \
    ros-humble-gazebo-ros-pkgs \
    ros-humble-gazebo-ros2-control \
    ros-humble-rviz2 \
    ros-humble-slam-toolbox \
    ros-humble-nav2-bringup \
    ros-humble-vision-opencv \
    ros-humble-image-transport \
    ros-humble-cv-bridge \
    ros-humble-tf2-tools \
    python3-pip \
    python3-colcon-common-extensions \
    python3-rosdep \
    git wget curl vim \
    libgl1-mesa-glx \
    libgl1-mesa-dri \
    mesa-utils \
    && rm -rf /var/lib/apt/lists/*

# For VIO/SLAM — OpenCV extras
RUN pip3 install opencv-python numpy scipy

# Source ROS2 on every shell
RUN echo "source /opt/ros/humble/setup.bash" >> /root/.bashrc
RUN echo "source /opt/ros/humble/setup.bash" >> /etc/bash.bashrc

# rosdep init
RUN rosdep init || true && rosdep update

WORKDIR /workspaces/DroneVio