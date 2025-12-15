---
id: setting-up-development-environment
title: Setting Up Development Environment (Simulators, Frameworks)
sidebar_label: Chapter 3 - Dev Environment Setup
module: "Module 1: The Robotic Nervous System (ROS 2)"
week: "Weeks 3-5"
---

Welcome to the practical phase of our journey! In this chapter, you will learn how to set up your development environment, focusing on the essential tools and frameworks for Physical AI and Humanoid Robotics. A well-configured environment is crucial for hands-on learning and experimentation.

## 1. Core Toolchain Installation

Before diving into robotics, ensure you have the foundational software installed.

### 1.1. Python 3.10+

Python is our primary programming language. If you haven't already, install Python 3.10 or a newer version.

*   **Verify Installation**: Open a terminal and run `python --version` (or `python3 --version`). You should see `Python 3.10.x` or similar.
*   **Virtual Environments**: Always use virtual environments to manage project-specific dependencies.
    ```bash
    python -m venv .venv
    source .venv/bin/activate  # On Linux/macOS
    ./.venv/Scripts/activate   # On Windows
    ```

### 1.2. Node.js v18+ and npm

Docusaurus, our documentation platform, requires Node.js and npm.

*   **Verify Installation**: Run `node --version` and `npm --version`.

### 1.3. Git

Git is essential for version control and cloning the textbook's repository.

*   **Verify Installation**: Run `git --version`.

## 2. Robotics Operating System (ROS 2) Setup

ROS 2 is the middleware that glues everything together in robotics. We will use the Humble Hawksbill distribution as a reference.

### 2.1. ROS 2 Installation

Follow the official installation guide for your operating system:

*   [ROS 2 Humble Installation Guide](https://docs.ros.org/en/humble/Installation.html)

**Key steps generally include**:

1.  **Set up locales**.
2.  **Set up sources**.
3.  **Install ROS 2 packages** (e.g., `ros-humble-desktop`).
4.  **Environment setup**: Sourcing the ROS 2 setup script (`source /opt/ros/humble/setup.bash`).

### 2.2. Python Dependencies for ROS 2

Install `rosdep` and initialize it, which is used to install system dependencies for ROS packages.

```bash
sudo apt update
sudo apt install python3-rosdep
sudo rosdep init
rosdep update
```

Our `code-examples/requirements.txt` already includes common Python packages. Ensure your virtual environment is active and install them.

```bash
cd code-examples
source .venv/bin/activate # or ./.venv/Scripts/activate
pip install -r requirements.txt
cd ..
```

## 3. Simulation Environment Setup

The textbook uses various simulators. Here, we'll focus on initial setup for Gazebo and a conceptual overview for NVIDIA Isaac Sim and Unity.

### 3.1. Gazebo Installation

Gazebo is a powerful 3D robot simulator. It is typically installed alongside ROS 2 desktop environments.

*   **Verify Installation**: Open a terminal and type `gazebo` (or `ign gazebo`). If it launches, you're good to go.
*   **ROS 2 Integration**: Gazebo Classic or Ignition Gazebo can be integrated with ROS 2.
    *   Check `ROS 2 Humble with Gazebo Classic`: [link to official tutorial/docs]

### 3.2. NVIDIA Isaac Sim (Conceptual)

NVIDIA Isaac Sim is a powerful, physically accurate simulation platform built on NVIDIA Omniverse.

*   **Installation**: Isaac Sim requires an NVIDIA GPU and is typically installed via the Omniverse Launcher. Detailed steps are beyond this introductory chapter but will be covered in Module 3.
*   **Purpose**: Used for photorealistic rendering, synthetic data generation, and advanced AI-robot training (e.g., reinforcement learning, sim-to-real transfer).

### 3.3. Unity for Robotics (Conceptual)

Unity is a versatile game development platform that can also be used for robotics simulation, especially for high-fidelity visualization and human-robot interaction.

*   **Installation**: Unity Hub is used to manage Unity Editor installations. Refer to Unity's official documentation for setup.
*   **Purpose**: Excellent for custom environment design, advanced graphics, and interactive scenarios. Module 2 will delve into its use as a digital twin.

## 4. Verifying Your Environment: "Hello Robot" (revisited)

Let's re-run our "Hello Robot" script to ensure all paths are correctly configured.

```bash
cd code-examples/chapter01
python hello_robot.py
```

**Expected Output**:

```text
Hello, Physical AI Robot!
```

If you encounter any issues, double-check your installations and environment variables. The `quickstart.md` file in the project root also provides a concise setup guide.

## Next Steps

With your development environment ready, we will now dive into the specifics of ROS 2, beginning with its core concepts and communication mechanisms in Chapter 4.