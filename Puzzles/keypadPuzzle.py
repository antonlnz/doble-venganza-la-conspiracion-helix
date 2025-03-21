import pygame

import os
from escena import *
from settings import *

class KeypadPuzzle(Escena): 
    def __init__(self, director):
        Escena.__init__(self, director)
        os.environ['SDL_VIDEO_CENTERED'] = '1'

        self.font = pygame.font.Font("Fuentes/SevenSegment.ttf", 36)
        self.game_over_font = pygame.font.Font("Fuentes/PricedownBl.otf", 70)

        self.keypadX = 747 #600
        self.keypadY = 192 #270
        self.keypad_width = 426 #435
        self.keypad_height = 696 #705
        
        self.button_width = 128 #384 margen 51 
        self.button_height = 128 #512 margen 65

        self.background = pygame.image.load('imagenes/Keypad/wall_texture.png')
        self.background = pygame.transform.scale(self.background, (WIDTH, HEIGHT))
        self.keypad_background = pygame.image.load("imagenes/Keypad/TallPanel_S.jpg")
        self.keypad_background = pygame.transform.scale(self.keypad_background, (self.keypad_width + 10, self.keypad_height + 10))
        self.screen_background = pygame.image.load("imagenes/Keypad/Windows_Screen.png") 
        self.screen_background = pygame.transform.scale(self.screen_background, (400, 100))

        self.keys_background = [
            pygame.image.load(f"imagenes/Keypad/keyboard_{i+1}.png") for i in range(9)
        ] + [
            pygame.image.load("imagenes/Keypad/keyboard_backspace_icon.png"),
            pygame.image.load("imagenes/Keypad/keyboard_0.png"),
            pygame.image.load("imagenes/Keypad/keyboard_enter.png")
        ]

        self.sound_end_game = pygame.mixer.Sound("Sonidos/wrong.wav")
        self.sound_completed = pygame.mixer.Sound("Sonidos/completed.wav")
        self.sound_click = pygame.mixer.Sound("Sonidos/click.wav")

        self.keypad_buttons = [
            ('1', (768, 348)), ('2', (896, 348)), ('3', (1024, 348)), 
            ('4', (768, 476)), ('5', (896, 476)), ('6', (1024, 476)), 
            ('7', (768, 604)), ('8', (896, 604)), ('9', (1024, 604)), 
            ('<-', (768, 732)), ('0', (896, 732)), ('OK', (1024, 732))
        ]

        self.keypad_button_click = [
            ((800, 380)), ((928, 380)), ((1056, 380)), 
            ((800, 508)), ((928, 508)), ((1056, 508)), 
            ((800, 636)), ((928, 636)), ((1056, 636)), 
            ((800, 764)), ((928, 764)), ((1050, 794))
        ]

        self.letters_rect = []

        self.mouse_clicks = []
        self.input_text = ""
        self.expected_text = "789456123"
        self.fail = False

    def game_over(self, screen):
        screen.fill(NEGRO)
        game_over_text = self.font.render('You lose', True, ROJO)
        screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - game_over_text.get_height() // 2))
        self.sound_end_game.play()
        pygame.display.flip()
        pygame.time.wait(2000)
        self.sound_end_game.stop()
        self.completado = True
        self.director.salirEscena()

    def click_on_button(self, pos, image, image_pos):
        x, y = pos
        x_image, y_image= image_pos

        x_local = x - x_image
        y_local = y - y_image

        if 0 <= x_local < image.get_width() and 0 <= y_local < image.get_height():
            pixel_color = image.get_at((x_local, y_local))
            if pixel_color.a > 0:
                return True
        return False

    def dibujar(self, pantalla):
        pantalla.blit(self.background, (0, 0))

        pantalla.blit(self.keypad_background, (self.keypadX - 5, self.keypadY - 5, self.keypad_width + 10, self.keypad_height + 10))

        pantalla.blit(self.screen_background, (self.keypadX+13, self.keypadY+14, self.keypad_width, self.button_height))
        
        window_text = self.font.render(self.input_text, True, NEGRO)
        window_text_rect = window_text.get_rect(center=(self.keypadX + self.keypad_width/2, self.keypadY + self.button_height/2))
        pantalla.blit(window_text, window_text_rect)

        for i, position in enumerate(self.keypad_button_click):
            x, y = position
            if i == 11:
                rect = pygame.Rect(x, y, self.button_width//2 + 10, self.button_height//3)    
            else:
                rect = pygame.Rect(x, y, self.button_width//2, self.button_height//2)

            pygame.draw.rect(pantalla, NEGRO, rect)

            self.letters_rect.append(rect)

        for (text, position), image in zip(self.keypad_buttons, self.keys_background):
            x, y = position
            
            #pygame.draw.rect(pantalla, NEGRO, (x, y, self.button_width, self.button_height))
            pantalla.blit(image, (x, y, self.button_width, self.button_height))
        
        if self.fail:
            self.game_over(pantalla)

    def eventos(self, eventos):
        for evento in eventos:
            if evento.type == pygame.QUIT:
                self.director.salirEscena()
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if evento.button == 1:
                    self.mouse_clicks.append(evento.pos)

    def update(self, tiempo):
        for click_pos in self.mouse_clicks:
            for (text, position), image, button_letter in zip(self.keypad_buttons, self.keys_background, self.letters_rect):  
                x, y = position
                button = pygame.Rect(x, y, self.button_width, self.button_height)
                if button.collidepoint(click_pos) and self.click_on_button(click_pos, image, position) or button_letter.collidepoint(click_pos):
                    self.sound_click.play() 
                    if text == '<-':
                        self.input_text = self.input_text[:-1]
                    elif text == 'OK':
                        if self.input_text == self.expected_text:
                            pygame.time.delay(500)
                            self.sound_completed.play()
                            self.input_text = ""
                            self.completado = True
                            #self.sound_completed.stop() #preguntar
                            self.director.salirEscena()
                        else:
                            pygame.time.delay(500)
                            self.fail = True
                    else:
                        self.input_text += text
        self.mouse_clicks.clear()
                
if __name__ == "__main__":
    director = None  # Replace with actual director object if available
    keypad = KeypadPuzzle(director)
    keypad.run()


    

