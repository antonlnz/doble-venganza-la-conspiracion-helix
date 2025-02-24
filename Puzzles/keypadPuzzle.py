import pygame

from settings import *

class KeypadPuzzle: 
    def __init__(self):
        self.font = pygame.font.Font(None, 36)

        self.keypadX = 0.3125*WIDTH #600
        self.keypadY = 0.25*HEIGHT #270
        self.keypad_width = 0.375*WIDTH #720
        self.keypad_height = 0.5*HEIGHT #540
        
        self.button_width = self.keypad_width/3
        self.button_height = self.keypad_height/5

        self.keypad_buttons = [
            ('1', (600, 378)), ('2', (840, 378)), ('3', (1080, 378)), 
            ('4', (600, 486)), ('5', (840, 486)), ('6', (1080, 486)), 
            ('7', (600, 594)), ('8', (840, 594)), ('9', (1080, 594)), 
            ('<-', (600, 702)), ('0', (840, 702)), ('OK', (1080, 702))
        ]

        self.input_text = ""

    def dibujar(self, pantalla):
        pantalla.fill(ROJO) #Temporal

        pygame.draw.rect(pantalla, NEGRO, (self.keypadX - 5, self.keypadY - 5, self.keypad_width + 10, self.keypad_height + 10))

        pygame.draw.rect(pantalla, BLANCO, (self.keypadX, self.keypadY, self.keypad_width, self.button_height))
        window_text = self.font.render(self.input_text, True, NEGRO)
        window_text_rect = window_text.get_rect(center=(self.keypadX + self.keypad_width/2, self.keypadY + self.button_height/2))
        pantalla.blit(window_text, window_text_rect)

        for text, position in self.keypad_buttons:
            x, y = position
            pygame.draw.rect(pantalla, GRIS, (x, y, self.button_width, self.button_height))
            pygame.draw.rect(pantalla, NEGRO, (x, y, self.button_width, self.button_height), 5)
            render_text = self.font.render(text, True, NEGRO)
            text_rect = render_text.get_rect(center=(x + self.button_width/2, y + self.button_height/2))
            pantalla.blit(render_text, text_rect)

    def eventos(self, mouse_click):
        for text, position in self.keypad_buttons:
            x, y = position
            button = pygame.Rect(x, y, self.button_width, self.button_height)
            if button.collidepoint(mouse_click):
                if text == '<-':
                    self.input_text = self.input_text[:-1]
                elif text == 'OK':
                    print("Codigo finalizado")
                else:
                    self.input_text += text
                


    

