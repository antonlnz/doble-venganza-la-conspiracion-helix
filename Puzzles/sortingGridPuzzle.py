import random
import pygame
from settings import *
from escena import Escena
import os


class SortingGridPuzzle(Escena):
    
    def __init__(self, director):
        Escena.__init__(self, director)
        os.environ['SDL_VIDEO_CENTERED'] = '1'

        self.grid_size = 3
        self.gridX = 660 #1920 - 600 = 1320 / 2 = 660
        self.gridY = 240 #1080 - 600 = 480 / 2 = 240
        self.tile_size = 200 

        self.font = pygame.font.Font(None, 20)

        self.numbers = list(range(1, self.grid_size*self.grid_size))
        self.numbers.append(0)
        random.shuffle(self.numbers)

        self.positions = [(col, row) for row in range(self.grid_size) for col in range(self.grid_size)]

        self.expected_result = [1, 2, 3, 4, 5, 6, 7, 8, 0]

        self.mouse_clicks = None
        self.click = False

        self.empty = self.positions[self.numbers.index(0)]  # Encuentra la posición del espacio vacío

    #def move(self, pos):
    #    empty_row, empty_col = self.empty
    #    if ((abs(empty_row - row) == 1 and empty_col == col) or (abs(empty_col - col) == 1 and empty_row == row)) :
    #        self.positions[empty_row][empty_col], self.positions[row][col] = self.positions[row][col], self.positions[empty_row][empty_col]
    #        self.empty = (row, col)

    def dibujar(self, pantalla):
        pantalla.fill(ROJO) #temporal

        pygame.draw.rect(pantalla, NEGRO, (655, 235, self.tile_size*3 + 10 , self.tile_size*3 + 10))

        for i, (col, row) in enumerate(self.positions):
            if self.numbers[i] != 0:
                pygame.draw.rect(pantalla, GRIS, (col*self.tile_size + self.gridX, row*self.tile_size + self.gridY, self.tile_size, self.tile_size))
                pygame.draw.rect(pantalla, NEGRO, (col*self.tile_size + self.gridX, row*self.tile_size + self.gridY, self.tile_size, self.tile_size), 5)

                number_text = self.font.render(str(self.numbers[i]), True, NEGRO)
                text_rect = number_text.get_rect(center=(self.gridX + col*self.tile_size + self.tile_size/2, self.gridY + row*self.tile_size + self.tile_size/2 ))
                pantalla.blit(number_text, text_rect)

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
            self.director.salirEscena()
            self.completado = True


    def eventos(self, eventos):
        for evento in eventos:
            if evento.type == pygame.QUIT:
                self.director.salirEscena()
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if evento.button == 1:
                    self.click = True
                    x, y = evento.pos
                    col = int((x - self.gridX) / self.tile_size)
                    row = int((y - self.gridY) / self.tile_size)
                    self.mouse_clicks = (col, row)

if __name__ == "__main__":
    director = None  # Replace with actual director object if available
    gridPuzzle = SortingGridPuzzle(director)
    gridPuzzle.run()