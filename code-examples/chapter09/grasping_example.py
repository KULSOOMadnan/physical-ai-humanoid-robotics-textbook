"""
Simulated Grasping Example for Chapter 9

This script demonstrates basic grasping concepts for humanoid robots.
It simulates a simple 2D scenario where a robot hand attempts to
grasp an object, evaluating grasp stability based on geometric and
force-related criteria.
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial.distance import cdist
import math

class SimpleObject:
    """
    Represents a simple 2D object (e.g., a rectangle or circle) for grasping simulation.
    """
    def __init__(self, shape='rectangle', params=None):
        self.shape = shape
        if params is None:
            if shape == 'rectangle':
                params = {'width': 1.0, 'height': 0.5}  # Default rectangle
            elif shape == 'circle':
                params = {'radius': 0.5}  # Default circle
        self.params = params
        self.position = np.array([0.0, 0.0])  # Center position
        self.orientation = 0.0  # Orientation in radians

    def get_boundary_points(self, num_points=20):
        """Generate points along the object's boundary."""
        if self.shape == 'rectangle':
            w = self.params['width'] / 2
            h = self.params['height'] / 2
            # Define rectangle corners in object's local frame
            corners_local = np.array([
                [-w, -h], [w, -h], [w, h], [-w, h]
            ])
            # Interpolate points along edges
            points = []
            for i in range(4):
                p1 = corners_local[i]
                p2 = corners_local[(i + 1) % 4]
                for t in np.linspace(0, 1, num_points // 4, endpoint=False):
                    points.append(p1 + t * (p2 - p1))
            return np.array(points)
        elif self.shape == 'circle':
            r = self.params['radius']
            angles = np.linspace(0, 2*np.pi, num_points, endpoint=False)
            points = np.array([[r * np.cos(a), r * np.sin(a)] for a in angles])
            return points
        else:
            return np.array([[0, 0]])  # Default fallback

    def get_support_lines(self, num_lines=8):
        """Get lines across the object for grasp evaluation."""
        if self.shape == 'rectangle':
            w = self.params['width']
            h = self.params['height']
            lines = []
            # Horizontal lines
            for y in np.linspace(-h/2, h/2, num_lines//2):
                lines.append(([-w/2, y], [w/2, y]))
            # Vertical lines
            for x in np.linspace(-w/2, w/2, num_lines//2):
                lines.append(([x, -h/2], [x, h/2]))
            return lines
        elif self.shape == 'circle':
            r = self.params['radius']
            lines = []
            for angle in np.linspace(0, np.pi, num_lines):
                x1 = r * np.cos(angle)
                y1 = r * np.sin(angle)
                x2 = -x1
                y2 = -y1
                lines.append(([x1, y1], [x2, y2]))
            return lines
        else:
            return [([0, 0], [0, 0])]  # Fallback

class SimpleHand:
    """
    Represents a simple 2-fingered robotic hand for grasping simulation.
    """
    def __init__(self, finger_length=0.8, finger_width=0.1):
        self.finger_length = finger_length
        self.finger_width = finger_width
        self.position = np.array([0.0, 0.0])  # Palm position
        self.orientation = 0.0  # Hand orientation in radians
        self.aperture = 1.0  # Distance between finger tips

    def get_finger_positions(self):
        """Calculate the positions of the two finger tips based on aperture and orientation."""
        # Calculate finger positions relative to palm
        half_aperture = self.aperture / 2
        # Finger 1 (positive direction relative to orientation)
        f1_local = np.array([half_aperture, 0])
        # Finger 2 (negative direction)
        f2_local = np.array([-half_aperture, 0])

        # Rotate based on hand orientation
        cos_theta = np.cos(self.orientation)
        sin_theta = np.sin(self.orientation)
        R = np.array([[cos_theta, -sin_theta], [sin_theta, cos_theta]])

        f1_world = self.position + R @ f1_local
        f2_world = self.position + R @ f2_local

        return f1_world, f2_world

    def get_hand_outline(self):
        """Get points representing the hand's outline for visualization."""
        # Simplified representation: two fingers and a palm
        f1, f2 = self.get_finger_positions()
        # Vector from f2 to f1
        vec = f1 - f2
        perp = np.array([-vec[1], vec[0]])  # Perpendicular vector
        perp_norm = perp / np.linalg.norm(perp) * self.finger_width

        # Points for finger 1
        f1_points = [
            f1,
            f1 + perp_norm,
            f1 - perp_norm
        ]
        # Points for finger 2
        f2_points = [
            f2,
            f2 + perp_norm,
            f2 - perp_norm
        ]
        # Connect fingers with a simple palm representation
        palm_points = [f1, f2]  # Simplified palm as a line between fingers

        return f1_points + f2_points + palm_points

def evaluate_grasp_quality(object_shape, hand):
    """
    Evaluate the quality of a grasp based on geometric criteria.
    This is a simplified model focusing on grasp width and object size.
    """
    f1_pos, f2_pos = hand.get_finger_positions()
    grasp_width = np.linalg.norm(f1_pos - f2_pos)

    # Object size approximation (for simple shapes)
    if object_shape.shape == 'rectangle':
        obj_size = max(object_shape.params['width'], object_shape.params['height'])
    elif object_shape.shape == 'circle':
        obj_size = 2 * object_shape.params['radius']
    else:
        obj_size = 1.0  # Default

    # Check if grasp width is appropriate
    min_grasp_width = obj_size * 0.5
    max_grasp_width = obj_size * 2.0

    if min_grasp_width <= grasp_width <= max_grasp_width:
        # Calculate grasp quality based on how well fingers align with object
        obj_boundary = object_shape.get_boundary_points()
        f1_to_obj = cdist([f1_pos], obj_boundary, 'euclidean').min()
        f2_to_obj = cdist([f2_pos], obj_boundary, 'euclidean').min()

        # A simple quality metric: closer fingers to object boundary is better
        # but not too close to avoid collision
        ideal_distance = 0.05  # Ideal distance from finger to object
        dist1_error = abs(f1_to_obj - ideal_distance)
        dist2_error = abs(f2_to_obj - ideal_distance)

        # Normalize error (lower is better)
        max_error = 0.5  # Assume max relevant error
        quality = 1.0 - min((dist1_error + dist2_error) / 2, max_error) / max_error
        quality = max(0.0, min(1.0, quality))  # Clamp to [0, 1]

        return quality
    else:
        return 0.0  # Grasp width inappropriate

def simulate_grasping_attempt():
    """
    Simulates a humanoid robot attempting to grasp an object.
    This involves positioning the hand, evaluating grasp quality,
    and simulating the outcome.
    """
    print("Simulating humanoid robot grasping attempt...")

    # Step 1: Define object
    print("1. Defining object to grasp...")
    obj = SimpleObject(shape='rectangle', params={'width': 0.8, 'height': 0.4})
    obj.position = np.array([2.0, 0.0])  # Place object at (2, 0)
    print(f"   Object: {obj.shape} with params {obj.params}")
    print(f"   Object position: {obj.position}")

    # Step 2: Define hand and initial position
    print("2. Positioning robotic hand...")
    hand = SimpleHand(finger_length=0.8, finger_width=0.1)
    hand.position = np.array([0.0, 0.0])  # Start at origin
    hand.orientation = 0.0  # Initially aligned with x-axis
    hand.aperture = 1.0  # Initial finger aperture

    # Visualize initial state
    plt.figure(figsize=(12, 6))

    # Subplot 1: Initial state
    plt.subplot(1, 2, 1)
    obj_boundary = obj.get_boundary_points()
    plt.plot(obj_boundary[:, 0] + obj.position[0], obj_boundary[:, 1] + obj.position[1], 'b-', label='Object')

    hand_outline = hand.get_hand_outline()
    hand_x = [p[0] for p in hand_outline]
    hand_y = [p[1] for p in hand_outline]
    plt.plot(hand_x, hand_y, 'r-', label='Hand (Initial)')

    plt.plot(obj.position[0], obj.position[1], 'bo', markersize=10, label='Object Center')
    plt.plot(hand.position[0], hand.position[1], 'ro', markersize=10, label='Hand Palm')

    plt.title("Initial State: Object and Hand Position")
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.axis('equal')

    # Step 3: Plan grasp (simplified: move hand to object, adjust aperture)
    print("3. Planning grasp approach...")
    # Move hand to object location (simplified linear approach)
    approach_offset = 0.5  # Distance from object center to grasp point
    grasp_pos = obj.position + np.array([0, 0])  # Grasp at object center for simplicity
    hand.position = grasp_pos + np.array([-approach_offset, 0])  # Approach from -X direction

    # Adjust aperture based on object size
    if obj.shape == 'rectangle':
        obj_size = max(obj.params['width'], obj.params['height'])
    elif obj.shape == 'circle':
        obj_size = 2 * obj.params['radius']
    else:
        obj_size = 1.0

    hand.aperture = obj_size * 0.8  # Slightly larger than object

    print(f"   Planned hand position: {hand.position}")
    print(f"   Planned hand aperture: {hand.aperture:.2f}")

    # Subplot 2: Grasp attempt
    plt.subplot(1, 2, 2)
    obj_boundary = obj.get_boundary_points()
    plt.plot(obj_boundary[:, 0] + obj.position[0], obj_boundary[:, 1] + obj.position[1], 'b-', label='Object')

    hand_outline = hand.get_hand_outline()
    hand_x = [p[0] for p in hand_outline]
    hand_y = [p[1] for p in hand_outline]
    plt.plot(hand_x, hand_y, 'r-', label='Hand (Grasp Position)')

    plt.plot(obj.position[0], obj.position[1], 'bo', markersize=10, label='Object Center')
    plt.plot(hand.position[0], hand.position[1], 'ro', markersize=10, label='Hand Palm')

    # Draw line representing grasp width
    f1_pos, f2_pos = hand.get_finger_positions()
    plt.plot([f1_pos[0], f2_pos[0]], [f1_pos[1], f2_pos[1]], 'g--', linewidth=2, label=f'Grasp Width: {hand.aperture:.2f}')

    plt.title("Grasp Attempt: Hand Positioned for Grasp")
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.axis('equal')

    plt.tight_layout()
    plt.show()

    # Step 4: Evaluate grasp quality
    print("4. Evaluating grasp quality...")
    quality = evaluate_grasp_quality(obj, hand)
    print(f"   Grasp quality score: {quality:.2f} (0.0 = poor, 1.0 = excellent)")

    # Step 5: Simulate grasp outcome
    print("5. Simulating grasp outcome...")
    if quality > 0.5:
        print("   Grasp successful! Object secured between fingers.")
        print("   Robot can now manipulate the object.")
        success = True
    else:
        print("   Grasp failed! Object not securely held.")
        if hand.aperture > obj_size * 1.5:
            print("   Reason: Hand aperture too wide.")
        elif hand.aperture < obj_size * 0.5:
            print("   Reason: Hand aperture too narrow.")
        else:
            print("   Reason: Hand position/orientation not optimal for stable grasp.")
        success = False

    # Additional analysis: Show support lines for grasp
    print("6. Analyzing grasp stability (simplified)...")
    support_lines = obj.get_support_lines(num_lines=6)
    f1_pos, f2_pos = hand.get_finger_positions()

    # Count how many support lines are "supported" by fingers
    supported_lines = 0
    for line_start, line_end in support_lines:
        # Transform line to world coordinates
        line_start_world = np.array(line_start) + obj.position
        line_end_world = np.array(line_end) + obj.position

        # Check if line is "supported" by fingers (simplified: if fingers are on opposite sides)
        # This is a very basic check
        line_vec = line_end_world - line_start_world
        perp_vec = np.array([-line_vec[1], line_vec[0]])  # Perpendicular to line
        f1_to_line = np.dot(f1_pos - line_start_world, perp_vec)
        f2_to_line = np.dot(f2_pos - line_start_world, perp_vec)

        if f1_to_line * f2_to_line < 0:  # Fingers on opposite sides of the line
            supported_lines += 1

    print(f"   Number of support lines with opposing fingers: {supported_lines}/6")
    print(f"   This indicates potential grasp stability.")

    print("\nGrasping simulation complete.")
    print("This example demonstrates key concepts in robotic grasping:")
    print("- Positioning the hand relative to the object")
    print("- Adjusting hand aperture for object size")
    print("- Evaluating grasp quality based on geometric factors")
    print("- Assessing potential stability of the grasp")
    print("Real humanoid robots use more sophisticated models incorporating")
    print("tactile feedback, dynamic forces, and complex hand kinematics.")

def main():
    simulate_grasping_attempt()

if __name__ == "__main__":
    main()
