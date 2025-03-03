import pygame
import random
import time

pygame.init()

#Constantes
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
TILE_SIZE = 100
GRID_WIDTH = SCREEN_WIDTH // TILE_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // TILE_SIZE

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Pantalla
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pipe Puzzle")

# Fotos en imagenes/Tuberias
background_img = pygame.image.load('imagenes/Tuberias/fondo.jpg')
background_img = pygame.transform.scale(background_img, (SCREEN_WIDTH, SCREEN_HEIGHT))
horizontal_img = pygame.image.load('imagenes/Tuberias/horizontal/pipe_horizontal.png')
vertical_img = pygame.image.load('imagenes/Tuberias/vertical/pipe_vertical.png')
corner_tl_img = pygame.image.load('imagenes/Tuberias/top_left/pipe_corner_top_left.png')
corner_tr_img = pygame.image.load('imagenes/Tuberias/top_right/pipe_corner_top_right.png')
corner_bl_img = pygame.image.load('imagenes/Tuberias/bottom_left/pipe_corner_bottom_left.png')
corner_br_img = pygame.image.load('imagenes/Tuberias/bottom_right/pipe_corner_bottom_right.png')

# Clase de las tuberias con los metodos para dibujar las tuberias con su imagen correspodiente
# y para rotar las tuberias (Poner la imagen de la tuberia en la posicion correcta)
class Pipe:
    def __init__(self, x, y, type):
        self.x = x
        self.y = y
        self.type = type

    def draw(self):
        if self.type == 'horizontal':
            img = horizontal_img
        elif self.type == 'vertical':
            img = vertical_img
        elif self.type == 'corner_tl':
            img = corner_tl_img
        elif self.type == 'corner_tr':
            img = corner_tr_img
        elif self.type == 'corner_bl':
            img = corner_bl_img
        elif self.type == 'corner_br':
            img = corner_br_img
        screen.blit(img, (self.x * TILE_SIZE, self.y * TILE_SIZE))

    def rotate(self):
        if self.type == 'horizontal':
            self.type = 'vertical'
        elif self.type == 'vertical':
            self.type = 'horizontal'
        elif self.type == 'corner_tl':
            self.type = 'corner_tr'
        elif self.type == 'corner_tr':
            self.type = 'corner_br'
        elif self.type == 'corner_br':
            self.type = 'corner_bl'
        elif self.type == 'corner_bl':
            self.type = 'corner_tl'

# Creamos la planilla de tuberias con el tamaño de la pantalla
grid = [[None for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]

# Este sería el estado inicial del puzzle (no esta muy dificil)
path = [
    (0, GRID_HEIGHT // 2, 'horizontal'),
    (1, GRID_HEIGHT // 2, 'horizontal'),
    (2, GRID_HEIGHT // 2, 'corner_tr'),
    (2, GRID_HEIGHT // 2 - 1, 'vertical'),
    (2, GRID_HEIGHT // 2 - 2, 'corner_br'),
    (3, GRID_HEIGHT // 2 - 2, 'horizontal'),
    (4, GRID_HEIGHT // 2 - 2, 'horizontal'),
    (5, GRID_HEIGHT // 2 - 2, 'corner_bl'),
    (5, GRID_HEIGHT // 2 - 1, 'vertical'),
    (5, GRID_HEIGHT // 2, 'corner_tl'),
    (6, GRID_HEIGHT // 2, 'horizontal'),
    (7, GRID_HEIGHT // 2, 'horizontal')
]

# Este sería el estado final del puzzle(Las rotaciones son con la imagagen correcta)
solution_path = [
    (0, GRID_HEIGHT // 2, 'horizontal'),
    (1, GRID_HEIGHT // 2, 'horizontal'),
    (2, GRID_HEIGHT // 2, 'corner_tl'),  # Cambiada
    (2, GRID_HEIGHT // 2 - 1, 'vertical'),
    (2, GRID_HEIGHT // 2 - 2, 'corner_br'),
    (3, GRID_HEIGHT // 2 - 2, 'horizontal'),
    (4, GRID_HEIGHT // 2 - 2, 'horizontal'),
    (5, GRID_HEIGHT // 2 - 2, 'corner_bl'),
    (5, GRID_HEIGHT // 2 - 1, 'vertical'),
    (5, GRID_HEIGHT // 2, 'corner_tr'),  # Cambiada
    (6, GRID_HEIGHT // 2, 'horizontal'),
    (7, GRID_HEIGHT // 2, 'horizontal')
]

# Ponemos las tuberias en la planilla siguiendo el path
for x, y, pipe_type in path:
    grid[y][x] = Pipe(x, y, pipe_type)

# Funcion para verificar si el puzzle esta resuelto (comparar el actual y el final)
def is_solved():
    for x, y, pipe_type in solution_path:
        if grid[y][x].type != pipe_type:
            return False
    return True

# Loop principal
start_time = time.time()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos
            grid_x = mouse_x // TILE_SIZE
            grid_y = mouse_y // TILE_SIZE
            if 0 <= grid_x < GRID_WIDTH and 0 <= grid_y < GRID_HEIGHT and grid[grid_y][grid_x] is not None:
                grid[grid_y][grid_x].rotate()

    screen.blit(background_img, (0, 0))

    for row in grid:
        for pipe in row:
            if pipe is not None:
                pipe.draw()

    # Dibujar el tiempo restante (20s)
    elapsed_time = time.time() - start_time
    remaining_time = max(0, 20 - int(elapsed_time))
    font = pygame.font.Font(None, 74)
    timer_text = font.render(f"Tiempo: {remaining_time}", True, BLACK)
    screen.blit(timer_text, (10, 10))

    pygame.display.flip()

    # Miramos si esta resuelto
    if is_solved():
        font = pygame.font.Font(None, 74)
        text = font.render("¡Felicidades!", True, BLACK)
        screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2 - text.get_height() // 2))
        pygame.display.flip()
        pygame.time.wait(3000) 
        running = False

    # Comprobar si el tiempo se ha acabado
    if elapsed_time >= 20:
        font = pygame.font.Font(None, 74)
        text = font.render("Perdiste", True, BLACK)
        screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2 - text.get_height() // 2))
        pygame.display.flip()
        pygame.time.wait(3000)  
        running = False

pygame.quit()
