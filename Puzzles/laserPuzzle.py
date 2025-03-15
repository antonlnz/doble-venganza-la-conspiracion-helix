import pygame
import sys
from escena import *
import os

pygame.init()

class LaserPuzzle(Escena):
    def __init__(self, director):
        Escena.__init__(self, director)
        # Center the window on the screen
        os.environ['SDL_VIDEO_CENTERED'] = '1'
        # Constantes
        self.SCREEN_WIDTH = 1920  
        self.SCREEN_HEIGHT = 1080
        self.grid_size = 5  # Set grid_size to 6
        self.TILE_WIDTH = (min(self.SCREEN_WIDTH, self.SCREEN_HEIGHT) * 0.9) // self.grid_size  # Adjust TILE_WIDTH to be 90% of the smaller screen dimension
        self.TILE_HEIGHT = self.TILE_WIDTH * 0.8  # Make TILE_HEIGHT 80% of TILE_WIDTH
        self.grid_offset_x = (self.SCREEN_WIDTH - (self.TILE_WIDTH * self.grid_size)) // 2  # Calculate horizontal offset
        self.grid_offset_y = (self.SCREEN_HEIGHT - (self.TILE_HEIGHT * self.grid_size)) // 2  # Calculate vertical offset
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.RED = (255, 0, 0)
        self.GREEN = (0, 255, 0)
        self.BLUE = (0, 0, 255)
        self.GRAY = (200, 200, 200)

        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        pygame.display.set_caption("Laser Puzzle")

        # Imagenes
        scale_factor = 0.8
        self.laser_img_horizontal = pygame.transform.rotate(pygame.image.load('imagenes/Laser/laser.png'), 90)
        self.laser_img_vertical = pygame.image.load('imagenes/Laser/laser.png')
        self.door_closed_img = pygame.transform.scale(pygame.image.load('imagenes/Laser/cadeado_fechado.png'), (int(self.TILE_WIDTH * scale_factor), int(self.TILE_HEIGHT * scale_factor)))
        self.door_open_img = pygame.transform.scale(pygame.image.load('imagenes/Laser/cadeado_aberto.png'), (int(self.TILE_WIDTH * scale_factor), int(self.TILE_HEIGHT * scale_factor)))
        self.mirror_up_img = pygame.transform.scale(pygame.image.load('imagenes/Laser/espejo.png'), (int(self.TILE_WIDTH * scale_factor), int(self.TILE_HEIGHT * scale_factor)))
        self.mirror_down_img = pygame.transform.scale(pygame.image.load('imagenes/Laser/espejo2.png'), (int(self.TILE_WIDTH * scale_factor), int(self.TILE_HEIGHT * scale_factor)))
        self.mirror_left_img = pygame.transform.scale(pygame.image.load('imagenes/Laser/espejo3.png'), (int(self.TILE_WIDTH * scale_factor), int(self.TILE_HEIGHT * scale_factor)))
        self.mirror_right_img = pygame.transform.scale(pygame.image.load('imagenes/Laser/espejo4.png'), (int(self.TILE_WIDTH * scale_factor), int(self.TILE_HEIGHT * scale_factor)))
        self.start_img = pygame.transform.scale(pygame.image.load('imagenes/Laser/inicio.png'), (int(self.TILE_WIDTH * scale_factor), int(self.TILE_HEIGHT * scale_factor)))

        self.background_img = pygame.image.load('imagenes/Laser/mecanismo_laser.jpg')
        self.background_img = pygame.transform.scale(self.background_img, (self.SCREEN_WIDTH, self.SCREEN_HEIGHT))

        self.grid = [[' ' for _ in range(self.grid_size)] for _ in range(self.grid_size)]
        self.laser_position = (1, 0)
        self.door_position = (self.grid_size - 1, self.grid_size - 1)
        self.mirrors = []
        self.door_open = False
        self.door_close = True
        self.running = True

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

    def draw(self):
        self.screen.blit(self.background_img, (0, 0))  # Draw the background image
        for y in range(self.grid_size):
            for x in range(self.grid_size):
                rect = pygame.Rect(self.grid_offset_x + x * self.TILE_WIDTH, self.grid_offset_y + y * self.TILE_HEIGHT, self.TILE_WIDTH, self.TILE_HEIGHT)
                pygame.draw.rect(self.screen, self.BLACK, rect)  # Draw black background for each cell
                pygame.draw.rect(self.screen, self.GRAY, rect, 1)  # Draw gray border for each cell
                if (x, y) == (0, 0):
                    self.screen.blit(self.start_img, rect.move((self.TILE_WIDTH - self.start_img.get_width()) // 2, (self.TILE_HEIGHT - self.start_img.get_height()) // 2))
                elif self.grid[y][x] == 'L':
                    self.screen.blit(self.laser_img_horizontal, rect)
                elif self.grid[y][x] == 'D':
                    if self.door_open:
                        self.screen.blit(self.door_open_img, rect.move((self.TILE_WIDTH - self.door_open_img.get_width()) // 2, (self.TILE_HEIGHT - self.door_open_img.get_height()) // 2))
                    else:
                        self.screen.blit(self.door_closed_img, rect.move((self.TILE_WIDTH - self.door_closed_img.get_width()) // 2, (self.TILE_HEIGHT - self.door_closed_img.get_height()) // 2))
                elif self.grid[y][x] == 'up':
                    self.screen.blit(self.mirror_up_img, rect.move((self.TILE_WIDTH - self.mirror_up_img.get_width()) // 2, (self.TILE_HEIGHT - self.mirror_up_img.get_height()) // 2))
                elif self.grid[y][x] == 'down':
                    self.screen.blit(self.mirror_down_img, rect.move((self.TILE_WIDTH - self.mirror_down_img.get_width()) // 2, (self.TILE_HEIGHT - self.mirror_down_img.get_height()) // 2))
                elif self.grid[y][x] == 'left':
                    self.screen.blit(self.mirror_left_img, rect.move((self.TILE_WIDTH - self.mirror_left_img.get_width()) // 2, (self.TILE_HEIGHT - self.mirror_left_img.get_height()) // 2))
                elif self.grid[y][x] == 'right':
                    self.screen.blit(self.mirror_right_img, rect.move((self.TILE_WIDTH - self.mirror_right_img.get_width()) // 2, (self.TILE_HEIGHT - self.mirror_right_img.get_height()) // 2))

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

    def draw_laser_path(self):
        laser_x, laser_y = self.laser_position
        direction = 'right'
        while 0 <= laser_x < self.grid_size and 0 <= laser_y < self.grid_size:
            rect = pygame.Rect(self.grid_offset_x + laser_x * self.TILE_WIDTH, self.grid_offset_y + laser_y * self.TILE_HEIGHT, self.TILE_WIDTH, self.TILE_HEIGHT)
            if direction in ['up', 'down']:
                self.screen.blit(self.laser_img_vertical, rect)
            else:
                self.screen.blit(self.laser_img_horizontal, rect)
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

    def clear_image(self, x, y):
        rect = pygame.Rect(x * self.TILE_WIDTH, y * self.TILE_HEIGHT, self.TILE_WIDTH, self.TILE_HEIGHT)
        pygame.draw.rect(self.screen, self.BLACK, rect)
        pygame.display.update(rect)

    def run(self):
        self.place_laser(1, 0)
        self.place_door(4, 4)
        self.place_mirror(2, 2, 'up')
        self.place_mirror(2, 4, 'up')
        self.place_mirror(2, 0, 'up')

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = event.pos
                    grid_x = int((mouse_x - self.grid_offset_x) // self.TILE_WIDTH)
                    grid_y = int((mouse_y - self.grid_offset_y) // self.TILE_HEIGHT)
                    if 0 <= grid_x < self.grid_size and 0 <= grid_y < self.grid_size:
                        if self.grid[grid_y][grid_x] in ['up', 'down', 'left', 'right']:
                            self.rotate_mirror(grid_x, grid_y)

            self.screen.fill(self.BLACK)
            self.draw()
            self.draw_laser_path()
            pygame.display.flip()

            if self.solve_puzzle():
                self.clear_image(self.door_position[0], self.door_position[1])
                self.door_open = True
                self.draw()
                # Paint the tile black and place the open lock image
                rect = pygame.Rect(self.grid_offset_x + self.door_position[0] * self.TILE_WIDTH, self.grid_offset_y + self.door_position[1] * self.TILE_HEIGHT, self.TILE_WIDTH, self.TILE_HEIGHT)
                pygame.draw.rect(self.screen, self.BLACK, rect)
                self.screen.blit(self.door_open_img, rect.move((self.TILE_WIDTH - self.door_open_img.get_width()) // 2, (self.TILE_HEIGHT - self.door_open_img.get_height()) // 2))
                pygame.display.flip()
                font = pygame.font.Font(None, 74)
                text = font.render("¡Felicidades!", True, self.BLACK)  # Change text color to black for better contrast
                # Draw a white line behind the text
                line_rect = pygame.Rect(0, self.SCREEN_HEIGHT // 2 - text.get_height() // 2, self.SCREEN_WIDTH, text.get_height())
                pygame.draw.rect(self.screen, self.WHITE, line_rect)
                self.screen.blit(text, (self.SCREEN_WIDTH // 2 - text.get_width() // 2, self.SCREEN_HEIGHT // 2 - text.get_height() // 2))
                pygame.display.flip()
                pygame.time.wait(3000)
                self.running = False

        pygame.quit()

    def update(self, tiempo):
        self.run()

    def eventos(self, eventos):
        for event in eventos:
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                grid_x = int((mouse_x - self.grid_offset_x) // self.TILE_WIDTH)
                grid_y = int((mouse_y - self.grid_offset_y) // self.TILE_HEIGHT)
                if 0 <= grid_x < self.grid_size and 0 <= grid_y < self.grid_size:
                    if self.grid[grid_y][grid_x] in ['up', 'down', 'left', 'right']:
                        self.rotate_mirror(grid_x, grid_y)

    def dibujar(self, pantalla):
        self.screen.fill(self.BLACK)
        self.draw()
        self.draw_laser_path()
        pygame.display.flip()

if __name__ == "__main__":
    director = None  # Replace with actual director object
    puzzle = LaserPuzzle(director)
    puzzle.run()