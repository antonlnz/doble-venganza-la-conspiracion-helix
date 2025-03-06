import pygame
import random
import time

# Inicializar pygame
pygame.init()

# Configuración de la pantalla
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Guardias Puzzle")

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Fuente
font = pygame.font.Font(None, 74)

# Cargar y escalar imagen de fondo
background_image = pygame.image.load('C:/Users/siimi/Documents/doble-venganza-la-conspiracion-helix/imagenes/Guardias/fondo_banco2.jpg')
background_image = pygame.transform.scale(background_image, (800, 600))

# Cargar y escalar imágenes de corazones
heart_full = pygame.image.load('C:/Users/siimi/Documents/doble-venganza-la-conspiracion-helix/imagenes/Guardias/heart_full_16x16.png')
heart_empty = pygame.image.load('C:/Users/siimi/Documents/doble-venganza-la-conspiracion-helix/imagenes/Guardias/heart_empty_16x16.png')
heart_full = pygame.transform.scale(heart_full, (24, 24))
heart_empty = pygame.transform.scale(heart_empty, (24, 24))

# Cargar imágenes de guardias
policeman_image = pygame.image.load('C:/Users/siimi/Documents/doble-venganza-la-conspiracion-helix/imagenes/Guardias/Policeman.png')
policewoman_image = pygame.image.load('C:/Users/siimi/Documents/doble-venganza-la-conspiracion-helix/imagenes/Guardias/Policewoman.png')
policeman_image = pygame.transform.scale(policeman_image, (200, 200))
policewoman_image = pygame.transform.scale(policewoman_image, (200, 200))

# Guardias
class Guardia:
    def __init__(self, x, y, image):
        self.x = x
        self.y = y
        self.image = image
        self.sequence = self.generate_sequence()
        self.current_index = 0
        self.health = len(self.sequence)
        self.wrong_key = False

    def generate_sequence(self):
        return [random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ') for _ in range(5)]

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y + 200))  # Colocar la imagen debajo del recuadro con las letras y centrarla
        correct_text = font.render(''.join(self.sequence[:self.current_index]), True, GREEN)
        if self.wrong_key:
            remaining_text = font.render(''.join(self.sequence[self.current_index:self.current_index + 1]), True, RED)
        else:
            remaining_text = font.render(''.join(self.sequence[self.current_index:self.current_index + 1]), True, BLACK)
        text_x = 60 + (580 - correct_text.get_width() - remaining_text.get_width()) // 2
        screen.blit(correct_text, (text_x, 160))
        screen.blit(remaining_text, (text_x + correct_text.get_width(), 160))

    def check_key(self, key):
        if key == self.sequence[self.current_index]:
            self.current_index += 1
            self.wrong_key = False
            if self.current_index == len(self.sequence):
                return True
        else:
            self.wrong_key = True
        return False

# Juego
def game():
    running = True
    clock = pygame.time.Clock()
    guardias = [
        Guardia(300, 200, policeman_image),
        Guardia(300, 200, policewoman_image),
        Guardia(300, 200, policeman_image)
    ]
    current_guardia_index = 0
    lives = 3
    last_key_time = time.time()
    start_time = time.time()
    time_limits = [10, 7, 5]  # Tiempos para cada guardia

    while running:
        screen.blit(background_image, (0, 0))
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                current_time = time.time()
                if current_time - last_key_time > 2:
                    last_key_time = current_time
                if guardias[current_guardia_index].check_key(pygame.key.name(event.key).upper()):
                    if guardias[current_guardia_index].current_index == len(guardias[current_guardia_index].sequence):
                        current_guardia_index += 1
                        if current_guardia_index >= len(guardias):
                            guardias = []  # Vaciar la lista de guardias
                            running = False
                            break
                        start_time = time.time()  # Reset the timer for each new guardia
                if guardias[current_guardia_index].wrong_key:
                    lives -= 1

        if current_guardia_index < len(time_limits):
            remaining_time = time_limits[current_guardia_index] - (time.time() - start_time)

        if remaining_time <= 0:
            running = False

        # Dibujar recuadros blancos
        pygame.draw.rect(screen, WHITE, (550, 50, 50, 50))  # Recuadro para el tiempo
        pygame.draw.rect(screen, WHITE, (150, 150, 500, 100))  # Recuadro para las palabras

        if current_guardia_index < len(guardias):
            guardias[current_guardia_index].draw(screen)

        # Mostrar cuenta atrás
        timer_text = font.render(str(int(remaining_time)), True, RED)
        timer_rect = timer_text.get_rect(center=(575, 75))
        screen.blit(timer_text, timer_rect)

        # Mostrar vidas
        for i in range(3):
            if i < lives:
                screen.blit(heart_full, (110 + i * 40, 60))
            else:
                screen.blit(heart_empty, (110 + i * 40, 60))

        if lives <= 0:
            running = False

        pygame.display.flip()
        clock.tick(60)

    # Mostrar mensaje de "Perdiste" o "Felicidades"
    screen.fill(WHITE)
    if lives <= 0 or remaining_time <= 0:
        end_text = font.render("Perdiste", True, RED)
    elif not guardias:
        end_text = font.render("Felicidades", True, GREEN)
    screen.blit(end_text, (275, 250))
    pygame.display.flip()
    pygame.time.wait(2000)  # Esperar 2 segundos antes de cerrar

    pygame.quit()

if __name__ == "__main__":
    game()
