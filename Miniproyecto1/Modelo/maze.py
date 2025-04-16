import random

class Maze:
    def __init__(self, grid):
        self.grid = grid
        self.rows = len(grid)
        self.cols = len(grid[0]) if grid else 0
        self.start = self.find_symbol('S')
        self.goal = self.find_symbol('G')

    def find_symbol(self, symbol):
        for i in range(self.rows):
            for j in range(self.cols):
                if self.grid[i][j] == symbol:
                    return (i, j)
        return None

    def is_valid(self, x, y):
        return (0 <= x < self.rows and
                0 <= y < self.cols and
                self.grid[x][y] != 1)

    def get_neighbors(self, x, y):
        directions = [(0,1), (1,0), (0,-1), (-1,0)]
        return [(x+dx, y+dy) for dx, dy in directions if self.is_valid(x+dx, y+dy)]

    def move_goal_randomly(self):
        if self.goal:
            x, y = self.goal
            if self.grid[x][y] == 'G':
                self.grid[x][y] = 0

        while True:
            nx = random.randint(0, self.rows - 1)
            ny = random.randint(0, self.cols - 1)
            if self.grid[nx][ny] == 0:
                self.grid[nx][ny] = 'G'
                self.goal = (nx, ny)
                break