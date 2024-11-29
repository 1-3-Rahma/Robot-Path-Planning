import tkinter as tk
from tkinter import Canvas
from grid import Grid
from algo import ucs, bfs, dfs , dls
from tkinter import PhotoImage
import time , sys

class PathfindingApp:
    def __init__(self, rows, cols, cell_size):
        self.rows = rows
        self.cols = cols
        self.cell_size = cell_size
        self.grid = Grid(rows, cols)
        self.algorithm = None
        self.path = []
        self.visiting_nodes = []
        self.depth_limit = 0
      
        

        # Create the main tkinter window
        self.root = tk.Tk()
        self.root.title("Robot Path Planning")

        # Canvas for drawing the grid
        self.canvas = tk.Canvas(self.root, width=cols * cell_size, height=rows * cell_size)
        self.canvas.pack()

        # Frame for buttons
        self.button_frame = tk.Frame(self.root)
        self.button_frame.pack()

        # Add buttons
        self.bfs_button = tk.Button(self.button_frame, text="BFS", command=lambda: self.set_algorithm("BFS"))
        self.bfs_button.grid(row=0, column=0, padx=10, pady=10)

        self.dfs_button = tk.Button(self.button_frame, text="DFS", command=lambda: self.set_algorithm("DFS"))
        self.dfs_button.grid(row=0, column=1, padx=10, pady=10)

        self.ucs_button = tk.Button(self.button_frame, text="UCS", command=lambda: self.set_algorithm("UCS"))
        self.ucs_button.grid(row=0, column=2, padx=10, pady=10)

        self.high_cost_button = tk.Button(self.button_frame, text="High Cost", command=self.set_high_cost, state=tk.DISABLED)
        self.high_cost_button.grid(row=0, column=3, padx=10, pady=10)
        
        self.dls_button = tk.Button(self.button_frame, text ="DLS", command=lambda: self.set_algorithm("DLS"))
        self.dls_button.grid(row=0, column=4, padx=10, pady=10)

        # Label to display the current depth limit
        self.limit_label = tk.Label(self.button_frame, text=f"Limit: {self.depth_limit}" , state=tk.DISABLED)
        self.limit_label.grid(row=0, column=5, padx=5, pady=10)

        # Buttons to increase and decrease the depth limit
        self.increase_limit_button = tk.Button(self.button_frame, text="+", command=self.increase_limit , state=tk.DISABLED)
        self.increase_limit_button.grid(row=0, column=6, padx=10, pady=10)

        self.decrease_limit_button = tk.Button(self.button_frame, text="-", command=self.decrease_limit , state=tk.DISABLED)
        self.decrease_limit_button.grid(row=0, column=7, padx=10, pady=10)

        self.start_button = tk.Button(self.button_frame, text="Start", command=self.run_algorithm)
        self.start_button.grid(row=0, column=8, padx=10, pady=10)

        # Add Reset button to the button frame
        self.reset_button = tk.Button(self.button_frame, text="Reset", command=self.reset_grid)
        self.reset_button.grid(row=0, column=9, padx=10, pady=10)

        # Add Start Point button
        self.start_point_button = tk.Button(self.button_frame, text="Set Start Point", command=self.set_start_point)
        self.start_point_button.grid(row=0, column=10, padx=10, pady=10)
        # Add Reset all
        self.resetall_button = tk.Button(self.button_frame, text="ResetAll", command=self.resetall_grid)
        self.resetall_button.grid(row=0, column=11, padx=10, pady=10)


        # Bind left mouse click for grid interactions
        self.canvas.bind("<Button-1>", self.handle_grid_click)

        # Load and resize images for the path and obstacles
        self.path_image = PhotoImage(file="robot.png")
        self.obs_image = PhotoImage(file="bomb.png")

        # Resize the image to fit the cell size
        self.path_image = self.path_image.subsample(int(self.path_image.width() / self.cell_size), 
                                                     int(self.path_image.height() / self.cell_size))
        self.obs_image = self.obs_image.subsample(int(self.obs_image.width() / self.cell_size), 
                                                 int(self.obs_image.height() / self.cell_size))
        
        self.draw_grid()

    def increase_limit(self):
        """Increase the depth limit and update the label."""
        self.depth_limit += 1
        self.limit_label.config(text=f"Limit: {self.depth_limit}")
       
    def decrease_limit(self):
        """Decrease the depth limit and update the label."""
        if self.depth_limit > 0:  # Ensure limit doesn't go below zero
            self.depth_limit -= 1
            self.limit_label.config(text=f"Limit: {self.depth_limit}")

    def draw_grid(self):
        """Draw the grid on the canvas."""
        self.canvas.delete("all")  # Clear the canvas
        for x in range(self.rows):
            for y in range(self.cols):
                cell = self.grid.grid[x][y]
                color = "white"  # Default color for empty cells

                if (x, y) == self.grid.start:
                    color = "green"  # Start point
                elif (x, y) == self.grid.target:
                    color = "red"  # Target point
                elif cell == -1:  # Obstacles
                    self.canvas.create_image(
                        y * self.cell_size, x * self.cell_size,
                        anchor=tk.NW, image=self.obs_image
                    )                              
                elif cell == 10:
                    color = "orange"  # High-cost cells

                # Draw each cell as a rectangle
                if cell != -1:  # Don't draw rectangles for obstacles, only for other cells
                    self.canvas.create_rectangle(
                        y * self.cell_size, x * self.cell_size,
                        (y + 1) * self.cell_size, (x + 1) * self.cell_size,
                        fill=color, outline="gray"
                    )
  
    def set_start_point(self):
        """Bind click event to set the start point."""
        self.canvas.bind("<Button-1>", self.set_start_point_cell)

    def set_start_point_cell(self, event):
        """Set the start point on the grid."""
        grid_x = event.y // self.cell_size
        grid_y = event.x // self.cell_size

        # Remove existing start point if any
        if self.grid.start:
            old_x, old_y = self.grid.start
            self.grid.grid[old_x][old_y] = 0  # Reset to empty cell

        # Set the new start point
        self.grid.start = (grid_x, grid_y)
        self.grid.grid[grid_x][grid_y] = "start"
        self.draw_grid()
        self.canvas.unbind("<Button-1>")  # Unbind after setting the point

    def set_algorithm(self, algorithm):
        """Set the selected algorithm and enable/disable high cost button."""
        self.algorithm = algorithm
        self.high_cost_button.config(state=tk.NORMAL if algorithm == "UCS" else tk.DISABLED)
        self.limit_label.config(state=tk.NORMAL if algorithm == "DLS" else tk.DISABLED)
        self.increase_limit_button.config(state=tk.NORMAL if algorithm == "DLS" else tk.DISABLED)
        self.decrease_limit_button.config(state=tk.NORMAL if algorithm == "DLS" else tk.DISABLED)

    def set_high_cost(self):
        """Set high-cost cell when High Cost button is clicked."""
        self.canvas.bind("<Button-1>", self.set_high_cost_cell)

    def set_high_cost_cell(self, event):
        """Mark a cell as high-cost on the grid."""
        grid_x = event.y // self.cell_size
        grid_y = event.x // self.cell_size
        
        if self.grid.grid[grid_x][grid_y] != -1:  # Avoid overriding obstacles
            self.grid.set_high_cost(grid_x, grid_y)
            self.draw_grid()
        self.canvas.bind("<Button-1>")  # Unbind after setting the high-cost cell

    def handle_grid_click(self, event):
        """Handle left mouse clicks on the grid to set obstacles."""
        grid_x = event.y // self.cell_size
        grid_y = event.x // self.cell_size
        if self.grid.grid[grid_x][grid_y] == 0:  # Only set obstacles on empty cells
            self.grid.set_obstacle(grid_x, grid_y)
            self.draw_grid()

    def reset_grid(self):
        """Reset the path and robot path while keeping obstacles"""
        # Iterate through the grid and reset only the path and robot path cells
        for row in range(self.rows):
            for col in range(self.cols):
                # Reset only cells that are part of the path or visited nodes
                if self.grid.grid[row][col] in ["robot" , "path"] or self.grid.grid[row][col] == 10:
                    self.grid.grid[row][col] = 0  # Reset to an empty cell

        # Clear path and visited nodes data structures
        self.path = []  
        self.visiting_nodes = []

        # Redraw the grid to update the visuals
        self.draw_grid()

        # Reset the canvas bindings (if needed)
        self.canvas.bind("<Button-1>", self.handle_grid_click)

        print("Path and robot path have been reset, obstacles remain intact.")

    def resetall_grid(self):
            """Reset the path and robot path while keeping obstacles"""
            # Iterate through the grid and reset only the path and robot path cells
            for row in range(self.rows):
                for col in range(self.cols):
                        self.grid.grid[row][col] = 0  # Reset to an empty cell

            # Clear path and visited nodes data structures
            self.path = []  
            self.visiting_nodes = []

            # Redraw the grid to update the visuals
            self.draw_grid()

            # Reset the canvas bindings (if needed)
            self.canvas.bind("<Button-1>", self.handle_grid_click)

            print("Reset All")

    def run_algorithm(self):
        """Run the selected algorithm and display the path."""

   
        # Measure space for visited nodes
        initial_space = sys.getsizeof(self.visiting_nodes)
        print(f"Initial size of visiting_nodes: {initial_space} bytes")

        if self.grid.start is None or self.grid.target is None:
            print("Please set the start point!")
            return  # Prevent running the algorithm if start or target is not set
        
 

        if not self.algorithm:
            print("No algorithm selected!")
            return
        
   
        
        if self.algorithm == "UCS":
            self.path, self.visiting_nodes, cost = ucs(self.grid.grid, self.grid.start , self.grid.target) or([], [] , None) 
        elif self.algorithm == "BFS":
            self.path, self.visiting_nodes = bfs(self.grid.grid, self.grid.start, self.grid.target) or ([], [])
        elif self.algorithm == "DFS":
            self.path, self.visiting_nodes = dfs(self.grid.grid, self.grid.start, self.grid.target) or ([], [])
        elif self.algorithm == "DLS":
            self.path, self.visiting_nodes = dls(self.grid.grid ,self.grid.start , self.grid.target , self.depth_limit)  
        else:
            print("Algorithm not supported.")
            return

        if self.path:
            print(f"Path found: {self.path}")
        else:
            print("No path found!")

        # Highlight visited nodes
        for node in self.visiting_nodes:
            self.canvas.create_oval(
                node[1] * self.cell_size + self.cell_size // 4, node[0] * self.cell_size + self.cell_size // 4,
                (node[1] + 1) * self.cell_size - self.cell_size // 4, (node[0] + 1) * self.cell_size - self.cell_size // 4,
                fill="yellow"
            )
            self.root.update()
            self.root.after(200)  # Pause for animation effect

        # Highlight the path and move the image along the path
        for i, p in enumerate(self.path):
            if p != self.grid.start and p != self.grid.target:
                # Move the image in the current path point
                self.canvas.create_image(
                    p[1] * self.cell_size + self.cell_size // 2, 
                    p[0] * self.cell_size + self.cell_size // 2, 
                    image=self.path_image
                )
                self.root.update()
                self.root.after(500)  # Pause for path animation effect
  
         # Measure space after the algorithm runs
        final_space = sys.getsizeof(self.visiting_nodes)
        print(f"Final size of visiting_nodes: {final_space} bytes")
        
        # Print memory usage for visiting_nodes
        print(f"Memory used by visiting_nodes: {final_space - initial_space} bytes")       
                    
    def start(self):
        """Start the tkinter main loop."""
        self.root.mainloop()


