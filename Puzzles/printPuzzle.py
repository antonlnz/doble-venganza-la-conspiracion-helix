import os
import pygame
import sys
import time
from escena import *
from settings import *
class Huella(Escena):
    def __init__(self, director):
        Escena.__init__(self, director)
        os.environ['SDL_VIDEO_CENTERED'] = '1'
        self.WIDTH = 1920  
        self.HEIGHT = 1080
        self.BLANCO = (0, 0, 0)
        self.NEGRO = (0, 0, 0)
        self.ROJO = (255, 0, 0)
        self.AZUL = (0, 0, 255)
        self.goal = pygame.Rect(self.WIDTH - 200, 0, 10, self.HEIGHT)
        self.player = pygame.Rect(10, self.HEIGHT // 2 - 25, 100, 100)  # Imagen 100x100
        self.player_collision_rect = pygame.Rect(self.player.x + 25, self.player.y + 25, 50, 50)  # Colisión 50x50
        self.font = pygame.font.Font(None, 74)
        self.message = ""
        self.level = 1
        self.game_over = False
        self.setup_level()
        pygame.mouse.set_pos(10, self.HEIGHT // 2)
        
        # Cargar imagen de fondo
        self.background_image = pygame.image.load("imagenes/Huella/suelo_factory.png")
        self.bg_width, self.bg_height = self.background_image.get_size()

        # Cargar imagen del jugador
        self.player_image = pygame.image.load("imagenes/Huella/soldado2.png")
        self.player_image = pygame.transform.scale(self.player_image, (80, 80))  # Imagen de 100x100
    
    def setup_level(self):
        pygame.mouse.set_pos(10, self.HEIGHT // 2)
        self.red_zones = []
        self.moving_zones = []
        self.vertical_moving_zones = []
        if self.level == 1:
            self.red_zones = [
                pygame.Rect(400, 10, 100, 650),  
                pygame.Rect(400, 900, 100, 550),  
                pygame.Rect(600, 10, 100, 800),  
                pygame.Rect(800, 900, 100, 750),  
                pygame.Rect(1000, 10, 100, 850),
                pygame.Rect(1200, 900, 100, 750),
                pygame.Rect(1400, 10, 100, 650),
                pygame.Rect(1600, 900, 100, 850)    
            ]
            self.vertical_moving_zones = [
                pygame.Rect(800, 100, 100, 100)
            ]
            self.vertical_direction = [1]
        elif self.level == 2:
            self.red_zones = [
                pygame.Rect(400, 10, 100, 650),  
                pygame.Rect(400, 900, 100, 600), 
                pygame.Rect(1200, 900, 100, 700),
                pygame.Rect(1400, 10, 100, 650),
                pygame.Rect(1600, 900, 100, 750) 
            ]
            self.moving_zones = [
                pygame.Rect(250, 300, 100, 200),
                pygame.Rect(1600, 450, 100, 200),
                pygame.Rect(250, 800, 100, 200),
                pygame.Rect(1600, 900, 100, 200)
            ]
            self.moving_direction =  [1, -1, 1, -1]
            self.vertical_moving_zones = [
                pygame.Rect(650, 600, 50, 200),
                pygame.Rect(800, 300, 50, 200),
                pygame.Rect(950, 700, 50, 200)
            ]
            self.vertical_direction = [-1, 1, -1]
        elif self.level == 3:
            self.red_zones = [
                pygame.Rect(400, 50, 100, 450),  
                pygame.Rect(400, 900, 100, 600),  
                pygame.Rect(600, 10, 100, 650),  
                pygame.Rect(800, 900, 100, 800),  
                pygame.Rect(1000, 10, 100, 750),
                pygame.Rect(1200, 900, 100, 750),
                pygame.Rect(1400, 10, 100, 600),
                pygame.Rect(1600, 900, 100, 850)    
            ]
            self.moving_zones = [
                pygame.Rect(250, 300, 100, 200),
                pygame.Rect(1600, 900, 100, 200)
            ]
            self.moving_direction =  [1, -1, 1, -1]
            self.vertical_moving_zones = [
                pygame.Rect(500, 200, 50, 300),
                pygame.Rect(650, 600, 50, 200),
                pygame.Rect(800, 300, 50, 200),
                pygame.Rect(950, 700, 50, 200)
            ]
            self.vertical_direction = [1, -1, 1, -1]
        pygame.mouse.set_pos(10, self.HEIGHT // 2)

    def update(self, tiempo):
        if self.game_over:
            if self.retardo():
                self.director.salirEscena()

        else:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            self.player.topleft = (mouse_x - self.player.width // 2, mouse_y - self.player.height // 2)
            
            # Actualizamos el rectángulo de colisión de acuerdo con la posición del jugador
            self.player_collision_rect.topleft = (self.player.x + 20, self.player.y + 25)  # Ajuste para que sea 50x50
            
            self.check_collisions()
            if self.level > 1:
                self.update_moving_zones()
                self.update_vertical_moving_zones()
    
    def update_moving_zones(self):
        for i, zone in enumerate(self.moving_zones):
            zone.x += self.moving_direction[i] * 5
            if zone.left < 20 or zone.right > self.WIDTH-20:
                self.moving_direction[i] *= -1
    
    def update_vertical_moving_zones(self):
        for i, zone in enumerate(self.vertical_moving_zones):
            zone.y += self.vertical_direction[i] * 5
            if zone.top < 10 or zone.bottom > self.HEIGHT-10:
                self.vertical_direction[i] *= -1        
    
    def check_collisions(self):
        # Usamos self.player_collision_rect (50x50) para la comprobación de colisiones
        for zone in self.red_zones:
            if self.player_collision_rect.colliderect(zone):
                self.message = "¡Perdiste!"
                pygame.mouse.set_visible(False)  # Ocultar el cursor
                pygame.event.set_grab(True)
                self.game_over = True
                if self.game_over:
                    if self.retardo():
                        self.director.salirEscena()
                return
        if self.level > 1:
            for zone in self.moving_zones:
                if self.player_collision_rect.colliderect(zone):
                    self.message = "¡Perdiste!"
                    pygame.mouse.set_visible(False)  # Ocultar el cursor
                    pygame.event.set_grab(True)
                    self.game_over = True
                    if self.game_over:
                        if self.retardo():
                            self.director.salirEscena()
                    return
            for zone in self.vertical_moving_zones:
                if self.player_collision_rect.colliderect(zone):
                    self.message = "¡Perdiste!"
                    pygame.mouse.set_visible(False)  # Ocultar el cursor
                    pygame.event.set_grab(True)
                    self.game_over = True
                    if self.game_over:
                        if self.retardo():
                            self.director.salirEscena()
                    return
        if self.player_collision_rect.colliderect(self.goal):
            if self.level < 3:
                self.level += 1
                self.setup_level()
            else:
                self.message = "¡Felicidades!"
                pygame.mouse.set_visible(False)  # Ocultar el cursor
                pygame.event.set_grab(True)
                self.game_over = True
                if self.game_over:
                    if self.retardo():
                        self.director.salirEscena()
            return
    
    def eventos(self, eventos):
        if self.game_over:
            return
        for event in eventos:
            if event.type == pygame.QUIT:
                sys.exit()
    
    def dibujar(self, pantalla):
        # Dibujar el fondo en mosaico
        for x in range(0, self.WIDTH, self.bg_width):
            for y in range(0, self.HEIGHT, self.bg_height):
                pantalla.blit(self.background_image, (x, y))
        
        # Dibuja la línea de meta
        for i in range(0, self.HEIGHT, 40):
            color = (255, 255, 255) if (i // 40) % 2 == 0 else self.NEGRO
            pygame.draw.rect(pantalla, color, pygame.Rect(self.WIDTH - 230, i, 20, 20))
            pygame.draw.rect(pantalla, color, pygame.Rect(self.WIDTH - 210, i + 20, 20, 20))
        
        # Dibujar zonas rojas con borde negro
        for zone in self.red_zones + self.moving_zones + self.vertical_moving_zones:
            pygame.draw.rect(pantalla, self.NEGRO, zone.inflate(4, 4))  # Borde negro
            pygame.draw.rect(pantalla, self.ROJO, zone)  # Zona roja
        
        # Dibujar imagen del jugador en su posición (100x100)
        pantalla.blit(self.player_image, self.player.topleft)
        
        if self.message:
            text = self.font.render(self.message, True, (255, 255, 255))
            pantalla.blit(text, (self.WIDTH // 2 - text.get_width() // 2, self.HEIGHT // 2 - text.get_height() // 2))
        
        pygame.display.flip()
