import pygame
import os
import random
import time
from escena import *

pygame.init()

class Pipe(Escena):
    def __init__(self, director):
        Escena.__init__(self, director)
        os.environ['SDL_VIDEO_CENTERED'] = '1'
        # Constantes
        self.SCREEN_WIDTH = 1920
        self.SCREEN_HEIGHT = 1080
        self.TILE_SIZE = self.SCREEN_WIDTH // 8  # 8 tiles horizontally
        self.GRID_WIDTH = 8
        self.GRID_HEIGHT = 6  # 6 tiles vertically

        # Colores
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)

        # Pantalla
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        pygame.display.set_caption("Pipe Puzzle")

        # Fotos en imagenes/Tuberias
        self.background_img = pygame.image.load('imagenes/Tuberias/fondo.jpg')
        self.background_img = pygame.transform.scale(self.background_img, (self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        self.horizontal_img = pygame.image.load('imagenes/Tuberias/horizontal/pipe_horizontal.png')
        self.horizontal_img = pygame.transform.scale(self.horizontal_img, (self.TILE_SIZE, self.TILE_SIZE))
        self.vertical_img = pygame.image.load('imagenes/Tuberias/vertical/pipe_vertical.png')
        self.vertical_img = pygame.transform.scale(self.vertical_img, (self.TILE_SIZE, self.TILE_SIZE))
        self.corner_tl_img = pygame.image.load('imagenes/Tuberias/top_left/pipe_corner_top_left.png')
        self.corner_tl_img = pygame.transform.scale(self.corner_tl_img, (self.TILE_SIZE, self.TILE_SIZE))
        self.corner_tr_img = pygame.image.load('imagenes/Tuberias/top_right/pipe_corner_top_right.png')
        self.corner_tr_img = pygame.transform.scale(self.corner_tr_img, (self.TILE_SIZE, self.TILE_SIZE))
        self.corner_bl_img = pygame.image.load('imagenes/Tuberias/bottom_left/pipe_corner_bottom_left.png')
        self.corner_bl_img = pygame.transform.scale(self.corner_bl_img, (self.TILE_SIZE, self.TILE_SIZE))
        self.corner_br_img = pygame.image.load('imagenes/Tuberias/bottom_right/pipe_corner_bottom_right.png')
        self.corner_br_img = pygame.transform.scale(self.corner_br_img, (self.TILE_SIZE, self.TILE_SIZE))

        # Este sería el estado inicial del puzzle (no esta muy dificil)
        self.path = [
            (0, self.GRID_HEIGHT // 2, 'horizontal'),
            (1, self.GRID_HEIGHT // 2, 'horizontal'),
            (2, self.GRID_HEIGHT // 2, 'corner_tr'),
            (2, self.GRID_HEIGHT // 2 - 1, 'vertical'),
            (2, self.GRID_HEIGHT // 2 - 2, 'corner_br'),
            (3, self.GRID_HEIGHT // 2 - 2, 'horizontal'),
            (4, self.GRID_HEIGHT // 2 - 2, 'horizontal'),
            (5, self.GRID_HEIGHT // 2 - 2, 'corner_bl'),
            (5, self.GRID_HEIGHT // 2 - 1, 'vertical'),
            (5, self.GRID_HEIGHT // 2, 'corner_tl'),
            (6, self.GRID_HEIGHT // 2, 'horizontal'),
            (7, self.GRID_HEIGHT // 2, 'horizontal')
        ]

        # Este sería el estado final del puzzle(Las rotaciones son con la imagagen correcta)
        self.solution_path = [
            (0, self.GRID_HEIGHT // 2, 'horizontal'),
            (1, self.GRID_HEIGHT // 2, 'horizontal'),
            (2, self.GRID_HEIGHT // 2, 'corner_tl'),  # Cambiada
            (2, self.GRID_HEIGHT // 2 - 1, 'vertical'),
            (2, self.GRID_HEIGHT // 2 - 2, 'corner_br'),
            (3, self.GRID_HEIGHT // 2 - 2, 'horizontal'),
            (4, self.GRID_HEIGHT // 2 - 2, 'horizontal'),
            (5, self.GRID_HEIGHT // 2 - 2, 'corner_bl'),
            (5, self.GRID_HEIGHT // 2 - 1, 'vertical'),
            (5, self.GRID_HEIGHT // 2, 'corner_tr'),  # Cambiada
            (6, self.GRID_HEIGHT // 2, 'horizontal'),
            (7, self.GRID_HEIGHT // 2, 'horizontal')
        ]

        # Inicializar la cuadrícula y agregar tuberías
        self.grid = [[None for _ in range(self.GRID_WIDTH)] for _ in range(self.GRID_HEIGHT)]
        for x, y, pipe_type in self.path:
            self.grid[y][x] = {'x': x, 'y': y, 'type': pipe_type}

        self.elapsed_time = 0
        self.start_time = None
        self.running = True
        self.end_time = None  # Añadido para manejar el tiempo de espera
        self.message = None  # Añadido para manejar los mensajes

    def draw(self):
        if self.type == 'horizontal':
            img = self.horizontal_img
        elif self.type == 'vertical':
            img = self.vertical_img
        elif self.type == 'corner_tl':
            img = self.corner_tl_img
        elif self.type == 'corner_tr':
            img = self.corner_tr_img
        elif self.type == 'corner_bl':
            img = self.corner_bl_img
        elif self.type == 'corner_br':
            img = self.corner_br_img
        self.screen.blit(img, (self.x * self.TILE_SIZE, self.y * self.TILE_SIZE))

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

    def is_solved(grid, solution_path):
        for x, y, pipe_type in solution_path:
            if grid[y][x]['type'] != pipe_type:
                return False
        return True

    def update(self, tiempo):
        # Comprobar si el tiempo se ha acabado
        if self.start_time is None:
            self.start_time = time.time()
        self.elapsed_time = time.time() - self.start_time
        if self.elapsed_time >= 20:
            self.message = "Perdiste"
            self.running = False
            self.end_time = time.time()

        # Miramos si esta resuelto
        if Pipe.is_solved(self.grid, self.solution_path):
            self.message = "¡Felicidades!"
            self.running = False
            self.end_time = time.time()

    def eventos(self, eventos):
        for event in eventos:
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                self.running = False
                self.director.salirEscena() 
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.start_time is None:
                    self.start_time = time.time()
                mouse_x, mouse_y = event.pos
                grid_x = mouse_x // self.TILE_SIZE
                grid_y = mouse_y // self.TILE_SIZE
                if 0 <= grid_x < self.GRID_WIDTH and 0 <= grid_y < self.GRID_HEIGHT and self.grid[grid_y][grid_x] is not None:
                    self.rotate_pipe(grid_y, grid_x)

    def rotate_pipe(self, y, x):
        pipe = self.grid[y][x]
        if pipe['type'] == 'horizontal':
            pipe['type'] = 'vertical'
        elif pipe['type'] == 'vertical':
            pipe['type'] = 'horizontal'
        elif pipe['type'] == 'corner_tl':
            pipe['type'] = 'corner_tr'
        elif pipe['type'] == 'corner_tr':
            pipe['type'] = 'corner_br'
        elif pipe['type'] == 'corner_br':
            pipe['type'] = 'corner_bl'
        elif pipe['type'] == 'corner_bl':
            pipe['type'] = 'corner_tl'

    def dibujar(self, pantalla):
        self.screen.blit(self.background_img, (0, 0))

        for row in self.grid:
            for pipe in row:
                if pipe is not None:
                    self.draw_pipe(pipe)

        # Dibujar el tiempo restante (20s)
        self.elapsed_time = time.time() - self.start_time
        remaining_time = max(0, 20 - int(self.elapsed_time))
        font = pygame.font.Font(None, 148)  # Increase font size
        timer_text = font.render(f"Tiempo: {remaining_time}", True, self.BLACK)
        timer_rect = timer_text.get_rect(center=(self.SCREEN_WIDTH // 2, 200))
        self.screen.blit(timer_text, timer_rect)

        # Mostrar mensaje si hay
        if self.message:
            # Dibujar línea blanca
            pygame.draw.rect(self.screen, self.WHITE, (0, self.SCREEN_HEIGHT // 2 - 50, self.SCREEN_WIDTH, 100))
            text = font.render(self.message, True, self.BLACK)
            self.screen.blit(text, (self.SCREEN_WIDTH // 2 - text.get_width() // 2, self.SCREEN_HEIGHT // 2 - text.get_height() // 2))
            pygame.display.flip()
            if self.retardo():
                self.completado = True
                self.director.salirEscena()
        else:
            pygame.display.flip()

    def draw_pipe(self, pipe):
        if pipe['type'] == 'horizontal':
            img = self.horizontal_img
        elif pipe['type'] == 'vertical':
            img = self.vertical_img
        elif pipe['type'] == 'corner_tl':
            img = self.corner_tl_img
        elif pipe['type'] == 'corner_tr':
            img = self.corner_tr_img
        elif pipe['type'] == 'corner_bl':
            img = self.corner_bl_img
        elif pipe['type'] == 'corner_br':
            img = self.corner_br_img
        self.screen.blit(img, (pipe['x'] * self.TILE_SIZE, pipe['y'] * self.TILE_SIZE))

if __name__ == "__main__":
    Pipe.main()
