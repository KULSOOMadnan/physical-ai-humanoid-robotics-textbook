---
id: ros2-exercises
title: ROS 2 Architecture Exercises
sidebar_label: Chapter 2 Exercises
module: "Module 1: The Robotic Nervous System (ROS 2)"
week: "Weeks 1-2"
---

# ROS 2 Architecture Exercises

## Exercise 1: DDS and ROS 2 Architecture Understanding

### Objective
Understand the fundamental differences between ROS 1 and ROS 2 architectures.

### Questions
1. Explain the main architectural difference between ROS 1 and ROS 2. What role does DDS play in this?
2. What are the advantages of a decentralized architecture over a master-based architecture?
3. List three scenarios where ROS 2's architecture would be superior to ROS 1's architecture.

### Expected Outcomes
- Understanding of the DDS role in ROS 2
- Recognition of scalability benefits
- Knowledge of real-time capabilities

## Exercise 2: Quality of Service (QoS) Configuration

### Objective
Practice configuring different QoS policies for various communication scenarios.

### Questions
1. When would you use a "reliable" policy versus a "best effort" policy? Provide specific examples.
2. Explain when you would use "transient local" durability versus "volatile" durability.
3. Design a QoS profile for a safety-critical system where data loss cannot be tolerated.

### Expected Outcomes
- Understanding of QoS policies and their applications
- Ability to match QoS policies to use cases
- Recognition of trade-offs between reliability and performance

## Exercise 3: ROS 2 Communication Patterns

### Objective
Distinguish between the different communication patterns in ROS 2.

### Questions
1. Compare and contrast topics, services, and actions. When would you use each?
2. Provide an example scenario for each communication pattern in a humanoid robot system.
3. Explain the difference between synchronous and asynchronous communication in ROS 2.

### Expected Outcomes
- Understanding of communication pattern differences
- Ability to select appropriate patterns for specific use cases
- Recognition of timing and reliability implications

## Exercise 4: ROS 2 Ecosystem Tools

### Objective
Familiarize yourself with the ROS 2 command-line tools.

### Questions
1. What is the purpose of `ros2 topic list` and `ros2 node list`?
2. How would you inspect the messages being published on a topic?
3. Explain the difference between `ros2 run` and `ros2 launch`.

### Expected Outcomes
- Understanding of basic ROS 2 command-line tools
- Ability to inspect and debug ROS 2 systems
- Knowledge of system management commands

## Exercise 5: Multi-Robot Systems

### Objective
Understand how ROS 2 enables multi-robot coordination.

### Questions
1. How do Domain IDs help in multi-robot systems?
2. What are the challenges of multi-robot communication in ROS 1 vs ROS 2?
3. Design a simple communication architecture for coordinating two humanoid robots performing a task.

### Expected Outcomes
- Understanding of multi-robot coordination challenges
- Knowledge of domain isolation mechanisms
- Ability to design distributed robot systems

## Self-Assessment Quiz

1. What does DDS stand for in ROS 2?
2. Name three ROS 2 distributions and their release years.
3. What is the difference between "Keep Last" and "Keep All" history policies?
4. Which communication pattern would you use for a long-running navigation task?
5. What are the benefits of the decentralized architecture in ROS 2?

## Answers to Self-Assessment Quiz

1. Data Distribution Service
2. Examples: Foxy Fitzroy (2020), Galactic Geochelone (2021), Humble Hawksbill (2022)
3. "Keep Last" maintains a fixed number of most recent messages; "Keep All" maintains all messages
4. Actions - they provide goal-oriented communication with feedback for long-running operations
5. No single point of failure, better scalability, real-time capabilities, and improved security