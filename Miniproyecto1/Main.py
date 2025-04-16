from Modelo.maze import Maze
from Controlador.Search import SearchController
from Vista.GUI import init_gui, draw_maze, draw_button, get_cell_from_click, handle_events, get_next_maze
import pygame
import time
import json

with open("laberintos.json", "r") as f:
    laberintos = json.load(f)

index_laberinto = 0
maze = Maze(laberintos[index_laberinto])
agente_pos = maze.start


path = []
last_move_time = time.time()
intervalo_queso = 10

programa_iniciado = False
posicion_actual = 0
estrategia_actual = 'A*'

BUTTON_HEIGHT = 40
BUTTON_WIDTH = 180
OFFSET_Y = BUTTON_HEIGHT + 10

def main():
    global index_laberinto, maze, agente_pos, path, last_move_time, programa_iniciado, posicion_actual, estrategia_actual
    screen = init_gui(maze.cols, maze.rows)
    running = True

    while running:
        screen.fill((30, 30, 30))
        cambiar_btn = draw_button(screen, text="Random Maze", pos=(10, 5), color=(70, 130, 180))
        estrategia_btn = draw_button(screen, text=f"Estrategia: {estrategia_actual.upper()}", pos=(210, 5), color=(255, 165, 0))
        iniciar_btn = None
        if not programa_iniciado:
            iniciar_btn = draw_button(screen, text="Start", pos=(450, 5), color=(46, 204, 113))

        draw_maze(screen, maze, agente_pos, path, offset_y=OFFSET_Y)
        pygame.display.flip()

        now = time.time()
        if programa_iniciado and path and posicion_actual < len(path):
            if now - last_move_time > 1:
                agente_pos = path[posicion_actual]
                maze.start = agente_pos
                posicion_actual += 1
                last_move_time = now

            if posicion_actual >= len(path):
                programa_iniciado = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if cambiar_btn.collidepoint(mouse_pos):
                    nuevo_grid, index_laberinto = get_next_maze(laberintos, index_laberinto, agente_pos)
                    maze = Maze(nuevo_grid)
                    agente_pos = maze.start
                    path = []
                    programa_iniciado = False
                    posicion_actual = 0
                    screen = init_gui(maze.cols, maze.rows)
                elif estrategia_btn.collidepoint(mouse_pos):
                    estrategias = ['A*', 'Amplitud', 'Profundidad']
                    index = estrategias.index(estrategia_actual)
                    estrategia_actual = estrategias[(index + 1) % len(estrategias)]
                elif iniciar_btn and iniciar_btn.collidepoint(mouse_pos):
                    if agente_pos:
                        controller = SearchController(maze, strategy=estrategia_actual)
                        path = controller.buscar()
                        if path:
                            programa_iniciado = True
                            posicion_actual = 0

                else:
                    celda = get_cell_from_click(mouse_pos, maze.rows, maze.cols, offset_y=OFFSET_Y)
                    if celda and maze.is_valid(*celda):
                        agente_pos = celda
                        maze.start = celda
                        path = []
                        programa_iniciado = False
                        posicion_actual = 0

        handle_events()

    pygame.quit()

if __name__ == '__main__':
    main()