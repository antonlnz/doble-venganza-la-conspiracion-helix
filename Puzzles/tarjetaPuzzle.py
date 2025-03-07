import pygame
import sys

pygame.init()

# Constantes
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tarjeta de Seguridad")
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

# Barra negra
bar_width = 10
bar_height = 40
bar_x = WIDTH // 2 - bar_width // 2  # Esto es para empezar en el centro
bar_y = HEIGHT // 2 - bar_height // 2
bar_speed = 5

# Margen de la zona roja
red_zone_margin = 50 

# Fotos 
background_image = pygame.image.load('imagenes/Tarjeta/fondo_seguridad.jpg')
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))
completion_image = pygame.image.load('imagenes/Tarjeta/tarjeta_guardia.jpg')
completion_image = pygame.transform.scale(completion_image, (300, 200)) 
heart_full = pygame.image.load('imagenes/Tarjeta/heart_full_16x16.png')
heart_empty = pygame.image.load('imagenes/Tarjeta/heart_empty_16x16.png')
heart_full = pygame.transform.scale(heart_full, (24, 24))
heart_empty = pygame.transform.scale(heart_empty, (24, 24))  

# Vidas
lives = 3
font = pygame.font.SysFont(None, 55)

# Aqui es donde hago los niveles y las zonas verdes
level = 1
green_zones = [
    {'x': WIDTH // 2 - 150, 'y': HEIGHT // 2 - 20, 'width': 300, 'height': 40},  # Nivel 1
    {'x': WIDTH // 4 - 50, 'y': HEIGHT // 2 - 20, 'width': 100, 'height': 40},  # Nivel 2 
    {'x': 3 * WIDTH // 4 - 50, 'y': HEIGHT // 2 - 20, 'width': 100, 'height': 40},  # Nivel 2 
    {'x': WIDTH // 4 - 25, 'y': HEIGHT // 2 - 20, 'width': 50, 'height': 40},  # Nivel 3 
    {'x': WIDTH // 2 - 25, 'y': HEIGHT // 2 - 20, 'width': 50, 'height': 40},  # Nivel 3 
    {'x': 3 * WIDTH // 4 - 25, 'y': HEIGHT // 2 - 20, 'width': 50, 'height': 40},  # Nivel 3 
    {'x': WIDTH // 6 - 20, 'y': HEIGHT // 2 - 20, 'width': 35, 'height': 40},  # Nivel 4 
    {'x': WIDTH // 3 - 20, 'y': HEIGHT // 2 - 20, 'width': 35, 'height': 40},  # Nivel 4 
    {'x': WIDTH // 2 - 20, 'y': HEIGHT // 2 - 20, 'width': 35, 'height': 40},  # Nivel 4 
    {'x': 2 * WIDTH // 3 - 20, 'y': HEIGHT // 2 - 20, 'width': 35, 'height': 40},  # Nivel 4 
    {'x': 5 * WIDTH // 6 - 20, 'y': HEIGHT // 2 - 20, 'width': 35, 'height': 40}  # Nivel 4 
]
current_green_zone = 0

# Función para dibujar y colocar las vidas
def draw_lives(screen, lives):
    hearts_width = 3 * 30  
    start_x = bar_x + (bar_width // 2) - (hearts_width // 2)  
    for i in range(3):
        if i < lives:
            screen.blit(heart_full, (start_x + i * 30, bar_y - 40))  
        else:
            screen.blit(heart_empty, (start_x + i * 30, bar_y - 40))  

# Función para terminar
def game_over(screen):
    screen.fill(BLACK)
    game_over_text = font.render('Perdiste', True, WHITE)
    screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - game_over_text.get_height() // 2))
    pygame.display.flip()
    pygame.time.wait(2000)  
    pygame.quit()
    sys.exit()

# Función para mostrar mensaje de completado y la foto
def show_completion_message(screen):
    screen.fill(BLACK)
    screen.blit(completion_image, (WIDTH // 2 - completion_image.get_width() // 2, HEIGHT // 2 - completion_image.get_height() // 2))
    completion_text = font.render('Conseguiste la tarjeta', True, WHITE)
    congrats_text = font.render('¡Felicidades!', True, WHITE)
    screen.blit(congrats_text, (WIDTH // 2 - congrats_text.get_width() // 2, HEIGHT // 2 - completion_image.get_height() // 2 - 40))
    screen.blit(completion_text, (WIDTH // 2 - completion_text.get_width() // 2, HEIGHT // 2 + completion_image.get_height() // 2 + 20))
    pygame.display.flip()
    pygame.time.wait(2000)  

# Dibujamos las zonas verdes de cada nivel usando las coordenadas de green_zones definidas arriba
def draw_green_zones(screen, level, current_green_zone):
    if level == 1:
        zone = green_zones[0]
        pygame.draw.rect(screen, GREEN, (zone['x'], zone['y'], zone['width'], zone['height']))
    elif level == 2:
        for i in range(1, 3):
            zone = green_zones[i]
            if i <= current_green_zone:
                pygame.draw.rect(screen, WHITE, (zone['x'], zone['y'], zone['width'], zone['height']))  # Blanco zona completada
            else:
                pygame.draw.rect(screen, GREEN, (zone['x'], zone['y'], zone['width'], zone['height']))  
    elif level == 3:
        for i in range(3, 6):
            zone = green_zones[i]
            if i <= current_green_zone + 2:
                pygame.draw.rect(screen, WHITE, (zone['x'], zone['y'], zone['width'], zone['height']))  # Blanco zona completada
            else:
                pygame.draw.rect(screen, GREEN, (zone['x'], zone['y'], zone['width'], zone['height']))  
    elif level == 4:
        for i in range(6, 11):
            zone = green_zones[i]
            if i <= current_green_zone + 5:
                pygame.draw.rect(screen, WHITE, (zone['x'], zone['y'], zone['width'], zone['height']))  # Blanco zona completada
            else:
                pygame.draw.rect(screen, GREEN, (zone['x'], zone['y'], zone['width'], zone['height'])) 

def check_success(bar_x, bar_width, green_zones, level, current_green_zone):
    if level == 1:
        green_zone = green_zones[0]
        return green_zone['x'] <= bar_x <= green_zone['x'] + green_zone['width'] - bar_width
    elif level == 2:
        for i in range(1, 3):
            green_zone = green_zones[i]
            if green_zone['x'] <= bar_x <= green_zone['x'] + green_zone['width'] - bar_width:
                if i <= current_green_zone:
                    return 'white_zone' 
                return True
        return False
    elif level == 3:
        for i in range(3, 6):
            green_zone = green_zones[i]
            if green_zone['x'] <= bar_x <= green_zone['x'] + green_zone['width'] - bar_width:
                if i <= current_green_zone + 2:
                    return 'white_zone'  
                return True
        return False
    elif level == 4:
        for i in range(6, 11):
            green_zone = green_zones[i]
            if green_zone['x'] <= bar_x <= green_zone['x'] + green_zone['width'] - bar_width:
                if i <= current_green_zone + 5:
                    return 'white_zone'  
                return True
        return False


running = True
bar_moving = True
bar_direction = 1  # 1 para derecha, -1 para izquierda
completed_zones = set()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and bar_moving:
                bar_moving = False
                result = check_success(bar_x, bar_width, green_zones, level, current_green_zone)
                if result == True:
                    if level == 1:
                        level = 2
                        current_green_zone = 0  # Aqui reseteo la zona verde actual para el nivel 2
                        bar_moving = True
                    elif level == 2:
                        for i in range(1, 3):
                            green_zone = green_zones[i]
                            if green_zone['x'] <= bar_x <= green_zone['x'] + green_zone['width'] - bar_width:
                                completed_zones.add(i)
                                break
                        if len(completed_zones) == 2:
                            level = 3
                            current_green_zone = 0  # Aqui reseteo la zona verde actual para el nivel 3
                            completed_zones.clear()
                        bar_moving = True
                    elif level == 3:
                        for i in range(3, 6):
                            green_zone = green_zones[i]
                            if green_zone['x'] <= bar_x <= green_zone['x'] + green_zone['width'] - bar_width:
                                completed_zones.add(i)
                                break
                        if len(completed_zones) == 3:
                            level = 4
                            current_green_zone = 0  # Aqui reseteo la zona verde actual para el nivel 4
                            completed_zones.clear()
                        bar_moving = True
                    elif level == 4:
                        for i in range(6, 11):
                            green_zone = green_zones[i]
                            if green_zone['x'] <= bar_x <= green_zone['x'] + green_zone['width'] - bar_width:
                                completed_zones.add(i)
                                break
                        if len(completed_zones) == 5:
                            show_completion_message(screen)  
                            running = False  # Acabar el juego y mostrar lo de completado
                        bar_moving = True
                else:
                    lives -= 1
                    if lives == 0:
                        running = False
                    else:
                        bar_moving = True  # Aqui es para sacar las vidas

    if bar_moving:
        bar_x += bar_speed * bar_direction
        if bar_x > WIDTH - red_zone_margin - bar_width or bar_x < red_zone_margin:
            bar_direction *= -1  # Esto es para cambiar la dirección de la barra

    # Aqui es para dibujar todo
    screen.blit(background_image, (0, 0))  
    if level == 1:
        pygame.draw.rect(screen, RED, (red_zone_margin, green_zones[0]['y'], green_zones[0]['x'] - red_zone_margin, green_zones[0]['height']))  
        pygame.draw.rect(screen, RED, (green_zones[0]['x'] + green_zones[0]['width'], green_zones[0]['y'], WIDTH - (green_zones[0]['x'] + green_zones[0]['width']) - red_zone_margin, green_zones[0]['height']))  
    elif level == 2:
        pygame.draw.rect(screen, RED, (red_zone_margin, green_zones[1]['y'], green_zones[1]['x'] - red_zone_margin, green_zones[1]['height']))  
        pygame.draw.rect(screen, RED, (green_zones[1]['x'] + green_zones[1]['width'], green_zones[1]['y'], green_zones[2]['x'] - (green_zones[1]['x'] + green_zones[1]['width']), green_zones[1]['height']))  
        pygame.draw.rect(screen, RED, (green_zones[2]['x'] + green_zones[2]['width'], green_zones[2]['y'], WIDTH - (green_zones[2]['x'] + green_zones[2]['width']) - red_zone_margin, green_zones[2]['height'])) 
    elif level == 3:
        pygame.draw.rect(screen, RED, (red_zone_margin, green_zones[3]['y'], green_zones[3]['x'] - red_zone_margin, green_zones[3]['height']))  
        pygame.draw.rect(screen, RED, (green_zones[3]['x'] + green_zones[3]['width'], green_zones[3]['y'], green_zones[4]['x'] - (green_zones[3]['x'] + green_zones[3]['width']), green_zones[3]['height']))  
        pygame.draw.rect(screen, RED, (green_zones[4]['x'] + green_zones[4]['width'], green_zones[4]['y'], green_zones[5]['x'] - (green_zones[4]['x'] + green_zones[4]['width']), green_zones[4]['height']))  
        pygame.draw.rect(screen, RED, (green_zones[5]['x'] + green_zones[5]['width'], green_zones[5]['y'], WIDTH - (green_zones[5]['x'] + green_zones[5]['width']) - red_zone_margin, green_zones[5]['height']))  
    elif level == 4:
        pygame.draw.rect(screen, RED, (red_zone_margin, green_zones[6]['y'], green_zones[6]['x'] - red_zone_margin, green_zones[6]['height']))  
        pygame.draw.rect(screen, RED, (green_zones[6]['x'] + green_zones[6]['width'], green_zones[6]['y'], green_zones[7]['x'] - (green_zones[6]['x'] + green_zones[6]['width']), green_zones[6]['height']))  
        pygame.draw.rect(screen, RED, (green_zones[7]['x'] + green_zones[7]['width'], green_zones[7]['y'], green_zones[8]['x'] - (green_zones[7]['x'] + green_zones[7]['width']), green_zones[7]['height'])) 
        pygame.draw.rect(screen, RED, (green_zones[8]['x'] + green_zones[8]['width'], green_zones[8]['y'], green_zones[9]['x'] - (green_zones[8]['x'] + green_zones[8]['width']), green_zones[8]['height']))  
        pygame.draw.rect(screen, RED, (green_zones[9]['x'] + green_zones[9]['width'], green_zones[9]['y'], green_zones[10]['x'] - (green_zones[9]['x'] + green_zones[9]['width']), green_zones[9]['height']))  
        pygame.draw.rect(screen, RED, (green_zones[10]['x'] + green_zones[10]['width'], green_zones[10]['y'], WIDTH - (green_zones[10]['x'] + green_zones[10]['width']) - red_zone_margin, green_zones[10]['height']))  
    draw_green_zones(screen, level, current_green_zone)
    for zone_index in completed_zones:
        zone = green_zones[zone_index]
        pygame.draw.rect(screen, WHITE, (zone['x'], zone['y'], zone['width'], zone['height']))  
    pygame.draw.rect(screen, BLACK, (bar_x, bar_y, bar_width, bar_height))  
    draw_lives(screen, lives)  
    pygame.display.flip()

    # Aqui es para mostrar el final si se acaban las vidas
    if lives == 0:
        game_over(screen)

    pygame.time.Clock().tick(60)

pygame.quit()
sys.exit()
