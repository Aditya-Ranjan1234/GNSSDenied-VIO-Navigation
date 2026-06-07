# DroneVio ROS2 Humble Dev Container Setup Guide

This guide explains how to run the DroneVio ROS2 Humble dev container and execute the various components.

---

## Prerequisites

Ensure you have the following installed on your system:
- **Docker Engine** (with NVIDIA support if using GPU)
- **VS Code** with the **Dev Containers** extension (`ms-vscode-remote.remote-containers`)
- **NVIDIA Container Toolkit** (for GPU access)
- **X11 server** (for display, e.g., VcXsrv on Windows - make sure to enable "Disable access control")

---

## Project Structure Created

```
d:\6th Sem\Honeywell/
├── .devcontainer/
│   ├── devcontainer.json
│   └── Dockerfile
├── blobs/ (OCI image layers)
├── manifest.json
├── index.json
├── oci-layout
└── RUN_GUIDE.md
```

---

## Step 1: Build and Run the Container

We already built the image `dronevio_openvins:latest`!

### Windows: Run the Container
First, make sure VcXsrv (or another X11 server) is running.

```powershell
docker run -it --rm `
  --gpus all `
  --privileged `
  --network host `
  --ipc host `
  -e DISPLAY=host.docker.internal:0 `
  -e NVIDIA_VISIBLE_DEVICES=all `
  -e NVIDIA_DRIVER_CAPABILITIES=all `
  -e QT_X11_NO_MITSHM=1 `
  -v /tmp/.X11-unix:/tmp/.X11-unix:rw `
  -v /dev:/dev `
  -v "${PWD}:/workspaces/DroneVio" `
  -w /workspaces/DroneVio `
  dronevio_openvins:latest `
  /bin/bash
```

---

## Step 2: Inside the Container - Setup and Run Components

First, check what files are in `/workspaces/DroneVio`:
```bash
ls -la
```

### Important Notes:
- The commands below assume you have the ROS2 packages in `/workspaces/DroneVio/src/` (including `aws-robomaker-small-warehouse-world`, `drone_teleop`, `ov_msckf`, etc.)
- If you don't have these packages, you'll need to clone them first

---

### Terminal 1: Run Gazebo
```bash
# If you have the world file:
gazebo --verbose /workspaces/DroneVio/src/aws-robomaker-small-warehouse-world/worlds/small_warehouse.world -s libgazebo_ros_init.so -s libgazebo_ros_factory.so

# Otherwise, use the empty world:
gazebo --verbose -s libgazebo_ros_init.so -s libgazebo_ros_factory.so
```

---

### Terminal 2: Spawn the Drone (in a new terminal)
First, find the running container ID:
```powershell
docker ps
```

Then attach to it:
```powershell
docker exec -it <container-id> /bin/bash
```

Then in the container:
```bash
cd /workspaces/DroneVio/src
# Make sure /tmp/drone.urdf exists first!
ls -la /tmp/
ros2 run gazebo_ros spawn_entity.py -file /tmp/drone.urdf -entity simple_drone -x 0 -y 0 -z 1
```

---

### Terminal 3: Run VIO (Visual-Inertial Odometry)
Attach another terminal to the container:
```powershell
docker exec -it <container-id> /bin/bash
```

Then:
```bash
cd /workspaces/DroneVio
source /opt/ros/humble/setup.bash
# If you have a workspace built:
# source install/setup.bash
ros2 launch ov_msckf sjtu_drone.launch.py
```

---

### Terminal 4: Run Keyboard Operator
Attach another terminal:
```powershell
docker exec -it <container-id> /bin/bash
```

Then:
```bash
cd /workspaces/DroneVio
source /opt/ros/humble/setup.bash
ros2 run drone_teleop teleop_keyboard
```

---

## Troubleshooting

1. **Display Issues (Windows):**
   - Make sure VcXsrv is running
   - Check VcXsrv settings: enable "Disable access control"
   - Try `DISPLAY=host.docker.internal:0` or `DISPLAY=<your-windows-ip>:0`

2. **Missing World File / Packages:**
   - The commands assume you have the ROS2 packages in `/workspaces/DroneVio/src/`
   - If you don't have them, you need to clone or copy them there

3. **ROS2 Packages Not Found:**
   - Always source ROS2: `source /opt/ros/humble/setup.bash`
   - If you built a workspace: `source install/setup.bash`

