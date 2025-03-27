import pygame
import os
import sys
import random
import time
from escena import *

class SimonDice(Escena):
    def __init__(self, director):
        Escena.__init__(self, director)
        os.environ['SDL_VIDEO_CENTERED'] = '1'
        self.width, self.height = 1920, 1080  # Updated values
        self.window = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Simón Dice")

        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.RED = (255, 0, 0)
        self.GREEN = (0, 255, 0)
        self.BLUE = (0, 0, 255)
        self.YELLOW = (255, 255, 0)

        self.TARGET_ROUNDS = 5
        self.COUNTDOWN_TIME = 30

        self.sequence = []
        self.user_sequence = []
        self.round_number = 0
        self.game_active = True
        self.start_time = None
        self.completado = False  # Add completado initialization

        self.button_radius = 110  # Increased radius
        self.button_positions = [
            (self.width//2 - 120, self.height//2 - 120),
            (self.width//2 + 120, self.height//2 - 120),
            (self.width//2 - 120, self.height//2 + 120),
            (self.width//2 + 120, self.height//2 + 120),
        ]

        self.buttons = [
            {"color": self.RED, "pos": pos} for pos in self.button_positions[:1]
        ] + [
            {"color": self.GREEN, "pos": pos} for pos in self.button_positions[1:2]
        ] + [
            {"color": self.BLUE, "pos": pos} for pos in self.button_positions[2:3]
        ] + [
            {"color": self.YELLOW, "pos": pos} for pos in self.button_positions[3:]
        ]

        self.sound_completed = pygame.mixer.Sound("Sonidos/completed.wav")
        self.sound_click = pygame.mixer.Sound("Sonidos/simon.wav")
        self.sound_blink = pygame.mixer.Sound("Sonidos/simon.wav")
        self.sound_blink.set_volume(0.2)
        self.sound_endgame = pygame.mixer.Sound("Sonidos/endgame.wav")

    def draw_background(self, pantalla):
        for y in range(self.height):
            color_value = int(50 + (y / self.height) * 100)
            pygame.draw.line(pantalla, (color_value, color_value, color_value), (0, y), (self.width, y))
        center_x, center_y = self.width // 2, self.height // 2
        for radius in range(300, 0, -10):
            alpha = max(0, 255 - (radius * 255 // 300))
            light_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
            pygame.draw.circle(light_surface, (255, 255, 255, alpha), (center_x, center_y), radius)
            pantalla.blit(light_surface, (0, 0))

    def draw_buttons(self, pantalla):
        for button in self.buttons:
            pygame.draw.circle(pantalla, button["color"], button["pos"], self.button_radius)
        pygame.display.update()

    def flash_button(self, pantalla, button):
        original_color = button["color"]
        pygame.draw.circle(pantalla, self.WHITE, button["pos"], self.button_radius)
        pygame.display.update()
        pygame.time.delay(200)
        pygame.draw.circle(pantalla, original_color, button["pos"], self.button_radius)
        pygame.display.update()
        pygame.time.delay(100)

    def show_sequence(self, pantalla):
        pygame.time.delay(200)
        for index in self.sequence:
            self.sound_blink.play()
            self.flash_button(pantalla, self.buttons[index])

    def check_user_input(self):
        for i in range(len(self.user_sequence)):
            if self.user_sequence[i] != self.sequence[i]:
                return False
        return True

    def draw_text(self, pantalla, text, x, y, size=100, color=None, background=False):  # Significantly increased default size
        if color is None:
            color = self.WHITE
        font = pygame.font.Font(None, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect(center=(self.width // 2, y))
        if background:
            pygame.draw.rect(pantalla, self.WHITE, (0, y - 50, self.width, text_rect.height + 40))  # Significantly increased line size
        pantalla.blit(text_surface, text_rect.topleft)

    def run(self):
        running = True
        while running:
            self.window.fill(self.BLACK)
            self.draw_background(self.window)
            self.draw_buttons(self.window)

            if self.game_active:
                elapsed_time = int(time.time() - self.start_time)
                remaining_time = max(0, self.COUNTDOWN_TIME - elapsed_time)
                self.draw_text(self.window, f"Tiempo: {remaining_time}s", self.width//2, 250)  # Set to 250
                if remaining_time <= 0:
                    self.game_active = False
                    self.director.salirEscena()  # Salir de la escena
                if len(self.user_sequence) == len(self.sequence):
                    if len(self.sequence) == self.round_number:
                        new_step = random.randint(0, 3)
                        self.sequence.append(new_step)
                        self.show_sequence(self.window)
                        self.user_sequence = []
            else:
                if self.round_number == self.TARGET_ROUNDS:
                    self.draw_text(self.window, "¡Felicidades!", self.width//2, self.height//2 - 30, 50, self.BLACK, background=True)
                else:
                    self.draw_text(self.window, "¡Perdiste!", self.width//2, self.height//2 - 30, 50, self.BLACK, background=True)
                pygame.display.flip()
                
                running = False
                if self.retardo():
                    self.director.salirEscena()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if self.game_active and event.type == pygame.MOUSEBUTTONDOWN:
                    for i, button in enumerate(self.buttons):
                        if (event.pos[0] - button["pos"][0])**2 + (event.pos[1] - button["pos"][1])**2 <= self.button_radius**2:
                            self.flash_button(self.window, button)
                            self.user_sequence.append(i)
                            if not self.check_user_input():
                                self.game_active = False
                            elif len(self.user_sequence) == len(self.sequence):
                                self.round_number += 1
                                if self.round_number == self.TARGET_ROUNDS:
                                    self.game_active = False

    def update(self, tiempo):
        if self.game_active:
            if self.start_time is None: 
                self.start_time = time.time()
                self.dibujar(self.window)
            elapsed_time = int(time.time() - self.start_time)
            remaining_time = max(0, self.COUNTDOWN_TIME - elapsed_time)
            self.draw_text(self.window, f"Tiempo: {remaining_time}s", self.width//2, 250)  # Set to 250
            if remaining_time <= 0:
                self.game_active = False
                self.director.salirEscena()  # Salir de la escena
            if len(self.user_sequence) == len(self.sequence):
                if len(self.sequence) == self.round_number:
                    new_step = random.randint(0, 3)
                    self.sequence.append(new_step)
                    self.show_sequence(self.window)
                    self.user_sequence = []
        else:
            if self.retardo():
                    self.director.salirEscena()

    def eventos(self, eventos):
        for event in eventos:
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                self.director.salirEscena()
            if self.game_active and event.type == pygame.MOUSEBUTTONDOWN:
                if self.start_time is None:
                    self.start_time = time.time()
                    self.dibujar(self.window) 
                for i, button in enumerate(self.buttons):
                    if (event.pos[0] - button["pos"][0])**2 + (event.pos[1] - button["pos"][1])**2 <= self.button_radius**2:
                        self.flash_button(self.window, button)
                        self.user_sequence.append(i)
                        if not self.check_user_input():
                            self.sound_endgame.play()
                            self.game_active = False
                        elif len(self.user_sequence) == len(self.sequence):
                            self.round_number += 1
                            if self.round_number == self.TARGET_ROUNDS:
                                self.sound_completed.play()
                                self.game_active = False

    def dibujar(self, pantalla):
        pantalla.fill(self.BLACK)
        self.draw_background(pantalla)
        self.draw_buttons(pantalla)
        if self.game_active:
            if self.start_time is not None:
                elapsed_time = int(time.time() - self.start_time)
                remaining_time = max(0, self.COUNTDOWN_TIME - elapsed_time)
                self.draw_text(pantalla, f"Tiempo: {remaining_time}s", self.width//2, 250)
        else:
            if self.round_number == self.TARGET_ROUNDS:
                self.draw_text(self.window, "¡Felicidades!", self.width//2, self.height//2 - 30, 50, self.BLACK, background=True)
                pygame.display.flip()
            else:
                self.draw_text(self.window, "¡Perdiste!", self.width//2, self.height//2 - 30, 50, self.BLACK, background=True)
                pygame.display.flip()
            self.completado = True


if __name__ == "__main__":
    game = SimonDice()
    game.run()