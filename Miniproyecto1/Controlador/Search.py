from Modelo.agent import Agent
from collections import deque
import heapq

class SearchController:
    def __init__(self, maze, strategy='A*'):
        self.maze = maze
        self.strategy = strategy

    def buscar(self):
        estrategias = ['A*', 'Amplitud', 'Profundidad', 'Costo Uniforme']
        for estrategia in estrategias:
            self.strategy = estrategia
            resultado = self._buscar_interno()
            if resultado:
                return resultado, estrategia  
        return ([], []), None

    def _buscar_interno(self):
        start_x, start_y = self.maze.start
        agente_inicial = Agent(start_x, start_y, strategy=self.strategy)

        if self.strategy == 'A*':
            frontier = []
            heapq.heappush(frontier, agente_inicial)
            pop = lambda: heapq.heappop(frontier)
            push = lambda a: heapq.heappush(frontier, a)

        elif self.strategy == 'Costo Uniforme':
            frontier = []
            heapq.heappush(frontier, (0, agente_inicial))
            pop = lambda: heapq.heappop(frontier)[1]
            push = lambda a: heapq.heappush(frontier, (a.recorrido, a))

        elif self.strategy == 'Amplitud':
            frontier = deque()
            frontier.append(agente_inicial)
            pop = lambda: frontier.popleft()
            push = lambda a: frontier.append(a)

        elif self.strategy == 'Profundidad':
            frontier = []
            frontier.append(agente_inicial)
            pop = lambda: frontier.pop()
            push = lambda a: frontier.append(a)

        else:
            return []

        visitados = set()

        nodos_expandidos = []

        while frontier:
            actual = pop()
            if (actual.x, actual.y) == self.maze.goal:
                return self.reconstruir_camino(actual), nodos_expandidos

            if (actual.x, actual.y) in visitados:
                continue
            visitados.add((actual.x, actual.y))
            nodos_expandidos.append((actual.x, actual.y))


            for vecino in actual.expandir(self.maze):
                if (vecino.x, vecino.y) not in visitados:
                    push(vecino)

        return []

    
    def reconstruir_camino(self, agente):
        camino = []
        while agente:
            camino.append((agente.x, agente.y))
            agente = agente.padre
        return camino[::-1]
