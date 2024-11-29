# Run the application

from ui import PathfindingApp
if __name__ == "__main__":
    app = PathfindingApp(rows=6, cols=6, cell_size=50)  # Grid size 6x6, cell size 50px
    app.root.mainloop()