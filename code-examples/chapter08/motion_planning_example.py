"""
Simulated Motion Planning Example for Chapter 8

This script demonstrates basic motion planning concepts for humanoid robots,
specifically focusing on obstacle avoidance using a grid-based A* algorithm.
It simulates a 2D top-down view of the environment where the robot needs
to find a path from a start point to a goal point while avoiding obstacles.
"""

import numpy as np
import matplotlib.pyplot as plt
from heapq import heappush, heappop
import math

class GridEnvironment:
    """
    Represents a 2D grid environment for motion planning.
    0 = free space, 1 = obstacle.
    """
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.grid = np.zeros((height, width), dtype=int)

    def add_obstacle(self, x, y):
        """Add a single obstacle cell."""
        if 0 <= x < self.width and 0 <= y < self.height:
            self.grid[y, x] = 1

    def add_obstacle_rectangle(self, x_min, y_min, x_max, y_max):
        """Add a rectangular obstacle."""
        for y in range(max(0, y_min), min(self.height, y_max + 1)):
            for x in range(max(0, x_min), min(self.width, x_max + 1)):
                self.grid[y, x] = 1

    def is_free(self, x, y):
        """Check if a cell is free (not an obstacle)."""
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.grid[y, x] == 0
        return False  # Out of bounds considered occupied

    def get_neighbors(self, x, y):
        """Get 8-connected neighbors of a cell."""
        neighbors = []
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue  # Skip the cell itself
                nx, ny = x + dx, y + dy
                if self.is_free(nx, ny):
                    # Add cost based on movement type (diagonal vs straight)
                    cost = math.sqrt(2) if dx != 0 and dy != 0 else 1.0
                    neighbors.append((nx, ny, cost))
        return neighbors

def heuristic(a, b):
    """Euclidean distance heuristic for A*."""
    return math.sqrt((a[0] - b[0])**2 + (a[1] - b[1])**2)

def a_star(grid_env, start, goal):
    """
    A* pathfinding algorithm implementation.
    """
    open_set = []
    heappush(open_set, (0, start))

    came_from = {}
    g_score = {start: 0}
    f_score = {start: heuristic(start, goal)}

    while open_set:
        current = heappop(open_set)[1]

        if current == goal:
            # Reconstruct path
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            path.reverse()
            return path

        for neighbor_x, neighbor_y, move_cost in grid_env.get_neighbors(current[0], current[1]):
            neighbor = (neighbor_x, neighbor_y)
            tentative_g_score = g_score[current] + move_cost

            if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = tentative_g_score + heuristic(neighbor, goal)
                heappush(open_set, (f_score[neighbor], neighbor))

    return None  # No path found

def simulate_humanoid_path_planning():
    """
    Simulates a humanoid robot planning a path in a 2D environment.
    This represents a simplified version of how a robot might plan
    to navigate around obstacles in its environment.
    """
    print("Simulating humanoid robot motion planning with obstacle avoidance...")

    # Step 1: Define environment
    print("1. Setting up environment...")
    env = GridEnvironment(width=20, height=20)

    # Add some obstacles to create a challenging path
    env.add_obstacle_rectangle(5, 5, 8, 15)  # Vertical wall
    env.add_obstacle_rectangle(12, 8, 18, 11)  # Horizontal wall
    env.add_obstacle_rectangle(10, 15, 13, 18)  # Small box near goal

    start = (2, 2)
    goal = (18, 18)

    print(f"   Environment size: {env.width}x{env.height}")
    print(f"   Start position: {start}")
    print(f"   Goal position: {goal}")

    # Step 2: Plan path using A*
    print("2. Planning path using A* algorithm...")
    path = a_star(env, start, goal)

    if path:
        print(f"   Path found with {len(path)} waypoints.")
        print(f"   First few waypoints: {path[:5]}")
        print(f"   Last few waypoints: {path[-5:]}")
    else:
        print("   No path found to goal!")
        return

    # Step 3: Visualize the result
    print("3. Visualizing path planning result...")

    # Create a visualization grid
    viz_grid = env.grid.copy().astype(float)
    viz_grid[viz_grid == 0] = 0.5  # Free space
    viz_grid[viz_grid == 1] = 1.0  # Obstacles

    # Mark the path
    for x, y in path:
        if viz_grid[y, x] == 0.5:  # Only mark free space, not obstacles
            viz_grid[y, x] = 0.2  # Path

    # Mark start and goal
    viz_grid[start[1], start[0]] = 0.0  # Start (black)
    viz_grid[goal[1], goal[0]] = 0.8   # Goal (dark gray)

    plt.figure(figsize=(10, 10))
    plt.imshow(viz_grid, cmap='gray', origin='upper')

    # Plot the path as a line
    path_x = [p[0] for p in path]
    path_y = [p[1] for p in path]
    plt.plot(path_x, path_y, 'b-', linewidth=2, label='Planned Path')

    # Mark start and goal
    plt.plot(start[0], start[1], 'go', markersize=10, label='Start')
    plt.plot(goal[0], goal[1], 'ro', markersize=10, label='Goal')

    plt.title("Humanoid Robot Motion Planning: Obstacle Avoidance\n(A* Pathfinding)")
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.legend()
    plt.grid(True, color='gray', linestyle='--', alpha=0.6)
    plt.show()

    # Step 4: Analyze path characteristics
    print("4. Analyzing path characteristics...")

    # Calculate path length
    total_length = 0.0
    for i in range(1, len(path)):
        dx = path[i][0] - path[i-1][0]
        dy = path[i][1] - path[i-1][1]
        move_dist = math.sqrt(dx**2 + dy**2)
        total_length += move_dist

    print(f"   Total path length: {total_length:.2f} units")
    print(f"   Number of turns/direction changes: {len(path)}")

    # Check if path goes around obstacles
    # (This is a simple check; in a real scenario, we'd have more complex analysis)
    path_around_obstacles = any(
        5 <= x <= 8 and 5 <= y <= 15 for x, y in path  # Near the vertical wall
    ) or any(
        12 <= x <= 18 and 8 <= y <= 11 for x, y in path  # Near the horizontal wall
    )

    if path_around_obstacles:
        print("   Path successfully avoids obstacles.")
    else:
        print("   Path may not adequately avoid obstacles (check implementation).")

    print("\nMotion planning simulation complete.")
    print("This example demonstrates how a robot might plan a collision-free path")
    print("from its current location to a goal, a fundamental skill for navigation.")
    print("In real humanoid robots, this planning would consider 3D space,")
    print("robot kinematics, balance constraints, and dynamic obstacles.")

def main():
    simulate_humanoid_path_planning()

if __name__ == "__main__":
    main()
