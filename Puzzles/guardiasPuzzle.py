import pygame
import random
import time
import sys
from escena import *
import os

# Configuración de la pantalla

# Colores

# Guardias
class Guardia(Escena):
    def __init__(self, director, x=0, y=0, image=None):
        Escena.__init__(self, director)
        pygame.init()
        os.environ['SDL_VIDEO_CENTERED'] = '1'
        self.WIDTH, self.HEIGHT = 1920, 1080
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Guardias Puzzle")
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.RED = (255, 0, 0)
        self.GREEN = (0, 255, 0)
        self.font = pygame.font.Font(None, 148)  # Adjust font size for larger screen
        # Cargar y escalar imagen de fondo
        self.background_image = pygame.image.load('imagenes/Guardias/fondo_banco2.jpg')
        self.background_image = pygame.transform.scale(self.background_image, (1920, 1080))

        # Cargar y escalar imágenes de corazones
        self.heart_full = pygame.image.load('imagenes/Guardias/heart_full_16x16.png')
        self.heart_empty = pygame.image.load('imagenes/Guardias/heart_empty_16x16.png')
        self.heart_full = pygame.transform.scale(self.heart_full, (48, 48))
        self.heart_empty = pygame.transform.scale(self.heart_empty, (48, 48))

        # Cargar imágenes de guardias
        self.policeman_image = pygame.image.load('imagenes/Guardias/Policeman.png')
        self.policewoman_image = pygame.image.load('imagenes/Guardias/Policewoman.png')
        self.policeman_image = pygame.transform.scale(self.policeman_image, (400, 400))
        self.policewoman_image = pygame.transform.scale(self.policewoman_image, (400, 400))
        self.x = x
        self.y = y
        self.image = image if image else self.policeman_image
        self.sequence = self.generate_sequence()
        self.current_index = 0
        self.health = len(self.sequence)
        self.wrong_key = False
        self.lives = 3
        self.last_key_time = time.time()
        self.start_time = time.time()
        self.time_limits = [10, 7, 5]  # Tiempos para cada guardia
        self.current_guardia_index = 0
        self.running = True
        self.remaining_time = self.time_limits[self.current_guardia_index]
        self.imagenes_guardias = [
            self.policeman_image,
            self.policewoman_image,
            self.policeman_image
        ]

    def generate_sequence(self):
        return [random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ') for _ in range(5)]

    def draw(self, screen):
        screen.blit(self.image, (self.WIDTH // 2 - self.image.get_width() // 2, self.HEIGHT // 2 - self.image.get_height() // 2 + 200))  # Move the image further down
        correct_text = self.font.render(''.join(self.sequence[:self.current_index]), True, self.GREEN)
        if self.wrong_key:
            remaining_text = self.font.render(''.join(self.sequence[self.current_index:self.current_index + 1]), True, self.RED)
        else:
            remaining_text = self.font.render(''.join(self.sequence[self.current_index:self.current_index + 1]), True, self.BLACK)
        text_x = (self.WIDTH - correct_text.get_width() - remaining_text.get_width()) // 2
        screen.blit(correct_text, (text_x, 320))
        screen.blit(remaining_text, (text_x + correct_text.get_width(), 320))

    def check_key(self, key):
        if self.current_index < len(self.sequence) and key == self.sequence[self.current_index]:
            self.current_index += 1
            self.wrong_key = False
            if self.current_index == len(self.sequence):
                self.current_index = 0  # Reiniciar el índice de la secuencia
                self.sequence = self.generate_sequence()  # Generar una nueva secuencia
                self.start_time = time.time()  # Reiniciar el tiempo de inicio
                self.current_guardia_index += 1
                if self.current_guardia_index >= len(self.time_limits):
                    self.running = False
                else:
                    self.remaining_time = self.time_limits[self.current_guardia_index]  # Actualizar el tiempo restante
                    self.image = self.imagenes_guardias[self.current_guardia_index]  # Actualizar la imagen del guardia
                return True
        else:
            self.wrong_key = True
        return False

    def eventos(self, eventos):
        for event in eventos:
            if event.type == pygame.QUIT:
                self.director.salirPrograma()
            elif event.type == pygame.KEYDOWN:
                current_time = time.time()
                if current_time - self.last_key_time > 2:
                    self.last_key_time = current_time
                if self.check_key(pygame.key.name(event.key).upper()):
                    if self.current_index == len(self.sequence):
                        self.current_guardia_index += 1
                        if self.current_guardia_index >= len(self.time_limits):
                            self.running = False
                        else:
                            self.start_time = time.time()  # Reset the timer for each new guardia
                            self.remaining_time = self.time_limits[self.current_guardia_index]  # Actualizar el tiempo restante
                            self.image = self.imagenes_guardias[self.current_guardia_index]  # Actualizar la imagen del guardia
                if self.wrong_key:
                    self.lives -= 1

    def update(self, tiempo_pasado):
        if self.current_guardia_index < len(self.time_limits):
            self.remaining_time = self.time_limits[self.current_guardia_index] - (time.time() - self.start_time)
        if self.remaining_time <= 0 or self.lives <= 0:
            self.running = False
    
    def dibujar(self, screen):
        screen.blit(self.background_image, (0, 0))
        pygame.draw.rect(screen, self.WHITE, (self.WIDTH - 350, 150, 100, 100))  # Recuadro para el tiempo
        pygame.draw.rect(screen, self.WHITE, (self.WIDTH // 2 - 500, 300, 1000, 200))  # Recuadro para las palabras
        self.draw(screen)
        timer_text = self.font.render(str(int(self.remaining_time)), True, self.RED)
        timer_rect = timer_text.get_rect(center=(self.WIDTH - 300, 200))
        screen.blit(timer_text, timer_rect)
        for i in range(3):
            if i < self.lives:
                screen.blit(self.heart_full, (250 + i * 80, 150))
            else:
                screen.blit(self.heart_empty, (250 + i * 80, 150))
        if not self.running:
            screen.fill(self.WHITE)
            if self.lives <= 0 or self.remaining_time <= 0:
                end_text = self.font.render("Perdiste", True, self.RED)
            else:
                end_text = self.font.render("Felicidades", True, self.GREEN)
            screen.blit(end_text, (self.WIDTH // 2 - end_text.get_width() // 2, self.HEIGHT // 2 - end_text.get_height() // 2))
            pygame.display.flip()
            pygame.time.wait(2000)  # Esperar 2 segundos antes de cerrar
            self.director.salirEscena()  # Add this line to exit the scene
            pygame.quit()
            sys.exit()
