# Autonomous Navigator for GNSS-Denied Environments

## Table of Contents
- [Introduction](#introduction)
- [Problem Statement](#problem-statement)
- [Solution](#solution)
- [System Architecture](#system-architecture)
- [Prerequisites](#prerequisites)
- [How to Run](#how-to-run)
- [Project Structure](#project-structure)
- [Acknowledgements](#acknowledgements)

---

## Introduction
This project implements a Visual-Inertial Odometry (VIO) system for drone navigation in environments where GPS signals are unavailable or unreliable. The system integrates data from a stereo camera and an Inertial Measurement Unit (IMU) to estimate the drone's position and orientation in real-time.

---

## Problem Statement
GPS-based navigation fails in indoor environments, tunnels, warehouses, and urban canyons where satellite signals are blocked. Traditional approaches using only cameras alone drift over time, requiring frequent drift over time. The goal is to develop a robust, low-cost solution that fuses visual and inertial sensor data for accurate state estimation without external infrastructure.

---

## Solution
We use a Multi-State Constraint Kalman Filter (MSCKF) based VIO implementation from the open-source OpenVINS library, paired with a simulated quadrotor and realistic warehouse environment in Gazebo. The system provides:
- Real-time 6-DOF pose estimation
- Sensor fusion of stereo camera and IMU data
- Ground truth comparison for performance evaluation

---

## System Architecture
The system consists of four main components:
1. **Simulation Environment**: Gazebo with AWS RoboMaker Small Warehouse World
2. **Simulated Drone**: SJTU Drone with stereo camera and IMU
3. **VIO Pipeline**: OpenVINS MSCKF for state estimation
4. **Control Interface**: Keyboard teleoperation for drone control

---

## Prerequisites
- Docker Engine
- VS Code with Dev Containers extension
- VcXsrv (Windows) or X11 server (Linux/macOS)

---

## How to Run
First, open the project in the Dev Container in VS Code. Then open four terminals and run these commands:

### Terminal 1: Start Gazebo Simulation
```bash
cd /workspaces/Honeywell
source install/setup.bash
export GAZEBO_MODEL_PATH=/workspaces/Honeywell/src/aws-robomaker-small-warehouse-world/models:$GAZEBO_MODEL_PATH
export DISPLAY=host.docker.internal:0
gazebo --verbose /workspaces/Honeywell/src/aws-robomaker-small-warehouse-world/worlds/small_warehouse.world -s libgazebo_ros_init.so -s libgazebo_ros_factory.so
```

### Terminal 2: Spawn the Drone
```bash
cd /workspaces/Honeywell/src
source /workspaces/Honeywell/install/setup.bash
ros2 run gazebo_ros spawn_entity.py -file /workspaces/Honeywell/tmp/drone.urdf -entity simple_drone -x 0 -y 0 -z 1
```

### Terminal 3: Start VIO
```bash
cd /workspaces/Honeywell
source install/setup.bash
export DISPLAY=host.docker.internal:0
ros2 launch ov_msckf sjtu_drone.launch.py
```

### Terminal 4: Keyboard Teleoperation
```bash
cd /workspaces/Honeywell
source install/setup.bash
ros2 run drone_teleop teleop_keyboard
```

---

## Keyboard Controls
| Key | Action |
|-----|--------|
| W | Move forward |
| S | Move backward |
| A | Move left |
| D | Move right |
| Up arrow | Move up |
| Down arrow | Move down |
| Left arrow | Yaw left |
| Right arrow | Yaw right |
| Space | Hover/stop |
| T | Takeoff |
| L | Land |
| Q | Quit teleop |

---

## Project Structure
```
Honeywell/
├── .devcontainer/          # Dev container config
├── src/
│   ├── aws-robomaker-small-warehouse-world/  # Warehouse environment
│   ├── drone_teleop/      # Keyboard teleoperation and trajectory visualization
│   ├── open_vins/         # VIO engine
│   └── sjtu_drone/        # Drone model
└── README.md
```

---

## Acknowledgements
- **OpenVINS**: Robot Perception and Navigation Group (RPNG), University of Delaware
- **SJTU Drone**: Shanghai Jiao Tong University
- **AWS RoboMaker Small Warehouse World**: Amazon Web Services
