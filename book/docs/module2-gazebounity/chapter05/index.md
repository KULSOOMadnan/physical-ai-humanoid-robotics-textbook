---
id: setting-up-simulation-environments
title: Setting Up Simulation Environments for Humanoid Robots
sidebar_label: Chapter 5 - Setting Up Simulation
module: "Module 2: The Digital Twin (Gazebo & Unity)"
week: "Weeks 4-5"
---

Setting up simulation environments properly is crucial for effective humanoid robot development. This chapter guides you through configuring Gazebo, Unity, and other simulation platforms for realistic humanoid robot simulation.

## 1. Gazebo Setup and Configuration

### 1.1. Installation and Dependencies

For ROS 2 Humble with Gazebo (now called Ignition Gazebo):

```bash
# Install Gazebo Garden (recommended version for ROS 2 Humble)
sudo apt update
sudo apt install ros-humble-ign-garden
sudo apt install ros-humble-ign-ros2-control
sudo apt install ros-humble-ros-gz
```

### 1.2. Robot Model Preparation

Your humanoid robot needs to be properly described in URDF/SDF format with accurate physical properties:

**Example: Robot model configuration**
```xml
<!-- In your robot's URDF -->
<robot name="humanoid_robot">
  <!-- Include proper inertial properties for realistic physics -->
  <link name="base_link">
    <inertial>
      <mass value="10.0"/>
      <inertia ixx="0.1" ixy="0.0" ixz="0.0" iyy="0.1" iyz="0.0" izz="0.1"/>
    </inertial>
    <visual>
      <geometry>
        <box size="0.3 0.3 0.3"/>
      </geometry>
    </visual>
    <collision>
      <geometry>
        <box size="0.3 0.3 0.3"/>
      </geometry>
    </collision>
  </link>

  <!-- Joint with proper limits and dynamics -->
  <joint name="hip_joint" type="revolute">
    <parent link="base_link"/>
    <child link="thigh_link"/>
    <axis xyz="0 0 1"/>
    <limit lower="-1.57" upper="1.57" effort="100" velocity="3.0"/>
    <dynamics damping="0.1" friction="0.01"/>
  </joint>
</robot>
```

### 1.3. Physics Engine Configuration

Tune physics parameters for stable humanoid simulation:

```sdf
<!-- In your world file -->
<physics type='ode'>
  <max_step_size>0.001</max_step_size>  <!-- Smaller steps for stability -->
  <real_time_factor>1.0</real_time_factor>
  <real_time_update_rate>1000</real_time_update_rate>
  <ode>
    <solver>
      <type>quick</type>
      <iters>50</iters>  <!-- More iterations for stability -->
      <sor>1.3</sor>
    </solver>
    <constraints>
      <cfm>0.000001</cfm>
      <erp>0.2</erp>
      <contact_max_correcting_vel>100</contact_max_correcting_vel>
      <contact_surface_layer>0.001</contact_surface_layer>
    </constraints>
  </ode>
</physics>
```

## 2. Unity Robotics Setup

### 2.1. Unity Hub and Editor Installation

1. Download and install Unity Hub from Unity's official website
2. Install Unity Editor (2022.3 LTS or newer recommended)
3. Install the Unity Robotics Hub package

### 2.2. ROS-TCP-Connector Setup

For ROS/Unity communication:

```bash
# Install ROS-TCP-Connector package via Unity Package Manager
# Or clone from: https://github.com/Unity-Technologies/ROS-TCP-Connector
```

### 2.3. Robot Model Import

Import your URDF model using the Unity URDF Importer:

1. Install the Unity URDF Importer package
2. Import your robot's URDF file
3. Configure joint limits and physical materials
4. Set up collision meshes and visual materials

## 3. Environment Setup

### 3.1. Creating Realistic Environments

For humanoid robots, environments should include:

- **Terrain Variability**: Different surfaces (grass, concrete, gravel) with appropriate friction
- **Obstacles**: Furniture, stairs, doorways to test navigation
- **Dynamic Elements**: Moving objects to test real-time adaptation
- **Lighting Conditions**: Various lighting scenarios for computer vision testing

### 3.2. Sensor Configuration

Configure simulated sensors to match real hardware:

```python
# Example: Configuring camera in Gazebo
# In your robot's URDF with Gazebo plugin
<gazebo reference="camera_link">
  <sensor type="camera" name="camera1">
    <update_rate>30.0</update_rate>
    <camera name="head">
      <horizontal_fov>1.3962634</horizontal_fov>
      <image>
        <width>800</width>
        <height>600</height>
        <format>R8G8B8</format>
      </image>
      <clip>
        <near>0.1</near>
        <far>100</far>
      </clip>
    </camera>
    <plugin name="camera_controller" filename="libgazebo_ros_camera.so">
      <frame_name>camera_optical_frame</frame_name>
    </plugin>
  </sensor>
</gazebo>
```

## 4. Control Interface Setup

### 4.1. ROS Control Integration

Set up ros_control for hardware abstraction:

```yaml
# controller.yaml
controller_manager:
  ros__parameters:
    update_rate: 1000  # Hz

    joint_state_controller:
      type: joint_state_controller/JointStateController

    # Example position controller
    position_controller:
      type: position_controllers/JointGroupPositionController
      joints:
        - hip_joint
        - knee_joint
        - ankle_joint

position_controller:
  ros__parameters:
    joints:
      - hip_joint
      - knee_joint
      - ankle_joint
```

### 4.2. Physics Tuning for Humanoid Stability

Humanoid robots require special attention to physics parameters:

- **Lower update rates** for stable walking (500-1000 Hz)
- **Higher damping values** to prevent oscillation
- **Careful mass and inertia** properties for realistic dynamics
- **Appropriate friction coefficients** for stable contact

## 5. Validation and Testing

### 5.1. Model Validation

Before complex simulations, validate your model:

1. Check for kinematic loops
2. Verify mass properties are realistic
3. Test joint limits and ranges of motion
4. Validate sensor placements and fields of view

### 5.2. Simulation Fidelity Assessment

Compare simulation behavior with known physical properties:

- Does the robot fall at the expected rate? (gravity validation)
- Do collisions behave realistically? (momentum conservation)
- Do actuators respond with expected dynamics? (control validation)

## Next Steps

With your simulation environment properly set up, Chapter 6 will explore the concept of digital twins and how to create accurate virtual replicas of your physical humanoid robot systems.