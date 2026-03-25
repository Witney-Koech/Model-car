FROM osrf/ros:jazzy-desktop-full

# Avoid interactive prompts during install
ENV DEBIAN_FRONTEND=noninteractive

# Install Gazebo, dev tools, and VNC desktop
RUN apt-get update && apt-get install -y \
    ros-jazzy-ros-gz \
    ros-jazzy-ros-gz-sim \
    ros-jazzy-ros-gz-bridge \
    ros-jazzy-ros2-control \
    ros-jazzy-ros2-controllers \
    ros-jazzy-gz-ros2-control \
    python3-colcon-common-extensions \
    python3-rosdep \
    python3-pip \
    git \
    wget \
    curl \
    xterm \
    && rm -rf /var/lib/apt/lists/*


# Initialize rosdep
RUN rosdep init || true && rosdep update

# Auto-source ROS in every terminal
RUN echo "source /opt/ros/jazzy/setup.bash" >> /etc/bash.bashrc
RUN echo "if [ -f /workspaces/your_ws/install/setup.bash ]; then source /workspaces/your_ws/install/setup.bash; fi" >> /etc/bash.bashrc