import os
import pygame
import sys
from escena import *
from settings import *

class Tarjeta(Escena):
    def __init__(self, director):
        Escena.__init__(self, director)
        # Center the window on the screen
        os.environ['SDL_VIDEO_CENTERED'] = '1'
        self.WIDTH, self.HEIGHT = WIDTH, HEIGHT
        # self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        # pygame.display.set_caption("Tarjeta de Seguridad")
        self.WHITE = (255, 255, 255)
        self.GREEN = (0, 255, 0)
        self.RED = (255, 0, 0)
        self.BLACK = (0, 0, 0)
        self.bar_width = 10
        self.bar_height = 40
        self.bar_x = self.WIDTH // 2 - self.bar_width // 2
        self.bar_y = self.HEIGHT // 2 - self.bar_height // 2
        self.bar_speed = 5
        self.red_zone_margin = 50
        self.background_image = pygame.image.load('imagenes/Tarjeta/fondo_seguridad.jpg')
        self.background_image = pygame.transform.scale(self.background_image, (self.WIDTH, self.HEIGHT))
        self.completion_image = pygame.image.load('imagenes/Tarjeta/tarjeta_guardia.jpg')
        self.completion_image = pygame.transform.scale(self.completion_image, (300, 200))
        self.heart_full = pygame.image.load('imagenes/Tarjeta/heart_full_16x16.png')
        self.heart_empty = pygame.image.load('imagenes/Tarjeta/heart_empty_16x16.png')
        self.heart_full = pygame.transform.scale(self.heart_full, (24, 24))
        self.heart_empty = pygame.transform.scale(self.heart_empty, (24, 24))
        self.lives = 3
        self.font = pygame.font.SysFont(None, 55)
        self.level = 1
        self.green_zones = [
            {'x': self.WIDTH // 2 - 150, 'y': self.HEIGHT // 2 - 20, 'width': 300, 'height': 40},
            {'x': self.WIDTH // 4 - 50, 'y': self.HEIGHT // 2 - 20, 'width': 100, 'height': 40},
            {'x': 3 * self.WIDTH // 4 - 50, 'y': self.HEIGHT // 2 - 20, 'width': 100, 'height': 40},
            {'x': self.WIDTH // 4 - 25, 'y': self.HEIGHT // 2 - 20, 'width': 50, 'height': 40},
            {'x': self.WIDTH // 2 - 25, 'y': self.HEIGHT // 2 - 20, 'width': 50, 'height': 40},
            {'x': 3 * self.WIDTH // 4 - 25, 'y': self.HEIGHT // 2 - 20, 'width': 50, 'height': 40},
            {'x': self.WIDTH // 6 - 20, 'y': self.HEIGHT // 2 - 20, 'width': 35, 'height': 40},
            {'x': self.WIDTH // 3 - 20, 'y': self.HEIGHT // 2 - 20, 'width': 35, 'height': 40},
            {'x': self.WIDTH // 2 - 20, 'y': self.HEIGHT // 2 - 20, 'width': 35, 'height': 40},
            {'x': 2 * self.WIDTH // 3 - 20, 'y': self.HEIGHT // 2 - 20, 'width': 35, 'height': 40},
            {'x': 5 * self.WIDTH // 6 - 20, 'y': self.HEIGHT // 2 - 20, 'width': 35, 'height': 40}
        ]
        self.current_green_zone = 0
        self.running = True
        self.bar_moving = True
        self.bar_direction = 1
        self.completed_zones = set()

    def draw_lives(self, screen):
        hearts_width = 3 * 30
        start_x = self.bar_x + (self.bar_width // 2) - (hearts_width // 2)
        for i in range(3):
            if i < self.lives:
                screen.blit(self.heart_full, (start_x + i * 30, self.bar_y - 40))
            else:
                screen.blit(self.heart_empty, (start_x + i * 30, self.bar_y - 40))

    def game_over(self, screen):
        screen.fill(self.BLACK)
        game_over_text = self.font.render('Perdiste', True, self.WHITE)
        screen.blit(game_over_text, (self.WIDTH // 2 - game_over_text.get_width() // 2, self.HEIGHT // 2 - game_over_text.get_height() // 2))
        pygame.display.flip()
        pygame.time.wait(2000)
        

    def show_completion_message(self, screen):
        screen.fill(self.BLACK)
        screen.blit(self.completion_image, (self.WIDTH // 2 - self.completion_image.get_width() // 2, self.HEIGHT // 2 - self.completion_image.get_height() // 2))
        completion_text = self.font.render('Conseguiste la tarjeta', True, self.WHITE)
        congrats_text = self.font.render('¡Felicidades!', True, self.WHITE)
        screen.blit(congrats_text, (self.WIDTH // 2 - congrats_text.get_width() // 2, self.HEIGHT // 2 - self.completion_image.get_height() // 2 - 40))
        screen.blit(completion_text, (self.WIDTH // 2 - completion_text.get_width() // 2, self.HEIGHT // 2 + self.completion_image.get_height() // 2 + 20))
        pygame.display.flip()
        pygame.time.wait(2000)
        

    def draw_green_zones(self, screen):
        if self.level == 1:
            zone = self.green_zones[0]
            pygame.draw.rect(screen, self.GREEN, (zone['x'], zone['y'], zone['width'], zone['height']))
        elif self.level == 2:
            for i in range(1, 3):
                zone = self.green_zones[i]
                if i <= self.current_green_zone:
                    pygame.draw.rect(screen, self.WHITE, (zone['x'], zone['y'], zone['width'], zone['height']))
                else:
                    pygame.draw.rect(screen, self.GREEN, (zone['x'], zone['y'], zone['width'], zone['height']))
        elif self.level == 3:
            for i in range(3, 6):
                zone = self.green_zones[i]
                if i <= self.current_green_zone + 2:
                    pygame.draw.rect(screen, self.WHITE, (zone['x'], zone['y'], zone['width'], zone['height']))
                else:
                    pygame.draw.rect(screen, self.GREEN, (zone['x'], zone['y'], zone['width'], zone['height']))
        elif self.level == 4:
            for i in range(6, 11):
                zone = self.green_zones[i]
                if i <= self.current_green_zone + 5:
                    pygame.draw.rect(screen, self.WHITE, (zone['x'], zone['y'], zone['width'], zone['height']))
                else:
                    pygame.draw.rect(screen, self.GREEN, (zone['x'], zone['y'], zone['width'], zone['height']))

    def check_success(self):
        if self.level == 1:
            green_zone = self.green_zones[0]
            return green_zone['x'] <= self.bar_x <= green_zone['x'] + green_zone['width'] - self.bar_width
        elif self.level == 2:
            for i in range(1, 3):
                green_zone = self.green_zones[i]
                if green_zone['x'] <= self.bar_x <= green_zone['x'] + green_zone['width'] - self.bar_width:
                    if i <= self.current_green_zone:
                        return 'white_zone'
                    return True
            return False
        elif self.level == 3:
            for i in range(3, 6):
                green_zone = self.green_zones[i]
                if green_zone['x'] <= self.bar_x <= green_zone['x'] + green_zone['width'] - self.bar_width:
                    if i <= self.current_green_zone + 2:
                        return 'white_zone'
                    return True
            return False
        elif self.level == 4:
            for i in range(6, 11):
                green_zone = self.green_zones[i]
                if green_zone['x'] <= self.bar_x <= green_zone['x'] + green_zone['width'] - self.bar_width:
                    if i <= self.current_green_zone + 5:
                        return 'white_zone'
                    return True
            return False

    def update(self, tiempo):
        if self.bar_moving:
            self.bar_x += self.bar_speed * self.bar_direction
            if self.bar_x > self.WIDTH - self.red_zone_margin - self.bar_width or self.bar_x < self.red_zone_margin:
                self.bar_direction *= -1

        if not self.bar_moving:
            result = self.check_success()
            if result == True:
                if self.level == 1:
                    self.level = 2
                    self.current_green_zone = 0
                    self.bar_moving = True
                elif self.level == 2:
                    for i in range(1, 3):
                        green_zone = self.green_zones[i]
                        if green_zone['x'] <= self.bar_x <= green_zone['x'] + green_zone['width'] - self.bar_width:
                            self.completed_zones.add(i)
                            break
                    if len(self.completed_zones) == 2:
                        self.level = 3
                        self.current_green_zone = 0
                        self.completed_zones.clear()
                    self.bar_moving = True
                elif self.level == 3:
                    for i in range(3, 6):
                        green_zone = self.green_zones[i]
                        if green_zone['x'] <= self.bar_x <= green_zone['x'] + green_zone['width'] - self.bar_width:
                            self.completed_zones.add(i)
                            break
                    if len(self.completed_zones) == 3:
                        self.level = 4
                        self.current_green_zone = 0
                        self.completed_zones.clear()
                    self.bar_moving = True
                elif self.level == 4:
                    for i in range(6, 11):
                        green_zone = self.green_zones[i]
                        if green_zone['x'] <= self.bar_x <= green_zone['x'] + green_zone['width'] - self.bar_width:
                            self.completed_zones.add(i)
                            break
                    
                    self.bar_moving = True
            else:
                self.lives -= 1
                if self.lives == 0:
                    self.running = False
                    self.completado = True
                    self.director.salirEscena()
                else:
                    self.bar_moving = True

    def eventos(self, eventos):
        for event in eventos:
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and self.bar_moving:
                    self.bar_moving = False

    def dibujar(self, pantalla):
        pantalla.blit(self.background_image, (0, 0))
        if self.level == 1:
            pygame.draw.rect(pantalla, self.RED, (self.red_zone_margin, self.green_zones[0]['y'], self.green_zones[0]['x'] - self.red_zone_margin, self.green_zones[0]['height']))
            pygame.draw.rect(pantalla, self.RED, (self.green_zones[0]['x'] + self.green_zones[0]['width'], self.green_zones[0]['y'], self.WIDTH - (self.green_zones[0]['x'] + self.green_zones[0]['width']) - self.red_zone_margin, self.green_zones[0]['height']))
        elif self.level == 2:
            pygame.draw.rect(pantalla, self.RED, (self.red_zone_margin, self.green_zones[1]['y'], self.green_zones[1]['x'] - self.red_zone_margin, self.green_zones[1]['height']))
            pygame.draw.rect(pantalla, self.RED, (self.green_zones[1]['x'] + self.green_zones[1]['width'], self.green_zones[1]['y'], self.green_zones[2]['x'] - (self.green_zones[1]['x'] + self.green_zones[1]['width']), self.green_zones[1]['height']))
            pygame.draw.rect(pantalla, self.RED, (self.green_zones[2]['x'] + self.green_zones[2]['width'], self.green_zones[2]['y'], self.WIDTH - (self.green_zones[2]['x'] + self.green_zones[2]['width']) - self.red_zone_margin, self.green_zones[2]['height']))
        elif self.level == 3:
            pygame.draw.rect(pantalla, self.RED, (self.red_zone_margin, self.green_zones[3]['y'], self.green_zones[3]['x'] - self.red_zone_margin, self.green_zones[3]['height']))
            pygame.draw.rect(pantalla, self.RED, (self.green_zones[3]['x'] + self.green_zones[3]['width'], self.green_zones[3]['y'], self.green_zones[4]['x'] - (self.green_zones[3]['x'] + self.green_zones[3]['width']), self.green_zones[3]['height']))
            pygame.draw.rect(pantalla, self.RED, (self.green_zones[4]['x'] + self.green_zones[4]['width'], self.green_zones[4]['y'], self.green_zones[5]['x'] - (self.green_zones[4]['x'] + self.green_zones[4]['width']), self.green_zones[4]['height']))
            pygame.draw.rect(pantalla, self.RED, (self.green_zones[5]['x'] + self.green_zones[5]['width'], self.green_zones[5]['y'], self.WIDTH - (self.green_zones[5]['x'] + self.green_zones[5]['width']) - self.red_zone_margin, self.green_zones[5]['height']))
        elif self.level == 4:
            pygame.draw.rect(pantalla, self.RED, (self.red_zone_margin, self.green_zones[6]['y'], self.green_zones[6]['x'] - self.red_zone_margin, self.green_zones[6]['height']))
            pygame.draw.rect(pantalla, self.RED, (self.green_zones[6]['x'] + self.green_zones[6]['width'], self.green_zones[6]['y'], self.green_zones[7]['x'] - (self.green_zones[6]['x'] + self.green_zones[6]['width']), self.green_zones[6]['height']))
            pygame.draw.rect(pantalla, self.RED, (self.green_zones[7]['x'] + self.green_zones[7]['width'], self.green_zones[7]['y'], self.green_zones[8]['x'] - (self.green_zones[7]['x'] + self.green_zones[7]['width']), self.green_zones[7]['height']))
            pygame.draw.rect(pantalla, self.RED, (self.green_zones[8]['x'] + self.green_zones[8]['width'], self.green_zones[8]['y'], self.green_zones[9]['x'] - (self.green_zones[8]['x'] + self.green_zones[8]['width']), self.green_zones[8]['height']))
            pygame.draw.rect(pantalla, self.RED, (self.green_zones[9]['x'] + self.green_zones[9]['width'], self.green_zones[9]['y'], self.green_zones[10]['x'] - (self.green_zones[9]['x'] + self.green_zones[9]['width']), self.green_zones[9]['height']))
            pygame.draw.rect(pantalla, self.RED, (self.green_zones[10]['x'] + self.green_zones[10]['width'], self.green_zones[10]['y'], self.WIDTH - (self.green_zones[10]['x'] + self.green_zones[10]['width']) - self.red_zone_margin, self.green_zones[10]['height']))
        self.draw_green_zones(pantalla)
        for zone_index in self.completed_zones:
            zone = self.green_zones[zone_index]
            pygame.draw.rect(pantalla, self.WHITE, (zone['x'], zone['y'], zone['width'], zone['height']))
        pygame.draw.rect(pantalla, self.BLACK, (self.bar_x, self.bar_y, self.bar_width, self.bar_height))
        self.draw_lives(pantalla)
        if self.lives == 0:
            self.game_over(pantalla)
            
        
        if len(self.completed_zones) == 5:
            self.show_completion_message(pantalla)
            self.completado = True
            self.director.salirEscena()
            
                
        pygame.display.flip()

if __name__ == "__main__":
    director = None  # Replace with actual director object if available
    tarjeta = Tarjeta(director)
    tarjeta.run()
