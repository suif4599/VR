import random
import numpy as np

class Maze2D:
    'one is path, zero is wall'
    def __init__(self, rows: int, cols: int) -> None:
        self.rows = rows
        self.cols = cols
        self.generate_maze()

    def generate_maze(self):
        num_rows = self.rows
        num_cols = self.cols
        M = np.zeros((num_rows, num_cols, 5), dtype=np.uint8)

        # Break the walls of enter and exit
        # M[0, 0, 0] = 1
        # M[num_rows - 1, num_cols - 1, 2] = 1

        possibility = [(0, 0)]

        while possibility:
            # random choose a candidate cell from the cell set histroy
            r, c = random.choice(possibility)
            M[r, c, 4] = 1  # designate this location as visited

            possibility.remove((r, c))
            check = []
            # If the randomly chosen cell has multiple edges
            # that connect it to the existing maze.
            if c > 0:  # the visit state of left cell (for example)
                if M[r, c - 1, 4] == 1:  # If this cell was visited,
                    check.append("L")  # it can be choiced as direction.
                elif M[r, c - 1, 4] == 0:  # else if it has not been visited...
                    possibility.append((r, c - 1))
                    M[r, c - 1, 4] = 2
            if r > 0:  # the visit state of up cell
                if M[r - 1, c, 4] == 1:
                    check.append("U")
                elif M[r - 1, c, 4] == 0:
                    possibility.append((r - 1, c))
                    M[r - 1, c, 4] = 2
            if c < num_cols - 1:  # the visit state of right cell
                if M[r, c + 1, 4] == 1:
                    check.append("R")
                elif M[r, c + 1, 4] == 0:
                    possibility.append((r, c + 1))
                    M[r, c + 1, 4] = 2
            if r < num_rows - 1:  # the visit state of down cell
                if M[r + 1, c, 4] == 1:
                    check.append("D")
                elif M[r + 1, c, 4] == 0:
                    possibility.append((r + 1, c))
                    M[r + 1, c, 4] = 2

            # Select one of these edges as direction at random,
            # and break the walls between these two cells.
            if len(check):
                move_direction = random.choice(check)  # Select a direction
                # Break the walls.
                if move_direction == "L":
                    M[r, c, 0] = 1
                    c = c - 1
                    M[r, c, 2] = 1
                if move_direction == "U":
                    M[r, c, 1] = 1
                    r = r - 1
                    M[r, c, 3] = 1
                if move_direction == "R":
                    M[r, c, 2] = 1
                    c = c + 1
                    M[r, c, 0] = 1
                if move_direction == "D":
                    M[r, c, 3] = 1
                    r = r + 1
                    M[r, c, 1] = 1

        # generate the maze into 2d array without display
        maze = np.zeros((num_rows * 2 + 1, num_cols * 2 + 1), dtype=np.uint8)
        for row in range(num_rows):
            for col in range(num_cols):
                maze[row * 2 + 1, col * 2 + 1] = 1
                if M[row, col, 0] == 1:
                    maze[row * 2 + 1, col * 2] = 1
                if M[row, col, 1] == 1:
                    maze[row * 2, col * 2 + 1] = 1
                if M[row, col, 2] == 1:
                    maze[row * 2 + 1, col * 2 + 2] = 1
                if M[row, col, 3] == 1:
                    maze[row * 2 + 2, col * 2 + 1] = 1
        self.maze = maze

# print(Maze2D(10, 10).maze)
