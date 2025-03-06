import pygame

pygame.init()

# Constantes
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
GRID_SIZE = 5
TILE_SIZE = SCREEN_WIDTH // GRID_SIZE
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GRAY = (200, 200, 200)


screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Laser Puzzle")

# Imagenes
laser_img_horizontal = pygame.transform.rotate(pygame.image.load('C:/Users/siimi/Documents/doble-venganza-la-conspiracion-helix/imagenes/Laser/laser.png'), 90)
laser_img_vertical = pygame.image.load('C:/Users/siimi/Documents/doble-venganza-la-conspiracion-helix/imagenes/Laser/laser.png')
door_closed_img = pygame.transform.scale(pygame.image.load('C:/Users/siimi/Documents/doble-venganza-la-conspiracion-helix/imagenes/Laser/cadeado_fechado.png'), (TILE_SIZE, TILE_SIZE))
door_open_img = pygame.transform.scale(pygame.image.load('C:/Users/siimi/Documents/doble-venganza-la-conspiracion-helix/imagenes/Laser/cadeado_aberto.png'), (TILE_SIZE, TILE_SIZE))
mirror_up_img = pygame.transform.scale(pygame.image.load('C:/Users/siimi/Documents/doble-venganza-la-conspiracion-helix/imagenes/Laser/espejo.png'), (TILE_SIZE, TILE_SIZE))
mirror_down_img = pygame.transform.scale(pygame.image.load('C:/Users/siimi/Documents/doble-venganza-la-conspiracion-helix/imagenes/Laser/espejo2.png'), (TILE_SIZE, TILE_SIZE))
mirror_left_img = pygame.transform.scale(pygame.image.load('C:/Users/siimi/Documents/doble-venganza-la-conspiracion-helix/imagenes/Laser/espejo3.png'), (TILE_SIZE, TILE_SIZE))
mirror_right_img = pygame.transform.scale(pygame.image.load('C:/Users/siimi/Documents/doble-venganza-la-conspiracion-helix/imagenes/Laser/espejo4.png'), (TILE_SIZE, TILE_SIZE))
start_img = pygame.transform.scale(pygame.image.load('C:/Users/siimi/Documents/doble-venganza-la-conspiracion-helix/imagenes/Laser/inicio.png'), (TILE_SIZE, TILE_SIZE))

