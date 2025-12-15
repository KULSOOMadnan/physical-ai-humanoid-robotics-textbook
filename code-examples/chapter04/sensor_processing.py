"""
Simulated Sensor Data Processing Example for Chapter 4

This script demonstrates basic computer vision processing techniques
relevant to robotics, such as object detection and feature extraction.
It uses OpenCV for image processing and NumPy for numerical operations.
"""

import numpy as np
import cv2
import matplotlib.pyplot as plt

def simulate_camera_image(width=640, height=480, num_objects=3):
    """
    Simulates a camera image with simple geometric shapes as objects.
    This represents the 'raw' sensor data from a robot's camera.
    """
    # Create a blank image
    image = np.ones((height, width, 3), dtype=np.uint8) * 255  # White background

    # Define colors for objects
    colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 0, 255)]

    # Draw random shapes (objects) on the image
    for i in range(num_objects):
        color = colors[i % len(colors)]
        center_x = np.random.randint(50, width - 50)
        center_y = np.random.randint(50, height - 50)
        size = np.random.randint(20, 60)

        shape_type = np.random.randint(0, 3)
        if shape_type == 0:  # Circle
            cv2.circle(image, (center_x, center_y), size, color, -1)
        elif shape_type == 1:  # Rectangle
            pt1 = (center_x - size, center_y - size)
            pt2 = (center_x + size, center_y + size)
            cv2.rectangle(image, pt1, pt2, color, -1)
        else:  # Triangle
            points = np.array([
                [center_x, center_y - size],
                [center_x - size, center_y + size],
                [center_x + size, center_y + size]
            ], np.int32)
            cv2.fillPoly(image, [points], color)

    return image

def detect_objects(image):
    """
    A simple object detection function using color-based segmentation.
    This simulates how a robot might identify objects in its visual field.
    """
    # Convert to HSV for easier color segmentation
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Define color ranges for the objects we created (simplified)
    # In a real scenario, this would be more complex or use deep learning
    lower_red = np.array([0, 50, 50])
    upper_red = np.array([10, 255, 255])
    lower_green = np.array([50, 50, 50])
    upper_green = np.array([70, 255, 255])
    lower_blue = np.array([110, 50, 50])
    upper_blue = np.array([130, 255, 255])

    # Create masks for each color
    mask_red = cv2.inRange(hsv, lower_red, upper_red)
    mask_green = cv2.inRange(hsv, lower_green, upper_green)
    mask_blue = cv2.inRange(hsv, lower_blue, upper_blue)

    # Combine masks
    combined_mask = mask_red + mask_green + mask_blue

    # Find contours of objects
    contours, _ = cv2.findContours(combined_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Filter out small contours (noise)
    min_area = 100
    filtered_contours = [cnt for cnt in contours if cv2.contourArea(cnt) > min_area]

    return filtered_contours

def analyze_object_features(contours, image):
    """
    Analyze features of detected objects, such as position and size.
    This information could be used for manipulation planning.
    """
    object_data = []

    for i, cnt in enumerate(filtered_contours):
        # Calculate bounding box
        x, y, w, h = cv2.boundingRect(cnt)

        # Calculate center of mass
        M = cv2.moments(cnt)
        if M["m00"] != 0:
            cx = int(M["m10"] / M["m00"])
            cy = int(M["m01"] / M["m00"])
        else:
            cx, cy = x + w//2, y + h//2  # Fallback to center of bounding box

        # Approximate contour to get shape characteristics
        epsilon = 0.04 * cv2.arcLength(cnt, True)
        approx = cv2.approxPolyDP(cnt, epsilon, True)
        num_vertices = len(approx)

        # Estimate object type based on vertices
        if num_vertices == 4:
            # Check if it's more like a square or rectangle
            aspect_ratio = float(w) / h
            if 0.75 <= aspect_ratio <= 1.25:
                shape_type = "Square"
            else:
                shape_type = "Rectangle"
        elif num_vertices == 3:
            shape_type = "Triangle"
        else:
            shape_type = "Circle/Ellipse"

        object_info = {
            'id': i,
            'center': (cx, cy),
            'bbox': (x, y, w, h),
            'size': w * h,  # Approximate size
            'shape_type': shape_type,
            'vertices': num_vertices
        }

        object_data.append(object_info)

    return object_data

def main():
    print("Simulating robot camera data processing...")

    # Step 1: Simulate camera image (raw sensor data)
    print("1. Capturing simulated image from robot camera...")
    simulated_image = simulate_camera_image()
    print(f"   Captured image of size: {simulated_image.shape}")

    # Step 2: Detect objects in the image
    print("2. Detecting objects in the image...")
    contours = detect_objects(simulated_image)
    print(f"   Detected {len(contours)} potential objects.")

    # Step 3: Analyze features of detected objects
    print("3. Analyzing object features...")
    object_features = analyze_object_features(contours, simulated_image)

    print(f"   Analyzed {len(object_features)} objects with the following features:")
    for obj in object_features:
        print(f"      - Object {obj['id']}: {obj['shape_type']}, "
              f"Center: {obj['center']}, Size: {obj['size']:.0f} px², "
              f"Vertices: {obj['vertices']}")

    # Step 4: Visualize results
    print("4. Visualizing results...")
    result_image = simulated_image.copy()

    # Draw bounding boxes and centers
    for obj in object_features:
        x, y, w, h = obj['bbox']
        cx, cy = obj['center']

        # Draw bounding box
        cv2.rectangle(result_image, (x, y), (x + w, y + h), (0, 0, 0), 2)

        # Draw center point
        cv2.circle(result_image, (cx, cy), 5, (0, 0, 0), -1)

        # Add label
        label = f"{obj['shape_type']}"
        cv2.putText(result_image, label, (x, y - 10),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)

    # Display original and processed images
    plt.figure(figsize=(12, 5))

    plt.subplot(1, 2, 1)
    plt.imshow(cv2.cvtColor(simulated_image, cv2.COLOR_BGR2RGB))
    plt.title("Original Simulated Image")
    plt.axis('off')

    plt.subplot(1, 2, 2)
    plt.imshow(cv2.cvtColor(result_image, cv2.COLOR_BGR2RGB))
    plt.title("Processed Image (Detected Objects)")
    plt.axis('off')

    plt.tight_layout()
    plt.show()

    print("\nSensor data processing simulation complete.")
    print("This example demonstrates how a robot might process")
    print("visual sensor data to identify and characterize objects")
    print("in its environment, which is crucial for tasks like")
    print("object manipulation and navigation.")

if __name__ == "__main__":
    main()
