import random
import numpy as np
from ..engine import Point, GeneralPoint
from math import inf

class Maze:
    'one is path, zero is wall'
    def __init__(self, rows: int, cols: int, height: int, delta: float = 0.2) -> None:
        self.rows = rows
        self.cols = cols
        self.height = height
        self.delta = delta
        self.generate_maze()

    def generate_maze(self): # from web, i extend it to 3d
        num_rows = self.rows
        num_cols = self.cols
        num_h = self.height
        M = np.zeros((num_rows, num_cols, num_h, 7), dtype=np.uint8)
        # The array M is going to hold the array information for each cell.
        # The first four coordinates tell if walls exist on those sides
        # and the fifth indicates if the cell has been visited in the search.
        # M(LEFT, UP, RIGHT, DOWN, FRONT, BACK, CHECK_IF_VISITED)

        # Break the walls of enter and exit
        # M[0, 0, 0] = 1
        # M[num_rows - 1, num_cols - 1, 2] = 1

        possibility = [(0, 0, 0)]

        while possibility:
            # random choose a candidate cell from the cell set histroy
            r, c, t = random.choice(possibility)
            M[r, c, t, 6] = 1  # designate this location as visited

            possibility.remove((r, c, t))
            check = []
            # If the randomly chosen cell has multiple edges
            # that connect it to the existing self.
            if c > 0:  # the visit state of left cell (for example)
                if M[r, c - 1, t, 6] == 1:  # If this cell was visited,
                    check.append("L")  # it can be choiced as direction.
                elif M[r, c - 1, t, 6] == 0:  # else if it has not been visited...
                    possibility.append((r, c - 1, t))
                    M[r, c - 1, t, 6] = 2
            if r > 0:  # the visit state of up cell
                if M[r - 1, c, t, 6] == 1:
                    check.append("U")
                elif M[r - 1, c, t, 6] == 0:
                    possibility.append((r - 1, c, t))
                    M[r - 1, c, t, 6] = 2
            if t > 0: # the visit state of front cell
                if M[r, c, t - 1, 6] == 1:
                    check.append("F")
                elif M[r, c, t - 1, 6] == 0:
                    possibility.append((r, c, t - 1))
                    M[r, c, t - 1, 6] = 2
            if c < num_cols - 1:  # the visit state of right cell
                if M[r, c + 1, t, 6] == 1:
                    check.append("R")
                elif M[r, c + 1, t, 6] == 0:
                    possibility.append((r, c + 1, t))
                    M[r, c + 1, t, 6] = 2
            if r < num_rows - 1:  # the visit state of down cell
                if M[r + 1, c, t, 6] == 1:
                    check.append("D")
                elif M[r + 1, c, t, 6] == 0:
                    possibility.append((r + 1, c, t))
                    M[r + 1, c, t, 6] = 2
            if t < num_h - 1:  # the visit state of back cell
                if M[r, c, t + 1, 6] == 1:
                    check.append("B")
                elif M[r, c, t + 1, 6] == 0:
                    possibility.append((r, c, t + 1))
                    M[r, c, t + 1, 6] = 2

            # Select one of these edges as direction at random,
            # and break the walls between these two cells.
            if len(check):
                move_direction = random.choice(check)  # Select a direction
                # Break the walls.
                if move_direction == "L":
                    M[r, c, t, 0] = 1
                    c = c - 1
                    M[r, c, t, 2] = 1
                if move_direction == "U":
                    M[r, c, t, 1] = 1
                    r = r - 1
                    M[r, c, t, 3] = 1
                if move_direction == "R":
                    M[r, c, t, 2] = 1
                    c = c + 1
                    M[r, c, t, 0] = 1
                if move_direction == "D":
                    M[r, c, t, 3] = 1
                    r = r + 1
                    M[r, c, t, 1] = 1
                if move_direction == "F":
                    M[r, c, t, 4] = 1
                    t = t - 1
                    M[r, c, t, 5] = 1
                if move_direction == "B":
                    M[r, c, t, 5] = 1
                    t = t + 1
                    M[r, c, t, 4] = 1

        # generate the maze into 2d array without display
        maze = np.zeros((num_rows * 2 + 1, num_cols * 2 + 1, num_h * 2 + 1), dtype=np.uint8)
        for row in range(num_rows):
            for col in range(num_cols):
                for height in range(num_h):
                    maze[row * 2 + 1, col * 2 + 1, height * 2 + 1] = 1
                    if M[row, col, height, 0] == 1:
                        maze[row * 2 + 1, col * 2, height * 2 + 1] = 1
                    if M[row, col, height, 1] == 1:
                        maze[row * 2, col * 2 + 1, height * 2 + 1] = 1
                    if M[row, col, height, 2] == 1:
                        maze[row * 2 + 1, col * 2 + 2, height * 2 + 1] = 1
                    if M[row, col, height, 3] == 1:
                        maze[row * 2 + 2, col * 2 + 1, height * 2 + 1] = 1
                    if M[row, col, height, 4] == 1:
                        maze[row * 2 + 1, col * 2 + 1, height * 2] = 1
                    if M[row, col, height, 5] == 1:
                        maze[row * 2 + 1, col * 2 + 1, height * 2 + 2] = 1
        self.maze = maze

    def position_refiner(self, position: Point) -> GeneralPoint:
        delta = self.delta
        if not self.maze[int(position.x + delta), int(position.y), int(position.z)]:
            return self.position_refiner(Point(int(position.x + delta) - delta * 1.01, position.y, position.z))
        if not self.maze[int(position.x - delta), int(position.y), int(position.z)]:
            return self.position_refiner(Point(int(position.x) + delta  * 1.01, position.y, position.z))
        if not self.maze[int(position.x), int(position.y + delta), int(position.z)]:
            return self.position_refiner(Point(position.x, int(position.y + delta) - delta * 1.01, position.z))
        if not self.maze[int(position.x), int(position.y - delta), int(position.z)]:
            return self.position_refiner(Point(position.x, int(position.y) + delta * 1.01, position.z))
        if not self.maze[int(position.x), int(position.y), int(position.z + delta)]:
            return self.position_refiner(Point(position.x, position.y, int(position.z + delta) - delta * 1.01))
        if not self.maze[int(position.x), int(position.y), int(position.z - delta)]:
            return self.position_refiner(Point(position.x, position.y, int(position.z) + delta * 1.01))
        return position

    def solute(self) -> np.ndarray:
        if hasattr(self, "solution"):
            return self.solution
        solution = np.zeros((self.rows * 2 + 1, self.cols * 2 + 1, self.height * 2 + 1), dtype=np.int32)
        solution[self.maze == 0] = -1
        available = [(self.rows * 2 - 1, self.cols * 2 - 1, self.height * 2 - 1, 1)]
        # visited path: > 0
        # unvisited path: 0
        # wall: -1
        while available:
            x, y, z, d = available.pop()
            if solution[x, y, z]: # if the cell is visited or wall
                continue
            solution[x, y, z] = d
            if solution[x + 1, y, z] == 0: # if the cell is a unvisited path
                solution[x + 1, y, z] = d + 1
                available.append((x + 2, y, z, d + 2))
            if solution[x - 1, y, z] == 0:
                solution[x - 1, y, z] = d + 1
                available.append((x - 2, y, z, d + 2))
            if solution[x, y + 1, z] == 0:
                solution[x, y + 1, z] = d + 1
                available.append((x, y + 2, z, d + 2))
            if solution[x, y - 1, z] == 0:
                solution[x, y - 1, z] = d + 1
                available.append((x, y - 2, z, d + 2))
            if solution[x, y, z + 1] == 0:
                solution[x, y, z + 1] = d + 1
                available.append((x, y, z + 2, d + 2))
            if solution[x, y, z - 1] == 0:
                solution[x, y, z - 1] = d + 1
                available.append((x, y, z - 2, d + 2))
        self.solution = solution
        return solution
    
    def next_path(self, position: GeneralPoint) -> Point:
        if isinstance(position, tuple):
            position = Point(*position)
        x, y, z = int(position.x), int(position.y), int(position.z)
        solution = self.solution
        xp = solution[x + 1, y, z] if solution[x + 1, y, z] > 0 else inf 
        xn = solution[x - 1, y, z] if solution[x - 1, y, z] > 0 else inf
        yp = solution[x, y + 1, z] if solution[x, y + 1, z] > 0 else inf
        yn = solution[x, y - 1, z] if solution[x, y - 1, z] > 0 else inf
        zp = solution[x, y, z + 1] if solution[x, y, z + 1] > 0 else inf
        zn = solution[x, y, z - 1] if solution[x, y, z - 1] > 0 else inf
        m = min(xp, xn, yp, yn, zp, zn)
        if xp == m:
            return Point(x + 1, y, z)
        if xn == m:
            return Point(x - 1, y, z)
        if yp == m:
            return Point(x, y + 1, z)
        if yn == m:
            return Point(x, y - 1, z)
        if zp == m:
            return Point(x, y, z + 1)
        if zn == m:
            return Point(x, y, z - 1)