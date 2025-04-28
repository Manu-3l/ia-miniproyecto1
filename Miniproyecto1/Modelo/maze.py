import random

class Maze:
    def __init__(self, grid):
        self.grid = grid
        self.rows = len(grid)
        self.cols = len(grid[0]) if grid else 0
        self.start = self.find_symbol('S')
        self.goal = self.find_symbol('G')

    def find_symbol(self, symbol):
        for y in range(self.rows):
            for x in range(self.cols):
                if self.grid[y][x] == symbol:
                    return (x, y)  # <-- muy importante: (columna, fila)
        return None



    def is_valid(self, x, y):
        return (0 <= x < self.rows and
                0 <= y < self.cols and
                self.grid[x][y] != 1)

    def get_neighbors(self, x, y):
        movimientos = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Arriba, Abajo, Izquierda, Derecha
        vecinos = []
        for dx, dy in movimientos:
            nuevo_x = x + dx
            nuevo_y = y + dy
            if 0 <= nuevo_y < self.rows and 0 <= nuevo_x < self.cols:
                if self.grid[nuevo_y][nuevo_x] != 1:
                    vecinos.append((nuevo_x, nuevo_y))
        return vecinos


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

    def get_random_free_cell(self, exclude=[]):
        free_cells = []
        for row in range(self.rows):
            for col in range(self.cols):
                if self.grid[row][col] == 0 and (col, row) not in exclude:
                    free_cells.append((col, row))
        if free_cells:
            return random.choice(free_cells)
        else:
            return (0, 0)