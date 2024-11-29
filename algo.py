import heapq
from collections import deque  # For BFS
import time

execution_time = 0

# BFS Algorithm
def bfs(grid, start, target):

    start_time = time.time()
    rows, cols = len(grid), len(grid[0])
    visited = set()
    queue = deque([(start, [])])  # (current_position, path)
    print(f"Starting BFS from {start} to {target}")  # Debugging line
    visiting_nodes = []

    while queue:
        current, path = queue.popleft()

        if current in visited:
            continue
        visited.add(current)
        visiting_nodes.append(current)

        if current == target:
            end_time = time.time()
            execution_time = end_time - start_time
            print(f"BFS execution time: {execution_time} seconds")
            return path, visiting_nodes

        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            x, y = current[0] + dx, current[1] + dy
            if 0 <= x < rows and 0 <= y < cols and grid[x][y] != -1:  # -1 represents obstacles
                queue.append(((x, y), path + [(x, y)]))

    print("No path found!")  # Debugging line
    end_time = time.time()
    execution_time = end_time - start_time
    print(f"BFS execution time: {execution_time} seconds")
    return None, visiting_nodes

# DFS Algorithm (Implemented with Stack)
def dfs (grid, start, target):
    start_time = time.time()
    rows, cols = len(grid), len(grid[0])
    visited = set()
    stack = [(start, [])]  # (current_position, path)
    visiting_nodes = []

    while stack:
        current, path = stack.pop()

        if current in visited:
            continue
        visited.add(current)
        visiting_nodes.append(current)

        if current == target:
            end_time = time.time()
            execution_time = end_time - start_time
            print(f"DFS execution time: {execution_time} seconds")
            return path, visiting_nodes

        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            x, y = current[0] + dx, current[1] + dy
            if 0 <= x < rows and 0 <= y < cols and grid[x][y] != -1:  # -1 represents obstacles
                stack.append(((x, y), path + [(x, y)]))

    end_time = time.time()
    execution_time = end_time - start_time
    print(f"DFS execution time: {execution_time} seconds")
    return None, visiting_nodes

# UCS Algorithm
def ucs(grid, start, target):
    # Start time
   
    start_time = time.time()
    rows, cols = len(grid), len(grid[0])
    visited = set()
    queue = []
    heapq.heappush(queue, (0, start, []))  # (cost, current_position, path)

    
    print(f"Starting UCS from {start} to {target}")  # Debugging line
    visiting_nodes = []

    while queue:
        current_cost, current, path = heapq.heappop(queue)

        # Debugging line to trace the path
        print(f"Visiting {current} with cost {current_cost}, current path: {path}")

        if current in visited:
            continue
        visited.add(current)
        visiting_nodes.append(current)

        if current == target:
            end_time = time.time()
            execution_time = end_time - start_time
            print(f"UCS execution time: {execution_time} seconds")
            return path, visiting_nodes, current_cost

        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            x, y = current[0] + dx, current[1] + dy
            if 0 <= x < rows and 0 <= y < cols:
                cell_value = grid[x][y]
                if cell_value != -1 and (x,y) not in visited:  # Avoid obstacles
                    if isinstance(cell_value, int):  # Ensure the cell value is an integer
                        new_cost = current_cost + cell_value
                        heapq.heappush(queue, (new_cost, (x, y), path + [(x, y)]))

    print("No path found!")  # Debugging line
    end_time = time.time()
    execution_time = end_time - start_time
    print(f"UCS execution time: {execution_time} seconds")
    return None, visiting_nodes, None

# Depth-Limited Search (DLS) Algorithm
def dls(grid, start, target, limit):
    start_time = time.time()
    rows, cols = len(grid), len(grid[0])
    visited = set()
    visiting_nodes = []
    
    def recursive_dls(node, depth, path):
        if depth > limit:
            return None  # Exceeded the depth limit
        if node in visited:
            return None  # Already visited
        if node == target:
            return path  # Target found

        visited.add(node)
        visiting_nodes.append(node)

        # Explore neighbors
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            x, y = node[0] + dx, node[1] + dy
            if 0 <= x < rows and 0 <= y < cols and not grid[x][y]:  # Assuming 0 means valid cell
                result = recursive_dls((x, y), depth + 1, path + [(x, y)])
                if result:
                    return result  # Return as soon as a path is found

        # Backtrack: remove from visited if this path doesn't work
        visited.remove(node)
        return None  # No path found from this node

    # Start the recursive search
    path = recursive_dls(start, 0, [start])
    end_time = time.time()
    execution_time = end_time - start_time
    print(f"DLS execution time: {execution_time} seconds")
    return path or [], visiting_nodes


