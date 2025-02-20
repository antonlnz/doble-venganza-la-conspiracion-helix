import pygame
import pytmx


class Ayuntamiento:
    def __init__(self):
        self.tmxdata = pytmx.load_pygame("Mapas/ayuntamiento48x48.tmx")

        self.width = self.tmxdata.width * self.tmxdata.tilewidth
        self.height = self.tmxdata.height * self.tmxdata.tileheight
        

    def dibujar(self,pantalla):
        ti = self.tmxdata.get_tile_image_by_gid
        
        for layer in self.tmxdata.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, gid, in layer:
                    tile = ti(gid)
                    if tile:
                        pantalla.blit(tile, (x * self.tmxdata.tilewidth, y * self.tmxdata.tileheight))
        
        
    
    def make_map(self):
        temp_surface = pygame.Surface((self.width, self.height))
        self.dibujar(temp_surface)
        return temp_surface