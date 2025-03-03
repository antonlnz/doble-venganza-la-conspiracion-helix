import pygame
import sys
import random
import time

pygame.init()

width, height = 800, 600
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Simón Dice")

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

TARGET_ROUNDS = 5
COUNTDOWN_TIME = 30

sequence = []
user_sequence = []
round_number = 0
game_active = True
start_time = time.time()

button_radius = 90
button_positions = [
    (width//2 - 120, height//2 - 120),
    (width//2 + 120, height//2 - 120),
    (width//2 - 120, height//2 + 120),
    (width//2 + 120, height//2 + 120),
]

buttons = [
    {"color": RED, "pos": pos} for pos in button_positions[:1]
] + [
    {"color": GREEN, "pos": pos} for pos in button_positions[1:2]
] + [
    {"color": BLUE, "pos": pos} for pos in button_positions[2:3]
] + [
    {"color": YELLOW, "pos": pos} for pos in button_positions[3:]
]

def draw_background():
    for y in range(height):
        color_value = int(50 + (y / height) * 100)
        pygame.draw.line(window, (color_value, color_value, color_value), (0, y), (width, y))
    center_x, center_y = width // 2, height // 2
    for radius in range(300, 0, -10):
        alpha = max(0, 255 - (radius * 255 // 300))
        light_surface = pygame.Surface((width, height), pygame.SRCALPHA)
        pygame.draw.circle(light_surface, (255, 255, 255, alpha), (center_x, center_y), radius)
        window.blit(light_surface, (0, 0))

def draw_buttons():
    for button in buttons:
        pygame.draw.circle(window, button["color"], button["pos"], button_radius)
    pygame.display.update()

def flash_button(button):
    original_color = button["color"]
    pygame.draw.circle(window, WHITE, button["pos"], button_radius)
    pygame.display.update()
    pygame.time.delay(200)
    pygame.draw.circle(window, original_color, button["pos"], button_radius)
    pygame.display.update()
    pygame.time.delay(100)

def show_sequence():
    pygame.time.delay(200)
    for index in sequence:
        flash_button(buttons[index])

def check_user_input():
    for i in range(len(user_sequence)):
        if user_sequence[i] != sequence[i]:
            return False
    return True

def draw_text(text, x, y, size=40, color=WHITE):
    font = pygame.font.Font(None, size)
    text_surface = font.render(text, True, color)
    window.blit(text_surface, (x, y))

running = True
while running:
    window.fill(BLACK)
    draw_background()
    draw_buttons()

    if game_active:
        elapsed_time = int(time.time() - start_time)
        remaining_time = max(0, COUNTDOWN_TIME - elapsed_time)
        draw_text(f"Tiempo: {remaining_time}s", width//2 - 100, 30)
        if remaining_time <= 0:
            game_active = False
        if len(user_sequence) == len(sequence):
            if len(sequence) == round_number:
                new_step = random.randint(0, 3)
                sequence.append(new_step)
                show_sequence()
                user_sequence = []
    else:
        draw_text("\u00a1Juego Terminado!", width//2 - 130, height//2 - 30, 50, BLACK)
        pygame.display.flip()
        pygame.time.delay(2000)
        running = False
    
    pygame.display.flip()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if game_active and event.type == pygame.MOUSEBUTTONDOWN:
            for i, button in enumerate(buttons):
                if (event.pos[0] - button["pos"][0])**2 + (event.pos[1] - button["pos"][1])**2 <= button_radius**2:
                    flash_button(button)
                    user_sequence.append(i)
                    if not check_user_input():
                        game_active = False
                    elif len(user_sequence) == len(sequence):
                        round_number += 1
                        if round_number == TARGET_ROUNDS:
                            game_active = False

pygame.quit()
sys.exit()