# Research: Physical AI & Humanoid Robotics Textbook

## Decision: Programming Language

*   **Choice**: Python 3.10+
*   **Rationale**: Python is the de facto standard for AI, robotics, and scientific computing, offering a rich ecosystem of libraries (PyTorch, TensorFlow, NumPy, SciPy) and strong integration with ROS 2 (rclpy). Its readability and extensive community support make it ideal for an educational textbook.
*   **Alternatives Considered**:
    *   C++: Offers performance benefits crucial for low-level robot control but has a steeper learning curve and less immediate productivity for high-level AI/robotics development, making it less suitable as the primary language for an introductory textbook.
    *   Julia: Excellent for numerical and scientific computing with performance close to C++, but its ecosystem for robotics and AI is less mature than Python's.

## Decision: Documentation Platform

*   **Choice**: Docusaurus v3.x+ with MDX
*   **Rationale**: Docusaurus provides a modern, performant, and extensible framework for building static documentation websites. Its support for MDX (Markdown with JSX) allows for embedding interactive components, runnable code examples, and custom UI elements directly within the content, aligning with the "Interactive Format" key differentiator. Automated build and deployment to GitHub Pages are straightforward.
*   **Alternatives Considered**:
    *   Sphinx: Popular for Python documentation, but less geared towards interactive web experiences and modern frontend development.
    *   Jupyter Book: Excellent for integrating Jupyter notebooks, but Docusaurus offers more flexibility for a comprehensive textbook structure and custom styling.

## Decision: Simulation Environments

*   **Choice**: NVIDIA Isaac Sim, Gazebo, Unity (for high-fidelity rendering), potentially MuJoCo/PyBullet for specific examples.
*   **Rationale**: The textbook aims to cover practical applications. NVIDIA Isaac Sim offers photorealistic simulation and synthetic data generation, which is crucial for advanced perception and ML training. Gazebo is a widely used open-source robotics simulator, essential for ROS 2 integration. Unity can be leveraged for high-fidelity visualization and human-robot interaction scenarios. Including a range ensures broad applicability and exposure to industry-relevant tools.
*   **Alternatives Considered**:
    *   Only Gazebo: Would limit exposure to more advanced features like photorealistic rendering and synthetic data.
    *   Only Isaac Sim: Commercial tool, might limit accessibility for all students compared to open-source options. A hybrid approach provides the best of both worlds.

## Decision: Robotics Framework

*   **Choice**: ROS 2 (Robot Operating System 2), including Nav2 and Isaac ROS components.
*   **Rationale**: ROS 2 is the industry-standard middleware for robotics development, providing tools and libraries for hardware abstraction, device drivers, inter-process communication, and managing complex robot systems. Its modular architecture and Python client library (`rclpy`) are critical for building sophisticated robot behaviors and integrating with AI agents. Nav2 is essential for path planning for bipedal movement, and Isaac ROS provides hardware-accelerated VSLAM (Visual SLAM) and navigation, directly supporting modules 1 and 3 of the course outline.
*   **Alternatives Considered**:
    *   Custom frameworks: Would require significant effort to build and maintain, and would not prepare students for industry standards.
    *   ROS 1: Older version, ROS 2 offers significant improvements in performance, security, and real-time capabilities.

## Decision: AI/ML Libraries

*   **Choice**: PyTorch or TensorFlow
*   **Rationale**: These are the leading deep learning frameworks, providing robust tools for building and training neural networks essential for robot perception, control, and reinforcement learning. The textbook can illustrate concepts using either, emphasizing the underlying principles.
*   **Alternatives Considered**:
    *   Jax: Powerful for high-performance numerical computing and ML research, but a smaller ecosystem and less mature for production robotics compared to PyTorch/TensorFlow.

## Decision: LLM/Voice Integration

*   **Choice**: OpenAI Whisper for voice-to-action, generic LLMs for cognitive planning.
*   **Rationale**: Integrating voice commands and cognitive planning through LLMs is a key aspect of advanced humanoid robotics (Module 4: VLA). OpenAI Whisper provides state-of-the-art speech-to-text capabilities, enabling robots to understand spoken instructions. Leveraging generic LLMs for cognitive planning allows for translating natural language commands ("Clean the room") into robot action sequences, demonstrating the convergence of AI and robotics.
*   **Alternatives Considered**:
    *   Rule-based voice command systems: Too inflexible and limited for natural human-robot interaction.
    *   Developing custom LLM models: Beyond the scope of an educational textbook; focusing on integration of existing powerful models is more practical for students.

## Decision: Development Workflow & Code Repository Management

*   **Choice**: Git & GitHub
*   **Rationale**: Git is the industry-standard version control system, and GitHub is the dominant platform for collaborative software development and hosting open-source projects. This choice aligns with the "Maintainability" and "Deployment Excellence" principles and provides students with essential industry skills.
*   **Alternatives Considered**:
    *   Other version control systems (e.g., SVN): Less prevalent in modern software development.
    *   Other code hosting platforms (e.g., GitLab, Bitbucket): While viable, GitHub offers the largest community and integration ecosystem.

## Decision: Automated Testing & Deployment

*   **Choice**: GitHub Actions for CI/CD
*   **Rationale**: GitHub Actions provides a robust and integrated solution for automating build, test, and deployment workflows directly within the GitHub repository. This supports continuous integration for code examples and continuous deployment to GitHub Pages for the textbook website, ensuring that content is always up-to-date and functional. This directly addresses the "Deployment Excellence" principle.
*   **Alternatives Considered**:
    *   Jenkins: Powerful, but requires setting up and managing a separate server, adding complexity.
    *   Other cloud CI/CD services: GitHub Actions offers tight integration with the chosen code hosting platform.
