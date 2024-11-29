class Grid:
    def __init__(self, rows, cols):   #10 , 10
        self.rows = rows
        self.cols = cols
        self.grid = [[0 for _ in range(cols)] for _ in range(rows)]  # 0 = empty, -1 = obstacle, 10 = high cost
        self.start = None
        self.target = (4,4)

    def set_obstacle(self, x, y):
        if 0 <= x < self.rows and 0 <= y < self.cols:
            if (x, y) != self.start and (x, y) != self.target:
                self.grid[x][y] = -1
                print(f"Obstacle set at: ({x}, {y})")
        else:
            print(f"Invalid coordinates: ({x}, {y})")

    def set_start(self, x, y):
        if not self.is_obstacle(x, y) and not self.is_high_cost(x, y):
            self.start = (x, y)
        else:
            print("Cannot set start on an obstacle or high-cost cell.")

    def set_high_cost(self, x, y):
        if (x, y) != self.start and (x, y) != self.target:  # Prevent setting high-cost on start or target
            self.grid[x][y] = 10  # Set high cost value to 10
            print(f"High-cost set at: ({x}, {y})")  # Debugging line

    def is_obstacle(self, x, y):
        return self.grid[x][y] == -1  # Check if cell is an obstacle

    def is_high_cost(self, x, y):
        return self.grid[x][y] == 10  # Check if cell is high cost
    
    def print_grid(self):
        for row in self.grid:
            print(row)
        print("\n")  # Separate prints for better readability


   