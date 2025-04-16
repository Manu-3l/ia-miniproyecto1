class Agent:
    def __init__(self, x, y, heuristica=0, recorrido=0, strategy='A*'):
        self.x = x
        self.y = y
        self.heuristica = heuristica
        self.recorrido = recorrido
        self.strategy = strategy
        self.padre = None

    def posicion(self):
        return (self.x, self.y)

    def expandir(self, maze):
        vecinos = []
        for nx, ny in maze.get_neighbors(self.x, self.y):
            nuevo_costo = self.recorrido + 1
            heur = self.calcular_heuristica((nx, ny), maze.goal)
            nuevo = Agent(nx, ny, heur, nuevo_costo, self.strategy)
            nuevo.padre = self
            vecinos.append(nuevo)
        return vecinos

    def calcular_heuristica(self, pos, goal):
        if self.strategy == 'A*':
            return abs(pos[0] - goal[0]) + abs(pos[1] - goal[1])
        return 0

    def __lt__(self, other):
        return (self.recorrido + self.heuristica) < (other.recorrido + other.heuristica)
