import pygame

CELL_SIZE = 60
BUTTON_HEIGHT = 40
BUTTON_WIDTH = 180

COLOR_BTN_TEXT = (255, 255, 255)

AGENT_COLORS = {
    "a_star": (255, 0, 0),
    "dfs": (255, 255, 0),
    "bfs": (0, 0, 255),
    "ucs": (0, 255, 0)
}

def draw_button(screen, text="Botón", pos=(10, 5), color=(100, 100, 100)):
    rect = pygame.Rect(pos[0], pos[1], BUTTON_WIDTH, BUTTON_HEIGHT)
    pygame.draw.rect(screen, color, rect, border_radius=6)
    font = pygame.font.SysFont(None, 24)
    text_surface = font.render(text, True, COLOR_BTN_TEXT)
    text_rect = text_surface.get_rect(center=rect.center)
    screen.blit(text_surface, text_rect)
    return rect

def draw_maze(screen, maze, agente_pos, path, estrategia='a_star', offset_y=0):
    for row in range(maze.rows):
        for col in range(maze.cols):
            x = col * CELL_SIZE
            y = row * CELL_SIZE + offset_y

            if maze.grid[row][col] == 1:
                color = (0, 0, 0)  # muro
            elif (col, row) == maze.goal:
                color = (255, 0, 0)  # goal
            elif (col, row) == agente_pos:
                color = AGENT_COLORS.get(estrategia, (0, 0, 255))  # agente
            else:
                color = (255, 255, 255)  # camino libre

            pygame.draw.rect(screen, color, (x, y, CELL_SIZE, CELL_SIZE))

            if (col, row) == agente_pos:
                pygame.draw.rect(screen, (0, 255, 0), (x, y, CELL_SIZE, CELL_SIZE), 4)



def draw_input_box(screen, input_text, pos=(10, 60)):
    font = pygame.font.SysFont(None, 28)
    input_box = pygame.Rect(pos[0], pos[1], 100, 32)
    pygame.draw.rect(screen, (255, 255, 255), input_box, 2)
    text_surface = font.render(input_text, True, (255, 255, 255))
    screen.blit(text_surface, (input_box.x + 5, input_box.y + 5))
    return input_box

def draw_agent_position(screen, agent_pos, maze_cols, offset_y=0):
    font = pygame.font.SysFont(None, 30)
    text = f"Posición: {agent_pos}"
    text_surface = font.render(text, True, (255, 255, 255))
    x_pos = maze_cols * CELL_SIZE + 20
    y_pos = offset_y + 20
    screen.blit(text_surface, (x_pos, y_pos))

def get_cell_from_click(mouse_pos, rows, cols, offset_y=0):
    x, y = mouse_pos
    if y < offset_y:
        return None
    col = x // CELL_SIZE
    row = (y - offset_y) // CELL_SIZE
    if 0 <= row < rows and 0 <= col < cols:
        return (col, row)
    return None

def handle_events():
    pass

def get_next_maze(laberintos, index_actual, agente_pos):
    nuevo_index = (index_actual + 1) % len(laberintos)
    nuevo = laberintos[nuevo_index]
    return nuevo, nuevo_index

def init_gui(cols, rows):
    pygame.init()
    screen_width = cols * CELL_SIZE + 300
    screen_height = rows * CELL_SIZE + BUTTON_HEIGHT + 10
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Laberinto Inteligente")
    return screen
