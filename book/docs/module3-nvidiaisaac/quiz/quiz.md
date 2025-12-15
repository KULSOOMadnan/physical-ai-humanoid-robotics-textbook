---
id: module3-quiz
title: Module 3 Quiz - Computer Vision & AI-Robot Brain
sidebar_label: Module 3 Quiz
module: "Module 3: The AI-Robot Brain (NVIDIA Isaac™)"
---

# Module 3 Quiz: Computer Vision Techniques Relevant to Robotics

import { Quiz } from '@site/src/components';

<Quiz
  title="Module 3 Quiz: Computer Vision Techniques Relevant to Robotics"
  questions={[
    {
      id: 1,
      question: "What is the main difference between robot vision and basic computer vision?",
      options: [
        "Robot vision is faster",
        "Robot vision incorporates the robot's spatial context, sensor configuration, and task requirements",
        "Robot vision uses different cameras",
        "Robot vision is more expensive"
      ],
      correctAnswer: 1,
      explanation: "Robot vision extends basic computer vision by incorporating the robot's spatial context, sensor configuration, and task requirements."
    },
    {
      id: 2,
      question: "What does the pinhole camera model describe?",
      options: [
        "How to build a camera",
        "The basic mathematical model describing how a 3D world is projected onto a 2D camera image",
        "How to calibrate a camera",
        "The internal components of a camera"
      ],
      correctAnswer: 1,
      explanation: "The pinhole camera model is the basic mathematical model describing how a 3D world is projected onto a 2D camera image."
    },
    {
      id: 3,
      question: "What are intrinsic parameters in camera calibration?",
      options: [
        "The camera's position in the world",
        "The camera's orientation relative to a world coordinate system",
        "Internal camera properties like focal length and principal point",
        "The type of lens used"
      ],
      correctAnswer: 2,
      explanation: "Intrinsic parameters are internal camera properties like focal length and principal point (center of the image)."
    },
    {
      id: 4,
      question: "Which color space is often more suitable for color-based segmentation?",
      options: [
        "RGB",
        "HSV",
        "CMYK",
        "LAB"
      ],
      correctAnswer: 1,
      explanation: "HSV color space is often more suitable for color-based segmentation tasks compared to RGB."
    },
    {
      id: 5,
      question: "What is the main advantage of YOLO (You Only Look Once) in object detection?",
      options: [
        "Highest accuracy",
        "Best for small objects",
        "Fast, single-shot detection that predicts bounding boxes and class probabilities directly from the full image",
        "Uses the least computational power"
      ],
      correctAnswer: 2,
      explanation: "YOLO is a fast, single-shot detector that predicts bounding boxes and class probabilities directly from the full image."
    },
    {
      id: 6,
      question: "What does a disparity map represent in stereo vision?",
      options: [
        "The color differences between images",
        "The difference in pixel locations of corresponding points in the left and right images to infer depth",
        "The brightness differences",
        "The size differences between objects"
      ],
      correctAnswer: 1,
      explanation: "A disparity map calculates the difference in pixel locations of corresponding points in the left and right images to infer depth."
    },
    {
      id: 7,
      question: "What is an RGB-D camera?",
      options: [
        "A camera that uses RGB lighting",
        "A camera that provides both color (RGB) and depth (D) information simultaneously",
        "A camera with three different sensors",
        "A camera that can switch between RGB and grayscale modes"
      ],
      correctAnswer: 1,
      explanation: "RGB-D cameras provide both color (RGB) and depth (D) information simultaneously (e.g., Intel RealSense, Microsoft Kinect)."
    },
    {
      id: 8,
      question: "What is a point cloud in 3D vision?",
      options: [
        "A collection of 2D points on an image",
        "A collection of 3D points representing the surface of objects in the scene",
        "A type of camera sensor",
        "A method of image compression"
      ],
      correctAnswer: 1,
      explanation: "A point cloud is a collection of 3D points representing the surface of objects in the scene, derived from depth data."
    },
    {
      id: 9,
      question: "What is transfer learning in the context of computer vision?",
      options: [
        "Moving a model from one computer to another",
        "Using pre-trained models and fine-tuning them on robot-specific datasets",
        "Copying code between projects",
        "Transferring images between devices"
      ],
      correctAnswer: 1,
      explanation: "Transfer learning involves using pre-trained models (e.g., trained on ImageNet) and fine-tuning them on robot-specific datasets for better performance with less data."
    },
    {
      id: 10,
      question: "What is the primary purpose of visual servoing?",
      options: [
        "To improve camera quality",
        "To use visual feedback to control the robot's motion",
        "To store visual data",
        "To compress image files"
      ],
      correctAnswer: 1,
      explanation: "Visual servoing uses visual feedback to control the robot's motion, for example, to center an object in the camera view or reach towards it."
    },
    {
      id: 11,
      question: "Which Python library is specifically mentioned for computer vision tasks?",
      options: [
        "NumPy",
        "Matplotlib",
        "OpenCV",
        "SciPy"
      ],
      correctAnswer: 2,
      explanation: "OpenCV is specifically mentioned as a powerful library for computer vision tasks."
    },
    {
      id: 12,
      question: "What is the purpose of geometric transformations in image preprocessing?",
      options: [
        "To increase image brightness",
        "To add color to grayscale images",
        "To perform operations like cropping, resizing, rotation, and perspective correction to prepare images for analysis",
        "To compress images"
      ],
      correctAnswer: 2,
      explanation: "Geometric transformations include operations like cropping, resizing, rotation, and perspective correction to prepare images for analysis."
    },
    {
      id: 13,
      question: "Which of the following is a traditional approach to object detection?",
      options: [
        "YOLO",
        "R-CNN",
        "Template Matching",
        "SSD"
      ],
      correctAnswer: 2,
      explanation: "Template Matching is a traditional approach to object detection, while YOLO, R-CNN, and SSD are deep learning-based approaches."
    },
    {
      id: 14,
      question: "What is the role of coordinate frame transformations in robot vision?",
      options: [
        "To change the image resolution",
        "To convert object poses from the camera frame to the robot's base frame",
        "To improve image quality",
        "To store images in different formats"
      ],
      correctAnswer: 1,
      explanation: "Coordinate frame transformations convert object poses from the camera frame to the robot's base frame using transformation matrices."
    },
    {
      id: 15,
      question: "Which of the following is a deep learning architecture for image classification?",
      options: [
        "HOG",
        "SIFT",
        "CNN",
        "ORB"
      ],
      correctAnswer: 2,
      explanation: "Convolutional Neural Networks (CNNs) are the standard architecture for image classification and feature extraction in deep learning."
    }
  ]}
/>