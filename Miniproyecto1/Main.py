import pygame
import json
import time
import tkinter as tk
from tkinter import simpledialog
from Modelo.maze import Maze
from Controlador.Search import SearchController
from Vista.GUI import init_gui, draw_ui_panel, draw_maze, draw_log_area, load_images, CELL_SIZE, MARGIN
import copy

def main():
    root = tk.Tk()
    root.withdraw()
    cols = simpledialog.askinteger("Dimensiones", "Número de columnas (X):", minvalue=5, maxvalue=30)
    rows = simpledialog.askinteger("Dimensiones", "Número de filas (Y):", minvalue=5, maxvalue=30)
    root.destroy()
    if not cols or not rows:
        cols, rows = 10, 10

    with open("laberintos.json", "r") as f:
        laberintos = json.load(f)

    index_laberinto = 0
    maze = Maze(copy.deepcopy(laberintos[index_laberinto]))
    agente_pos = maze.start

    screen = init_gui(cols, rows)
    mouse_img, cheese_img = load_images()
    font = pygame.font.SysFont(None, 24)

    button_generate = pygame.Rect(30, 400, 100, 40)
    button_start = pygame.Rect(150, 400, 100, 40)
    button_pause = pygame.Rect(30, 460, 100, 40)
    button_reset = pygame.Rect(150, 460, 100, 40)
    button_strategy = pygame.Rect(90, 520, 120, 40)

    buttons = [
        ("Generar", button_generate, (70, 130, 180)),
        ("Iniciar", button_start, (46, 204, 113)),
        ("Pausa", button_pause, (50, 50, 50)),
        ("Reiniciar", button_reset, (231, 76, 60)),
        ("Técnica", button_strategy, (255, 165, 0))
    ]

    running = True
    programa_iniciado = False
    pausa = False
    path = []
    logs = []
    expanded_nodes = []
    posicion_actual = 0
    estrategia_actual = 'a_star'
    last_move_time = time.time()
    goal_timer_interval = 10
    last_goal_change_time = time.time()

    def get_next_maze(laberintos, index_actual):
        nuevo_index = (index_actual + 1) % len(laberintos)
        nuevo = laberintos[nuevo_index]
        return nuevo, nuevo_index

    while running:
        screen.fill((30, 30, 30))

        input_values = {
            "Ancho": cols,
            "Alto": rows,
            "Ratón X": agente_pos[0] if agente_pos else '-',
            "Ratón Y": agente_pos[1] if agente_pos else '-',
            "Queso X": maze.goal[0] if maze.goal else '-',
            "Queso Y": maze.goal[1] if maze.goal else '-',
            "Técnica": estrategia_actual.upper(),
            "Velocidad": "0.5s",

        }


        draw_ui_panel(screen, font, input_values, buttons)
        draw_maze(screen, maze, agente_pos, maze.goal, mouse_img, cheese_img, offset_x=300)
        draw_log_area(screen, font, logs, cols)
        pygame.display.flip()

        now = time.time()

        if programa_iniciado and not pausa and path and posicion_actual < len(path):
            if now - last_move_time > 0.5:
                agente_pos = path[posicion_actual]
                maze.start = agente_pos
                posicion_actual += 1
                last_move_time = now
                logs.append(f"Nodo actual: {agente_pos}")
                if expanded_nodes:
                    nodos_str = ", ".join([str(n) for n in expanded_nodes[-5:]])
                    logs.append(f"Nodos expandidos ({estrategia_actual.upper()}): {nodos_str}")


            if posicion_actual >= len(path) or agente_pos == maze.goal:
                programa_iniciado = False
                pausa = False
                logs.append("Agente llegó al goal.")

        if programa_iniciado and time.time() - last_goal_change_time >= goal_timer_interval:
            maze.goal = maze.get_random_free_cell(exclude=[agente_pos])
            last_goal_change_time = time.time()
            controller = SearchController(maze, strategy=estrategia_actual)
            (resultados, estrategia_usada) = controller.buscar()
            path, expanded_nodes = resultados

            if path:
                estrategia_actual = estrategia_usada.lower()
                logs.append(f"Nuevo camino encontrado con: {estrategia_usada.upper()}")
                posicion_actual = 0
            else:
                programa_iniciado = False
                logs.append("No hay camino disponible con ninguna estrategia.")


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()

                if button_generate.collidepoint(mouse_pos):
                    nuevo_grid, index_laberinto = get_next_maze(laberintos, index_laberinto)
                    maze = Maze(copy.deepcopy(nuevo_grid))
                    agente_pos = maze.start
                    path = []
                    expanded_nodes = []
                    programa_iniciado = False
                    pausa = False
                    logs.append("Nuevo laberinto generado.")

                elif button_start.collidepoint(mouse_pos):
                    if agente_pos and maze.goal:
                        controller = SearchController(maze, strategy=estrategia_actual)
                        (resultados, estrategia_usada) = controller.buscar()
                        path, expanded_nodes = resultados

                        if path:
                            estrategia_actual = estrategia_usada.lower()
                            logs.append(f"Nuevo camino encontrado con: {estrategia_usada.upper()}")
                            posicion_actual = 0
                            programa_iniciado = True
                        else:
                            programa_iniciado = False
                            logs.append("No hay camino disponible con ninguna estrategia.")


                elif button_pause.collidepoint(mouse_pos):
                    pausa = not pausa
                    logs.append("Pausa activada." if pausa else "Pausa desactivada.")

                elif button_reset.collidepoint(mouse_pos):
                    agente_pos = maze.start
                    path = []
                    expanded_nodes = []
                    programa_iniciado = False
                    pausa = False
                    posicion_actual = 0
                    logs.append("Agente reiniciado.")

                elif button_strategy.collidepoint(mouse_pos):
                    estrategias = ['a_star', 'bfs', 'dfs', 'ucs']
                    index = estrategias.index(estrategia_actual)
                    estrategia_actual = estrategias[(index + 1) % len(estrategias)]
                    logs.append(f"Cambio de técnica: {estrategia_actual.upper()}")

                else:
                    x_click, y_click = mouse_pos
                    if x_click >= 300:
                        col = (x_click - 300) // (CELL_SIZE + MARGIN)
                        row = (y_click - 100) // (CELL_SIZE + MARGIN)

                        if 0 <= col < maze.cols and 0 <= row < maze.rows:
                            if not programa_iniciado:
                                if maze.grid[row][col] != 1 and (col, row) != maze.goal:
                                    agente_pos = (col, row)
                                    maze.start = agente_pos
                                    logs.append(f"Nuevo agente en: {agente_pos}")

                            else:
                                if maze.grid[row][col] == 0 and (col, row) != maze.goal and (col, row) != agente_pos:
                                    maze.grid[row][col] = 1
                                    logs.append(f"Muro colocado en: ({col}, {row})")

                                    controller = SearchController(maze, strategy=estrategia_actual)
                                    (resultados, estrategia_usada) = controller.buscar()
                                    path, expanded_nodes = resultados

                                    if path:
                                        estrategia_actual = estrategia_usada.lower()
                                        logs.append(f"Nuevo camino encontrado con: {estrategia_usada.upper()}")
                                        posicion_actual = 0
                                    else:
                                        programa_iniciado = False
                                        logs.append("No hay camino disponible con ninguna estrategia.")


    pygame.quit()

if __name__ == '__main__':
    main()
