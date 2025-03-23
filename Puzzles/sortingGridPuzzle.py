import math
import random
import pygame
from settings import *
from escena import Escena
import os


class SortingGridPuzzle(Escena):
    
    def __init__(self, director):
        Escena.__init__(self, director)
        os.environ['SDL_VIDEO_CENTERED'] = '1'
        pygame.mixer.pre_init(44100, 16, 3, 4096)
        pygame.mixer.init()

        self.background = pygame.image.load("imagenes/Grid/Background.jpg")
        self.background = pygame.transform.scale(self.background, (WIDTH, HEIGHT))

        self.grid_size = 3
        self.gridX = 660 #1920 - 600 = 1320 / 2 = 660
        self.gridY = 240 #1080 - 600 = 480 / 2 = 240
        self.tile_size = 200 

        self.background_tile = pygame.image.load("imagenes/Grid/Tiles.jpg")
        self.background_tile = pygame.transform.scale(self.background_tile, (self.tile_size, self.tile_size))
  
        self.font = pygame.font.Font("Fuentes/Orbitron-ExtraBold.ttf", 65)
        self.timer_font = pygame.font.Font("Fuentes/SevenSegment.ttf", 70)
        self.game_over_font = pygame.font.Font("Fuentes/PricedownBl.otf", 70)

        self.sound_timer = pygame.mixer.Sound("Sonidos/cronometro.wav")
        self.sound_end_game = pygame.mixer.Sound("Sonidos/endgame.wav")
        self.sound_completed = pygame.mixer.Sound("Sonidos/completed.wav")
        self.sound_warning = pygame.mixer.Sound("Sonidos/warning.mp3")

        self.numbers = self.generate_puzzle()

        self.positions = [(col, row) for row in range(self.grid_size) for col in range(self.grid_size)]

        self.expected_result = [1, 2, 3, 4, 5, 6, 7, 8, 0]

        self.mouse_clicks = None
        self.click = False

        self.empty = self.positions[self.numbers.index(0)]  # Encuentra la posición del espacio vacío

        self.time_limit = 90000 
        self.time_remaining = self.time_limit
        self.completion_time = 3000
        self.completion_time_remaining = self.completion_time

        # Variables para animación de tiempo
        self.timer_alpha = 255
        self.timer_pulsing = False
        self.timer_pulse_speed = 0.01
        
        # Variables para el halo rojo
        self.red_halo_active = False
        self.halo_alpha = 0
        self.halo_max_alpha = 100

        self.fail = False

    def count_inversions(self, numbers): 
        inversions = 0
        list_num =  [n for n in numbers if n != 0]
        for i in range(len(list_num)):
            for j in range(i + 1, len(list_num)):
                if list_num[i] > list_num[j]:
                    inversions += 1
        return inversions
                
    def generate_puzzle(self):
        while True:
            numeros = list(range(1, self.grid_size*self.grid_size))
            numeros.append(0)
            random.shuffle(numeros)

            inversions = self.count_inversions(numeros)

            if inversions % 2 == 0:
                return numeros           

    def move(self, pos):
        x, y = pos
        col = int((x - self.gridX) / self.tile_size)
        row = int((y - self.gridY) / self.tile_size)
        if self.gridX <= x <= self.gridX + self.tile_size * self.grid_size and self.gridY <= y <= self.gridY + self.tile_size * self.grid_size:
            if 0 <= col < self.grid_size and 0 <= row < self.grid_size:
                self.mouse_clicks = (col, row)
                self.click = True

    def game_over(self, screen):
        screen.fill(NEGRO)
        game_over_text = self.font.render('You lose', True, ROJO)
        screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - game_over_text.get_height() // 2))
        pygame.display.flip()
        self.sound_end_game.play()
        self.sound_end_game.stop()
        self.completado = True

    def dibujar(self, pantalla):
        pantalla.blit(self.background, (0, 0))

        pygame.draw.rect(pantalla, NEGRO, (655, 235, self.tile_size*3 + 10 , self.tile_size*3 + 10))

        seconds_left = max(0, int(self.time_remaining / 1000))
        time_text = f"{seconds_left}"

        for i, (col, row) in enumerate(self.positions):
            if self.numbers[i] != 0:

                pantalla.blit(self.background_tile, (col*self.tile_size + self.gridX, row*self.tile_size + self.gridY, self.tile_size, self.tile_size))

                pygame.draw.rect(pantalla, NEGRO, (col*self.tile_size + self.gridX, row*self.tile_size + self.gridY, self.tile_size, self.tile_size), 5)

                number_text = self.font.render(str(self.numbers[i]), True, NEGRO)
                text_rect = number_text.get_rect(center=(self.gridX + col*self.tile_size + self.tile_size/2, self.gridY + row*self.tile_size + self.tile_size/2 ))
                pantalla.blit(number_text, text_rect)

        if seconds_left <= 30:
            # Crear una superficie con canal alfa para el parpadeo
            time_color = ROJO
            time_surface = self.timer_font.render(time_text, True, time_color)
            time_rect = time_surface.get_rect(center=(960, 200))
            time_surface_alpha = pygame.Surface(time_surface.get_size(), pygame.SRCALPHA)
            time_surface_alpha.fill((255, 0, 0, int(self.timer_alpha)))
            time_surface.blit(time_surface_alpha, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
        else:
            time_color = NEGRO
            time_surface = self.timer_font.render(time_text, True, time_color)
            time_rect = time_surface.get_rect(center=(960, 200))
            
        pantalla.blit(time_surface, time_rect)

        # Dibujar el halo rojo en los últimos 10 segundos
        if seconds_left <= 15 and self.red_halo_active:
            # Crear una superficie semitransparente para el halo
            halo_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
                
            # Crear un efecto de halo continuo al rededor del borde del panel
            border_size = 100  # Tamaño del borde donde se concentra el efecto
                
            # En lugar de dibujar líneas separadas, dibujamos un rectángulo con degradado
            for grosor in range(border_size):
                # Calcular alfa basado en distancia al borde (más opaco en los bordes)
                alpha = int((self.halo_alpha * (border_size - grosor) / border_size))
                
                # Dibujar un rectángulo completo (contorno) para cada nivel de opacidad
                pygame.draw.rect(halo_surface, (255, 0, 0, alpha), 
                                (grosor, grosor, WIDTH - 2 * grosor, HEIGHT - 2 * grosor), 1)
                
            pantalla.blit(halo_surface, (0, 0))

        if self.completado:
            for i, (col, row) in enumerate(self.positions):
                pantalla.blit(self.background_tile, (col*self.tile_size + self.gridX, row*self.tile_size + self.gridY, self.tile_size, self.tile_size))

        if self.fail:
            self.game_over(pantalla)

    def update(self, tiempo):
        if self.click:
            empty_col, empty_row = self.empty
            col, row = self.mouse_clicks
            empty_index = self.positions.index(self.empty)
            click_index = self.positions.index(self.mouse_clicks)   
            if ((abs(empty_row - row) == 1 and empty_col == col) or (abs(empty_col - col) == 1 and empty_row == row)) :
                self.numbers[empty_index], self.numbers[click_index] = self.numbers[click_index], self.numbers[empty_index]
                self.empty = (col, row)
            self.click = False

        if self.numbers == self.expected_result:
            if pygame.mixer.get_busy():
                self.sound_timer.stop()
            self.completion_time_remaining -= tiempo
            self.completado = True
            self.sound_completed.play()
            if self.completion_time_remaining <= 0:
                self.sound_completed.stop()
        
        if not self.completado:
            self.time_remaining -= tiempo
            segundos_restantes = max(0, int(self.time_remaining / 1000))

            # Activar efectos de parpadeo en los últimos 15 segundos
            if segundos_restantes <= 30:
                self.timer_pulsing = True
                # Calcular valor de alfa para el parpadeo del temporizador (oscila entre 100 y 255)
                self.timer_alpha = 100 + 155 * (0.5 + 0.5 * math.sin(pygame.time.get_ticks() * self.timer_pulse_speed))
            else:
                self.timer_pulsing = False
                self.timer_alpha = 255
                
            # Activar el halo rojo en los últimos 10 segundos
            if segundos_restantes <= 15:
                self.red_halo_active = True
                # Calcular valor de alfa para el halo (oscila entre 0 y max_alpha)
                self.halo_alpha = self.halo_max_alpha * (0.5 + 0.5 * math.sin(pygame.time.get_ticks() * 0.005))
            else:
                self.red_halo_active = False
                
            # Verificar si se acabó el tiempo
            if self.time_remaining <= 0:
                self.time_remaining = 0
                self.fail = True
                self.sound_timer.stop()
                self.sound_warning.stop()

            if segundos_restantes <= 30 and segundos_restantes > 15:
                if not pygame.mixer.get_busy():
                    self.sound_timer.play(1)
                
            if segundos_restantes == 15:
                self.sound_warning.play()

        if self.completado:
            if self.retardo():
                self.director.salirEscena()

    def eventos(self, eventos):
        for evento in eventos:
            if evento.type == pygame.QUIT:
                self.director.salirEscena()
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if evento.button == 1:
                    self.move(evento.pos)

if __name__ == "__main__":
    director = None  # Replace with actual director object if available
    gridPuzzle = SortingGridPuzzle(director)
    gridPuzzle.run()