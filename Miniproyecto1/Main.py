from Modelo.maze import Maze
from Controlador.Search import SearchController
from Vista.GUI import init_gui, draw_maze, draw_button, draw_input_box, draw_agent_position, get_cell_from_click, handle_events, get_next_maze
import pygame
import time
import json
import tkinter as tk
from tkinter import simpledialog

def solicitar_dimensiones():
    root = tk.Tk()
    root.withdraw()
    cols = simpledialog.askinteger("Dimensiones", "Número de columnas (X):", minvalue=5, maxvalue=30)
    rows = simpledialog.askinteger("Dimensiones", "Número de filas (Y):", minvalue=5, maxvalue=30)
    root.destroy()
    if not cols or not rows:
        cols, rows = 10, 10
    return cols, rows

cols, rows = solicitar_dimensiones()

with open("laberintos.json", "r") as f:
    laberintos = json.load(f)

index_laberinto = 0
maze = Maze(laberintos[index_laberinto])
agente_pos = maze.start

screen = init_gui(maze.cols, maze.rows)
path = []
last_move_time = time.time()
intervalo_queso = 10

programa_iniciado = False
colocando_muros = False
posicion_actual = 0
estrategia_actual = 'a_star'
input_text = "10"
goal_timer_interval = 10
last_goal_change_time = time.time()
input_active = False

BUTTON_HEIGHT = 40
BUTTON_WIDTH = 180
OFFSET_Y = BUTTON_HEIGHT + 10


def main():
    global index_laberinto, maze, agente_pos, path, last_move_time, programa_iniciado, posicion_actual, estrategia_actual, colocando_muros, input_text, goal_timer_interval, last_goal_change_time, input_active, screen
    running = True

    while running:
        screen.fill((30, 30, 30))
        cambiar_btn = draw_button(screen, text="Random Maze", pos=(10, 5), color=(70, 130, 180))
        estrategia_btn = draw_button(screen, text=f"Estrategia: {estrategia_actual.upper()}", pos=(210, 5), color=(255, 165, 0))
        iniciar_btn = None
        if not programa_iniciado:
            iniciar_btn = draw_button(screen, text="Inicio", pos=(450, 5), color=(46, 204, 113))

        input_box = draw_input_box(screen, input_text, pos=(650, 5))

        draw_maze(screen, maze, agente_pos, path, estrategia_actual, offset_y=OFFSET_Y)
        draw_agent_position(screen, agente_pos, maze.cols, offset_y=OFFSET_Y)
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
                colocando_muros = False

        if time.time() - last_goal_change_time >= goal_timer_interval:
            maze.goal = maze.get_random_free_cell(exclude=[agente_pos])
            last_goal_change_time = time.time()

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
                    estrategias = ['a_star', 'bfs', 'dfs', 'ucs']
                    index = estrategias.index(estrategia_actual)
                    estrategia_actual = estrategias[(index + 1) % len(estrategias)]
                elif iniciar_btn and iniciar_btn.collidepoint(mouse_pos):
                    if agente_pos:
                        controller = SearchController(maze, strategy=estrategia_actual)
                        path = controller.buscar()
                        if path:
                            programa_iniciado = True
                            posicion_actual = 0
                            colocando_muros = True
                else:
                    if input_box.collidepoint(mouse_pos):
                        input_active = True
                    else:
                        input_active = False
                    celda = get_cell_from_click(mouse_pos, maze.rows, maze.cols, offset_y=OFFSET_Y)
                    if celda:
                        if colocando_muros and programa_iniciado:
                            x, y = celda
                            if maze.grid[y][x] == 0 and (x, y) != agente_pos and (x, y) != maze.goal:
                                maze.grid[y][x] = 1
                        elif not programa_iniciado:
                            agente_pos = celda
                            maze.start = celda
                            path = []
                            programa_iniciado = False
                            colocando_muros = False
                            posicion_actual = 0
            elif event.type == pygame.KEYDOWN:
                if input_active:
                    if event.key == pygame.K_RETURN:
                        try:
                            goal_timer_interval = int(input_text)
                        except:
                            goal_timer_interval = 10
                        input_text = ""
                    elif event.key == pygame.K_BACKSPACE:
                        input_text = input_text[:-1]
                    else:
                        if len(input_text) < 3 and event.unicode.isdigit():
                            input_text += event.unicode

        handle_events()

    pygame.quit()

if __name__ == '__main__':
    main()