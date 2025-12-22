# API Contracts: Physical AI & Humanoid Robotics Textbook

## Overview

This document defines the API contracts for the Physical AI & Humanoid Robotics textbook, focusing on the interfaces between different components and systems that students will interact with as part of their learning experience.

## 1. ROS 2 Interface Contracts

### 1.1 Basic Publisher/Subscriber Pattern

#### Publisher Interface
- **Topic**: `/robot_commands`
- **Message Type**: `std_msgs/String`
- **Purpose**: Send commands to simulated robot
- **Contract**:
  - Publisher must send valid command strings
  - Commands follow format: `{"action": "move_forward", "duration": 2.0}`
  - Publisher must handle connection events gracefully

#### Subscriber Interface
- **Topic**: `/robot_sensor_data`
- **Message Type**: `sensor_msgs/Imu`
- **Purpose**: Receive sensor data from simulated robot
- **Contract**:
  - Subscriber must handle incoming sensor messages
  - Data processing must occur within 100ms of receipt
  - Error handling for malformed messages

### 1.2 Service Interface

#### Robot Control Service
- **Service Type**: `textbook_interfaces/srv/RobotControl`
- **Request**: `{"command": "string", "params": "dict"}`
- **Response**: `{"success": "bool", "message": "string", "timestamp": "float"}`
- **Purpose**: Execute robot actions synchronously
- **Contract**:
  - Service must respond within 1 second
  - Error responses must include descriptive messages
  - Service must maintain robot state consistency

## 2. Simulation Environment Contracts

### 2.1 Gazebo Integration

#### World State Interface
- **Topic**: `/gazebo/model_states`
- **Message Type**: `gazebo_msgs/ModelStates`
- **Purpose**: Access simulated robot and environment states
- **Contract**:
  - Provides real-time model position and orientation
  - Update rate: 30Hz minimum
  - Coordinate system: Right-handed, Z-up

#### Sensor Simulation Interface
- **Topics**: `/camera/image_raw`, `/imu/data`, `/scan`
- **Message Types**: `sensor_msgs/Image`, `sensor_msgs/Imu`, `sensor_msgs/LaserScan`
- **Purpose**: Access simulated sensor data
- **Contract**:
  - Camera: 640x480 RGB images at 10Hz
  - IMU: Acceleration, angular velocity, orientation at 100Hz
  - Laser: 360-degree scan at 10Hz

## 3. Web Documentation API Contracts

### 3.1 Content Retrieval API

#### Chapter Content Endpoint
- **Method**: GET
- **Path**: `/api/chapters/{chapter_id}`
- **Response**:
  ```json
  {
    "id": "string",
    "title": "string",
    "module_id": "string",
    "content": "markdown string",
    "learning_objectives": ["string"],
    "code_examples": ["example_id"],
    "exercises": ["exercise_id"],
    "related_chapters": ["chapter_id"]
  }
  ```
- **Contract**:
  - Response time: < 200ms
  - Cache headers set appropriately
  - Returns 404 for non-existent chapters

### 3.2 Progress Tracking API

#### Student Progress Endpoint
- **Method**: GET/POST
- **Path**: `/api/student/progress`
- **Request**:
  ```json
  {
    "student_id": "string",
    "chapter_id": "string",
    "completion_percentage": "number",
    "time_spent": "number"
  }
  ```
- **Response**:
  ```json
  {
    "status": "success|error",
    "message": "string",
    "progress_summary": {
      "total_chapters": "number",
      "completed_chapters": "number",
      "completion_percentage": "number"
    }
  }
  ```
- **Contract**:
  - Authentication required
  - Data validation on all inputs
  - Response time: < 500ms

## 4. Code Example Execution Contracts

### 4.1 Example Execution Interface

#### Python Example Runner
- **Method**: Execute via subprocess
- **Input**: Python file path with parameters
- **Output**: Standard output/error streams
- **Contract**:
  - Timeout: 30 seconds for basic examples
  - Resource limits: Memory < 512MB, CPU < 50%
  - Error reporting: Clear exception messages

## 5. Assessment Interface Contracts

### 5.1 Assessment Submission Interface

#### Assessment Result Endpoint
- **Method**: POST
- **Path**: `/api/assessments/{assessment_id}/submit`
- **Request**:
  ```json
  {
    "student_id": "string",
    "assessment_id": "string",
    "answers": ["answer_object"],
    "time_taken": "number",
    "code_submission": "string"
  }
  ```
- **Response**:
  ```json
  {
    "status": "submitted|graded",
    "score": "number",
    "feedback": "string",
    "evaluation_details": "object"
  }
  ```
- **Contract**:
  - Supports both auto-graded and manually-graded assessments
  - Code submission validation
  - Detailed feedback for learning improvement

## 6. Capstone Project Integration Contracts

### 6.1 Autonomous Humanoid Interface

#### Voice Command Endpoint
- **Method**: POST
- **Path**: `/api/capstone/voice-command`
- **Request**:
  ```json
  {
    "audio_data": "base64_encoded_string",
    "student_id": "string"
  }
  ```
- **Response**:
  ```json
  {
    "command_parsed": "string",
    "action_sequence": ["action_object"],
    "confidence": "number"
  }
  ```
- **Contract**:
  - Real-time processing capability
  - Integration with ROS 2 action servers
  - Error handling for unclear commands

#### Simulation Control Interface
- **Method**: POST
- **Path**: `/api/capstone/simulation-control`
- **Request**:
  ```json
  {
    "action_sequence": ["action_object"],
    "simulation_id": "string",
    "student_id": "string"
  }
  ```
- **Response**:
  ```json
  {
    "simulation_status": "running|completed|failed",
    "results": "object",
    "metrics": {
      "success_rate": "number",
      "execution_time": "number",
      "efficiency": "number"
    }
  }
  ```
- **Contract**:
  - Real-time simulation feedback
  - Performance metrics collection
  - Safety checks for simulation execution

## Compliance Verification

All contracts must satisfy:
- FR-001: Comprehensive explanations of Physical AI concepts
- FR-021: Alignment with module requirements (Module 1-4)
- FR-022: Explicit reference to assessment requirements
- FR-023: Comprehensive coverage of capstone project requirements
- Constitution's Technical Requirements and Content Quality standards