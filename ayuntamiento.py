import pygame
import pytmx

from personajes import *
from settings import *


class Ayuntamiento:
    def __init__(self):
        self.tmxdata = pytmx.load_pygame("Mapas/ayuntamiento48x48.tmx")

        self.width = self.tmxdata.width * self.tmxdata.tilewidth
        self.height = self.tmxdata.height * self.tmxdata.tileheight
        self.grupoObstaculos = pygame.sprite.Group()

        for tile_object in self.tmxdata.objects:
            self.grupoObstaculos.add(Obstacle(pygame.Rect(tile_object.x, tile_object.y, tile_object.width, tile_object.height)))

        

    def dibujar(self,pantalla):
        ti = self.tmxdata.get_tile_image_by_gid
        
        for layer in self.tmxdata.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, gid, in layer:
                    tile = ti(gid)
                    
                    if tile:
                        pantalla.blit(tile, (x * self.tmxdata.tilewidth, y * self.tmxdata.tileheight))       
    
    def make_map(self):
        temp_surface = pygame.Surface((self.width, self.height)).convert()
        self.dibujar(temp_surface)
        return temp_surface
    

class Obstacle(MiSprite):
    def __init__(self,rectangulo):
        # Primero invocamos al constructor de la clase padre
        MiSprite.__init__(self)
        # Rectangulo con las coordenadas en pantalla que ocupara
        self.rect = rectangulo
        # Y lo situamos de forma global en esas coordenadas
        self.establecerPosicion((self.rect.left, self.rect.bottom))

        # self.image = pygame.Surface((0, 0))