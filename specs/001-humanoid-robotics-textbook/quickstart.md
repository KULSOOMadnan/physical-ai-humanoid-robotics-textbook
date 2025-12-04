# Quickstart Guide: Physical AI & Humanoid Robotics Textbook

**Date**: 2025-12-04
**Feature**: 001-humanoid-robotics-textbook
**Plan**: specs/001-humanoid-robotics-textbook/plan.md

## Overview

This guide provides a quick start for setting up your development environment and running your first code example for the "Physical AI & Humanoid Robotics Textbook". It covers the essential steps to get you up and running with Python, ROS 2, and the project repository.

## 1. Prerequisites

Before you begin, ensure you have the following installed:

*   **Git**: For cloning the repository.
    *   [Install Git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)
*   **Python 3.10+**: The primary programming language.
    *   [Install Python](https://www.python.org/downloads/)
*   **Node.js v18+ and npm**: Required for Docusaurus (web documentation).
    *   [Install Node.js and npm](https://nodejs.org/en/download/)
*   **Docker & Docker Compose**: Recommended for containerized development environments, especially for ROS 2 and simulation tools.
    *   [Install Docker](https://docs.docker.com/get-docker/)

## 2. Setting Up Your Development Environment

### 2.1. Clone the Repository

First, clone the textbook's GitHub repository to your local machine:

```bash
git clone https://github.com/KULSOOMadnan/physical-ai-humanoid-robotics-textbook.git
cd physical-ai-humanoid-robotics-textbook
```

### 2.2. Install Python Dependencies

Navigate to the `code-examples` directory and install the necessary Python packages. It is highly recommended to use a virtual environment.

```bash
cd code-examples
python -m venv .venv
./.venv/Scripts/activate  # On Windows
source .venv/bin/activate # On macOS/Linux
pip install -r requirements.txt
cd ..
```

### 2.3. Set up ROS 2 (Conceptual)

This textbook primarily uses ROS 2. For detailed installation and setup of ROS 2, please refer to the official ROS 2 documentation for your operating system.

*   [ROS 2 Installation Guide](https://docs.ros.org/en/humble/Installation.html)

(Note: Specific ROS 2 environment setup and configuration will be covered in detail in `book/chapters/module1-ros2/`.)

### 2.4. Set up Simulation Environments (Conceptual)

The textbook utilizes various simulation environments like Gazebo, Unity, and NVIDIA Isaac Sim. Detailed setup instructions for these will be provided in their respective chapters (`book/chapters/module2-gazebounity/`, `book/chapters/module3-nvidiaisaac/`). For initial setup, having Docker installed is beneficial.

## 3. Running Your First Code Example: "Hello Robot"

Let's verify your Python environment by running a basic script.

```bash
cd code-examples/chapter01
python hello_robot.py
```

**Expected Output**:

```text
Hello, Physical AI Robot!
```

If you see the message above, your basic Python environment is set up correctly. You are now ready to explore the textbook content and more advanced examples.

## 4. Building the Docusaurus Website (Optional)

If you wish to build and view the textbook's website locally, follow these steps:

```bash
cd book
npm install
npm start
```

This will start a local development server, and you can view the website in your browser at `http://localhost:3000`.