# Clase del laser
class LaserPuzzle:
    def __init__(self, grid_size):
        self.grid_size = grid_size
        self.grid = [[' ' for _ in range(grid_size)] for _ in range(grid_size)]
        self.laser_position = (1, 0)
        self.door_position = (grid_size - 1, grid_size - 1)
        self.mirrors = []
        self.door_open = False
        self.door_close = True
    
    # Metodos para colocar el laser, la puerta y los espejos
    def place_laser(self, x, y):
        self.laser_position = (x, y)
        self.grid[y][x] = 'L'

    def place_door(self, x, y):
        self.door_position = (x, y)
        self.grid[y][x] = 'D'

    def place_mirror(self, x, y, direction):
        self.mirrors.append((x, y, direction))
        self.grid[y][x] = direction

    def display_grid(self):
        for row in self.grid:
            print(' '.join(row))

    # Metodo para dibujar el tablero con las imagenes
    def draw(self):
        for y in range(self.grid_size):
            for x in range(self.grid_size):
                rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                pygame.draw.rect(screen, GRAY, rect, 1)
                if (x, y) == (0, 0):
                    screen.blit(start_img, rect)
                elif self.grid[y][x] == 'L':
                    screen.blit(laser_img_horizontal, rect)
                elif self.grid[y][x] == 'D':
                    if self.door_open:
                        screen.blit(door_open_img, rect)
                    else:
                        screen.blit(door_closed_img, rect)
                elif self.grid[y][x] == 'up':
                    screen.blit(mirror_up_img, rect)
                elif self.grid[y][x] == 'down':
                    screen.blit(mirror_down_img, rect)
                elif self.grid[y][x] == 'left':
                    screen.blit(mirror_left_img, rect)
                elif self.grid[y][x] == 'right':
                    screen.blit(mirror_right_img, rect)
    # Funcion para hacer rotar los espejos
    def rotate_mirror(self, x, y):
        for i, (mx, my, direction) in enumerate(self.mirrors):
            if mx == x and my == y:
                new_direction = {
                    'up': 'right',
                    'right': 'down',
                    'down': 'left',
                    'left': 'up'
                }[direction]
                self.mirrors[i] = (x, y, new_direction)
                self.grid[y][x] = new_direction
                break
    # Metodo para ver si el puzzle esta resuelto
    def solve_puzzle(self):
        laser_x, laser_y = self.laser_position
        direction = 'right'
        while 0 <= laser_x < self.grid_size and 0 <= laser_y < self.grid_size:
            if (laser_x, laser_y) == self.door_position:
                self.door_open = True
                self.door_close = False
                return True
            if self.grid[laser_y][laser_x] == 'up':
                if direction == 'right':
                    direction = 'up'
                elif direction == 'left':
                    direction = 'down'
                elif direction == 'up':
                    direction = 'right'
                elif direction == 'down':
                    direction = 'left'
            elif self.grid[laser_y][laser_x] == 'down':
                if direction == 'right':
                    direction = 'down'
                elif direction == 'left':
                    direction = 'up'
                elif direction == 'up':
                    direction = 'left'
                elif direction == 'down':
                    direction = 'right'
            elif self.grid[laser_y][laser_x] == 'left':
                if direction == 'right':
                    direction = 'left'
                elif direction == 'left':
                    direction = 'right'
                elif direction == 'up':
                    direction = 'down'
                elif direction == 'down':
                    direction = 'up'
            elif self.grid[laser_y][laser_x] == 'right':
                if direction == 'right':
                    direction = 'right'
                elif direction == 'left':
                    direction = 'left'
                elif direction == 'up':
                    direction = 'up'
                elif direction == 'down':
                    direction = 'down'
            if direction == 'right':
                laser_x += 1
            elif direction == 'left':
                laser_x -= 1
            elif direction == 'up':
                laser_y -= 1
            elif direction == 'down':
                laser_y += 1
        return False
    
    # Metodo para dibujar el camino del laser
    def draw_laser_path(self):
        laser_x, laser_y = self.laser_position
        direction = 'right'
        while 0 <= laser_x < self.grid_size and 0 <= laser_y < self.grid_size:
            rect = pygame.Rect(laser_x * TILE_SIZE, laser_y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
            if direction in ['up', 'down']:
                screen.blit(laser_img_vertical, rect)
            else:
                screen.blit(laser_img_horizontal, rect)
            if (laser_x, laser_y) == self.door_position:
                break
            if self.grid[laser_y][laser_x] == 'up':
                if direction == 'right':
                    direction = 'up'
                elif direction == 'left':
                    direction = 'down'
                elif direction == 'up':
                    direction = 'right'
                elif direction == 'down':
                    direction = 'left'
            elif self.grid[laser_y][laser_x] == 'down':
                if direction == 'right':
                    direction = 'down'
                elif direction == 'left':
                    direction = 'up'
                elif direction == 'up':
                    direction = 'left'
                elif direction == 'down':
                    direction = 'right'
            elif self.grid[laser_y][laser_x] == 'left':
                if direction == 'right':
                    direction = 'left'
                elif direction == 'left':
                    direction = 'right'
                elif direction == 'up':
                    direction = 'down'
                elif direction == 'down':
                    direction = 'up'
            elif self.grid[laser_y][laser_x] == 'right':
                if direction == 'right':
                    direction = 'right'
                elif direction == 'left':
                    direction = 'left'
                elif direction == 'up':
                    direction = 'up'
                elif direction == 'down':
                    direction = 'down'
            if direction == 'right':
                laser_x += 1
            elif direction == 'left':
                laser_x -= 1
            elif direction == 'up':
                laser_y -= 1
            elif direction == 'down':
                laser_y += 1

# Funcion para limpiar la imagen del candado cerrado
def clear_image(x, y):
    rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
    pygame.draw.rect(screen, BLACK, rect)  
    pygame.display.update(rect) 

# Ponemos las cosas en su posición
puzzle = LaserPuzzle(GRID_SIZE)
puzzle.place_laser(1, 0)
puzzle.place_door(4, 4)
puzzle.place_mirror(2, 2, 'up')
puzzle.place_mirror(2, 4, 'up')
puzzle.place_mirror(2, 0, 'up')  

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos
            grid_x = mouse_x // TILE_SIZE
            grid_y = mouse_y // TILE_SIZE
            if puzzle.grid[grid_y][grid_x] in ['up', 'down', 'left', 'right']:
                puzzle.rotate_mirror(grid_x, grid_y)

    screen.fill(BLACK)
    puzzle.draw()
    puzzle.draw_laser_path()
    pygame.display.flip()

    if puzzle.solve_puzzle():
        clear_image(puzzle.door_position[0], puzzle.door_position[1])  # Limpiamos la imagen del candado cerrado
        puzzle.door_open = True
        puzzle.draw()
        pygame.display.flip()
        font = pygame.font.Font(None, 74)
        text = font.render("¡Felicidades!", True, WHITE)
        screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2 - text.get_height() // 2))
        pygame.display.flip()
        pygame.time.wait(3000)
        running = False

pygame.quit()