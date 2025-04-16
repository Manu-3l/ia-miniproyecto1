import pygame

CELL_SIZE = 60
MARGIN = 2
BUTTON_HEIGHT = 40
BUTTON_WIDTH = 80

COLOR_BG = (30, 30, 30)
COLOR_WALL = (0, 0, 0)
COLOR_FREE = (255, 255, 255)
COLOR_START = (0, 255, 0)
COLOR_GOAL = (255, 0, 0)
COLOR_AGENT = (0, 0, 255)
COLOR_PATH = (200, 200, 255)
COLOR_BTN = (100, 100, 100)

def draw_button(screen, text="Botón", pos=(10, 5), color=(100, 100, 100)):
    rect = pygame.Rect(pos[0], pos[1], BUTTON_WIDTH, BUTTON_HEIGHT)
    pygame.draw.rect(screen, color, rect, border_radius=6)
    font = pygame.font.SysFont(None, 12)
    text_surface = font.render(text, True, COLOR_FREE)
    text_rect = text_surface.get_rect(center=rect.center)
    screen.blit(text_surface, text_rect)
    return rect

def draw_maze(screen, maze, agente_pos, path, offset_y=0):
    for row in range(maze.rows):
        for col in range(maze.cols):
            x = col * CELL_SIZE
            y = row * CELL_SIZE + offset_y

            if maze.grid[row][col] == 1:
                color = (0, 0, 0)
            elif (row, col) == maze.goal:
                color = (255, 0, 0)
            elif (row, col) == agente_pos:
                color = (0, 0, 255)
            else:
                color = (255, 255, 255)

            pygame.draw.rect(screen, color, (x, y, CELL_SIZE, CELL_SIZE))

            if (row, col) == agente_pos:
                pygame.draw.rect(screen, (0, 255, 0), (x, y, CELL_SIZE, CELL_SIZE), 4)

def get_cell_from_click(mouse_pos, rows, cols, offset_y=0):
    x, y = mouse_pos
    if y < offset_y:
        return None
    col = x // CELL_SIZE
    row = (y - offset_y) // CELL_SIZE
    if 0 <= row < rows and 0 <= col < cols:
        return (row, col)
    return None

def handle_events():
    pass

def get_next_maze(laberintos, index_actual, agente_pos):
    nuevo_index = (index_actual + 1) % len(laberintos)
    nuevo = laberintos[nuevo_index]
    return nuevo, nuevo_index

def init_gui(cols, rows):
    pygame.init()
    screen_width = cols * CELL_SIZE
    screen_height = rows * CELL_SIZE + BUTTON_HEIGHT + 10
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Laberinto Inteligente")
    return screen