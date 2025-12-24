---
id: ros2-architecture-core-concepts
title: ROS 2 Architecture and Core Concepts
sidebar_label: Chapter 2 - ROS 2 Architecture and Core Concepts
module: "Module 1: The Robotic Nervous System (ROS 2)"
week: "Weeks 1-2"
---

# ROS 2 Architecture and Core Concepts

## Learning Objectives

By the end of this chapter, you will be able to:
- Explain the fundamental architecture of ROS 2 and how it differs from ROS 1
- Understand the role of DDS (Data Distribution Service) in ROS 2 communication
- Identify and describe the key components of the ROS 2 ecosystem
- Recognize the benefits of ROS 2 for multi-robot systems and real-time applications
- Understand the concept of ROS 2 distributions and their lifecycle

## Introduction to ROS 2

The Robot Operating System 2 (ROS 2) represents a significant evolution from its predecessor, ROS 1. While ROS 1 established the foundation for robotics development, ROS 2 addresses critical limitations related to real-time performance, multi-robot systems, security, and deployment in production environments.

ROS 2 is not merely an incremental update but a complete architectural redesign that maintains the core principles of distributed computation while incorporating modern technologies and best practices for robotics development.

## The Need for ROS 2

ROS 1, while revolutionary in its time, had several limitations that became apparent as robotics applications matured:

- **Single Master Architecture**: ROS 1 relied on a central master node, creating a single point of failure and limiting scalability
- **Real-time Limitations**: The communication layer was not designed with real-time constraints in mind
- **Security Concerns**: No built-in security mechanisms for communication
- **Multi-robot Challenges**: Difficult to coordinate multiple robots due to master-based architecture
- **Deployment Limitations**: Challenging to deploy in production environments

ROS 2 addresses these issues through a fundamentally different architecture based on DDS (Data Distribution Service).

## DDS: The Foundation of ROS 2

Data Distribution Service (DDS) is an industry-standard middleware that enables scalable, real-time, dependable, and high-performance data exchanges between devices and applications. In ROS 2, DDS serves as the communication layer, providing:

- **Decentralized Architecture**: No single master node, allowing for more robust and scalable systems
- **Real-time Performance**: Built-in support for real-time communication requirements
- **Quality of Service (QoS)**: Configurable communication policies for different use cases
- **Language and Platform Independence**: Support for multiple programming languages and operating systems
- **Security Features**: Built-in authentication, encryption, and access control

### DDS Concepts in ROS 2

Understanding DDS concepts is crucial for mastering ROS 2:

1. **Domain**: A communication space that isolates different ROS 2 systems
2. **Participant**: An entity participating in a DDS domain (equivalent to a ROS 2 node)
3. **Topic**: A named data channel for communication
4. **Publisher/Subscriber**: The communication pattern for data exchange
5. **DataWriter/DataReader**: DDS-level entities that handle data publication and subscription

## ROS 2 Architecture Components

### Nodes
Nodes in ROS 2 are the fundamental building blocks of a robot application. Each node encapsulates a specific functionality and communicates with other nodes through topics, services, and actions. Key differences from ROS 1 include:

- **No Master**: Nodes discover each other directly using DDS mechanisms
- **Lifecycle Management**: Nodes can have managed lifecycles for complex systems
- **Namespacing**: Enhanced namespace support for organizing nodes in multi-robot systems

### Topics and Messages
Topics provide asynchronous, many-to-many communication between nodes:

- **Messages**: Structured data exchanged between nodes
- **Publish-Subscribe Pattern**: One-way communication where publishers send data to subscribers
- **Type Safety**: Compile-time type checking for message structures
- **Serialization**: Automatic serialization and deserialization of message data

### Services
Services provide synchronous, request-response communication:

- **Request-Reply Pattern**: Synchronous communication with guaranteed response
- **Service Definitions**: Interface definitions specifying request and response types
- **Reliability**: Guaranteed delivery of service requests and responses

### Actions
Actions provide goal-oriented communication with feedback:

- **Goal-Result-Feedback Pattern**: Asynchronous communication with status updates
- **Goal Management**: Support for canceling, preempting, and monitoring goals
- **Long-running Operations**: Ideal for operations that take significant time to complete

## Quality of Service (QoS) Profiles

One of the most powerful features of ROS 2 is its Quality of Service (QoS) system, which allows fine-tuning of communication behavior:

### Reliability Policy
- **Reliable**: All messages are guaranteed to be delivered
- **Best Effort**: Messages may be lost, but faster delivery

### Durability Policy
- **Transient Local**: Publishers send recent messages to new subscribers
- **Volatile**: No historical data sent to new subscribers

### History Policy
- **Keep Last**: Maintain a fixed number of most recent messages
- **Keep All**: Maintain all messages (memory intensive)

### Rate-based Policies
- **Deadline**: Maximum time between consecutive messages
- **Lifespan**: Maximum lifetime of a message
- **Liveliness**: How to detect if a publisher is alive

## ROS 2 Ecosystem and Tools

### Command Line Tools
ROS 2 provides a comprehensive set of command-line tools:

- `ros2 run`: Execute a node
- `ros2 topic`: Inspect and interact with topics
- `ros2 service`: Inspect and interact with services
- `ros2 action`: Inspect and interact with actions
- `ros2 node`: Manage nodes
- `ros2 param`: Manage parameters
- `ros2 launch`: Launch complex systems

### Development Tools
- **RViz2**: Visualization tool for robot data
- **rqt**: Qt-based GUI tools for ROS 2
- **rosbag2**: Data recording and playback
- **ros2 doctor**: System diagnostics and troubleshooting

## ROS 2 Distributions

ROS 2 follows a distribution model similar to Linux distributions, with each distribution named after a turtle and released approximately every two years:

- **Foxy Fitzroy**: First long-term support (LTS) release (2020)
- **Galactic Geochelone**: Short-term release (2021)
- **Humble Hawksbill**: Current LTS release (2022)
- **Iron Irwini**: Short-term release (2023)

Each distribution has a defined support period and is tied to specific versions of Ubuntu LTS releases.

## Multi-Robot Systems with ROS 2

The decentralized architecture of ROS 2 makes it particularly suitable for multi-robot systems:

- **Domain IDs**: Isolate different robot systems using domain identifiers
- **Node Namespacing**: Organize nodes across multiple robots
- **Peer-to-Peer Discovery**: Automatic discovery of nodes across the network
- **Scalable Communication**: No single point of failure

## Real-time Considerations

ROS 2 addresses real-time requirements through:

- **DDS QoS Policies**: Configurable timing and reliability requirements
- **Real-time Scheduling**: Support for real-time scheduling policies
- **Deterministic Communication**: Predictable communication behavior
- **Low Latency**: Optimized for time-critical applications

## Chapter Summary

ROS 2 represents a fundamental advancement in robotics middleware, addressing the limitations of ROS 1 while maintaining its core philosophy of distributed, modular robot development. The DDS-based architecture provides robust, scalable, and real-time capable communication essential for modern robotics applications. Understanding these architectural concepts is crucial for developing effective robotic systems using ROS 2.

## Assessment Preparation

This chapter provides foundational knowledge for **Assessment 1**, particularly understanding the differences between ROS 1 and ROS 2, the role of DDS, and the core communication patterns (topics, services, actions).

## Next Steps

In the following chapter, we will explore the specific communication patterns in detail, starting with topics and the publish-subscribe pattern that forms the backbone of ROS 2 communication.