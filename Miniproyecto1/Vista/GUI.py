import pygame
import os

CELL_SIZE = 40
MARGIN = 5
PANEL_WIDTH = 300
LOG_HEIGHT = 150

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LIGHT_GRAY = (200, 200, 200)
DARK_GRAY = (50, 50, 50)
BLUE = (70, 130, 180)
GREEN = (46, 204, 113)
RED = (231, 76, 60)

# Cargar imágenes
def load_images():
    base_path = os.path.join(os.getcwd(), "Archivos")
    mouse_img = pygame.image.load(os.path.join(base_path, "mouse.png"))
    cheese_img = pygame.image.load(os.path.join(base_path, "cheese.png"))
    return pygame.transform.scale(mouse_img, (CELL_SIZE, CELL_SIZE)), pygame.transform.scale(cheese_img, (CELL_SIZE, CELL_SIZE))

# Inicializar pantalla
def init_gui(cols, rows):
    pygame.init()
    width = cols * (CELL_SIZE + MARGIN) + PANEL_WIDTH
    height = rows * (CELL_SIZE + MARGIN) + 100 + LOG_HEIGHT
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Agente Inteligente en Laberinto Dinámico")
    return screen

# Dibujar panel izquierdo (botones, inputs)
def draw_ui_panel(screen, font, input_values, buttons):
    x_offset = 10
    y_offset = 20

    # Título
    title = font.render("Agente Inteligente", True, (70, 130, 180))
    screen.blit(title, (x_offset, y_offset))
    y_offset += 40

    # Inputs
    labels = ["Ancho", "Alto", "Ratón X", "Ratón Y", "Queso X", "Queso Y", "Técnica", "Velocidad"]
    for label in labels:
        text = font.render(f"{label}:", True, (255, 255, 255))
        screen.blit(text, (x_offset, y_offset))

        # Mostrar valor
        valor = str(input_values.get(label, "-"))
        valor_surface = font.render(valor, True, (200, 200, 200))
        screen.blit(valor_surface, (x_offset + 120, y_offset))

        y_offset += 30

    # Botones
    for btn_text, rect, color in buttons:
        pygame.draw.rect(screen, color, rect, border_radius=8)
        text = font.render(btn_text, True, (0, 0, 0))
        text_rect = text.get_rect(center=rect.center)
        screen.blit(text, text_rect)


# Dibujar laberinto
def draw_maze(screen, maze, agent_pos, goal_pos, mouse_img, cheese_img, offset_x):
    for row in range(maze.rows):
        for col in range(maze.cols):
            x = offset_x + col * (CELL_SIZE + MARGIN)
            y = 100 + row * (CELL_SIZE + MARGIN)

            color = WHITE if maze.grid[row][col] != 1 else DARK_GRAY
            pygame.draw.rect(screen, color, (x, y, CELL_SIZE, CELL_SIZE))

            if (col, row) == agent_pos:
                screen.blit(mouse_img, (x, y))
            elif (col, row) == goal_pos:
                screen.blit(cheese_img, (x, y))

# Dibujar área de log
def draw_log_area(screen, font, logs, cols):
    width = cols * (CELL_SIZE + MARGIN) + PANEL_WIDTH
    log_rect = pygame.Rect(0, screen.get_height() - LOG_HEIGHT, width, LOG_HEIGHT)
    pygame.draw.rect(screen, LIGHT_GRAY, log_rect)

    y = log_rect.y + 10
    for log in logs[-5:]:
        log_text = font.render(log, True, BLACK)
        screen.blit(log_text, (20, y))
        y += 25
