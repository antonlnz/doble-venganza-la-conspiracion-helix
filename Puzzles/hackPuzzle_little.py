import pygame
import sys
import os
from escena import *

class Hack(Escena):
    def __init__(self, director):
        Escena.__init__(self, director)
        os.environ['SDL_VIDEO_CENTERED'] = '1'
        
        # Constantes
        self.TILE_SIZE = 200
        self.GRID_SIZE = 3
        self.SCREEN_WIDTH = self.TILE_SIZE * self.GRID_SIZE
        self.SCREEN_HEIGHT = self.TILE_SIZE * self.GRID_SIZE
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        
        # Creamos un fondo en negro
        self.blank_surface = pygame.Surface((self.TILE_SIZE * self.GRID_SIZE, self.TILE_SIZE * self.GRID_SIZE))
        self.blank_surface.fill(self.BLACK)
        
        # Creamos las letras de HG
        font = pygame.font.Font(None, 600)
        text = font.render("HG", True, self.WHITE)
        text_rect = text.get_rect(center=(self.TILE_SIZE * self.GRID_SIZE // 2, self.TILE_SIZE * self.GRID_SIZE // 2))
        self.blank_surface.blit(text, text_rect)
        
        # Orden inicial del puzzle y orden final
        self.predefined_order = [0, 1, 2, 3, 4, 5, 6, 8, 7]
        self.final_order = list(range(9))
        
        # Creamos las piezas (tiles)
        self.tiles = []
        for y in range(self.GRID_SIZE):
            for x in range(self.GRID_SIZE):
                if not (x == self.GRID_SIZE - 1 and y == self.GRID_SIZE - 1):
                    rect = pygame.Rect(x * self.TILE_SIZE, y * self.TILE_SIZE, self.TILE_SIZE, self.TILE_SIZE)
                    tile = self.blank_surface.subsurface(rect).copy()
                    pygame.draw.rect(tile, self.WHITE, tile.get_rect(), 5)
                    self.tiles.append(tile)
        
        # Creamos la pieza "libre"
        self.tiles.append(pygame.Surface((self.TILE_SIZE, self.TILE_SIZE)))
        self.tiles[-1].fill(self.BLACK)
        
        # Ponemos las piezas en el orden predefinido
        self.tiles = [self.tiles[i] for i in self.predefined_order]
        
        # Creamos la ventana
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        pygame.display.set_caption('Govern of IronRidge')
        
    def is_solved(self):
        return self.predefined_order == self.final_order
    
    def get_blank_tile_index(self):
        return self.predefined_order.index(8)
    
    def swap_tiles(self, index1, index2):
        self.tiles[index1], self.tiles[index2] = self.tiles[index2], self.tiles[index1]
        self.predefined_order[index1], self.predefined_order[index2] = self.predefined_order[index2], self.predefined_order[index1]
    
    def handle_tile_movement(self, pos):
        blank_index = self.get_blank_tile_index()
        blank_x = (blank_index % self.GRID_SIZE) * self.TILE_SIZE
        blank_y = (blank_index // self.GRID_SIZE) * self.TILE_SIZE
        
        for i, tile in enumerate(self.tiles):
            x = (i % self.GRID_SIZE) * self.TILE_SIZE
            y = (i // self.GRID_SIZE) * self.TILE_SIZE
            rect = pygame.Rect(x, y, self.TILE_SIZE, self.TILE_SIZE)
            if rect.collidepoint(pos):
                if (abs(blank_x - x) == self.TILE_SIZE and blank_y == y) or (abs(blank_y - y) == self.TILE_SIZE and blank_x == x):
                    self.swap_tiles(i, blank_index)
                    break
    
    def update(self, tiempo):
        if self.is_solved():
            print("¡Puzzle resuelto!")
            self.completado = True
            if self.retardo():
                self.director.salirEscena()
    def eventos(self, eventos):
        for event in eventos:
            if event.type == pygame.QUIT:
                self.director.salirPrograma()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.handle_tile_movement(event.pos)

    def dibujar(self, pantalla):
        pantalla.fill(self.BLACK)
        for i, tile in enumerate(self.tiles):
            x = (i % self.GRID_SIZE) * self.TILE_SIZE
            y = (i // self.GRID_SIZE) * self.TILE_SIZE
            pantalla.blit(tile, (x, y))
        pygame.display.flip()
        

if __name__ == "__main__":
    director = None  # Replace with actual director instance
    game = Hack(director)
    game.run()
