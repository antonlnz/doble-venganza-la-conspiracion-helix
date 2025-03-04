import math
import numpy
import pygame
import pytmx

from personajes import *
from settings import *


class Ayuntamiento:
    def __init__(self):
        self.tmxdata = pytmx.load_pygame("Mapas/ayuntamiento48x48v2.tmx")

        

        self.jugador1 = Jugador()
        self.grupoJugadores = pygame.sprite.Group( self.jugador1)

        self.grupoSpritesDinamicos = pygame.sprite.Group( self.jugador1)
        self.grupoSprites = pygame.sprite.Group()

        self.offset = pygame.math.Vector2()
        self.half_w = WIDTH//2
        self.half_h = HEIGHT//2

        self.jugador1.establecerPosicion((self.half_w, self.half_h))

        self.center_target_camera(self.jugador1)

        self.width = self.tmxdata.width * self.tmxdata.tilewidth
        self.height = self.tmxdata.height * self.tmxdata.tileheight
        self.grupoObstaculos = pygame.sprite.Group()
        self.grupoObjetos = pygame.sprite.Group()
        self.grupoTiles = pygame.sprite.Group()
        
        for layer in self.tmxdata.visible_layers:
            if hasattr(layer,'data'):
                for x, y, surf, in layer.tiles():
                    obj = Object(pygame.Rect(x * self.tmxdata.tilewidth, y * self.tmxdata.tileheight, self.tmxdata.tilewidth, self.tmxdata.tileheight), surf)
                    self.grupoTiles.add(obj)
                    self.grupoSprites.add(obj)

        for objectGroup in self.tmxdata.objectgroups:
            if objectGroup.name == "Obstáculos":
                for object in objectGroup:
                    self.grupoObstaculos.add(Obstacle(pygame.Rect(object.x, object.y, object.width, object.height)))

            elif objectGroup.name == "PuertasAbiertas":
                for object in objectGroup: 
                    obj = Object(pygame.Rect(object.x, object.y, object.width, object.height), object.image)
                    self.grupoObjetos.add(obj)
                    self.grupoSprites.add(obj)
            else:
                for object in objectGroup: 
                    obj = Object(pygame.Rect(object.x, object.y, object.width, object.height), object.image)
                    self.grupoObstaculos.add(obj)
                    self.grupoObjetos.add(obj)
                    self.grupoSprites.add(obj)
           
        self.grupoSprites.add(self.jugador1)


    def center_target_camera(self, target):
        (posx, posy) = target.posicion
        self.offset.x = posx - self.half_w
        self.offset.y = posy - self.half_h
        

    def dibujar(self,pantalla):
        
        # self.grupoTiles.draw(pantalla)
        # self.grupoObjetos.draw(pantalla)
        self.grupoSprites.draw(pantalla)
        # pygame.draw.rect(pantalla, ROJO, self.jugador1.rect)

    def eventos(self, lista_eventos):
        for evento in lista_eventos:
            # Si se sale del programa
            if evento.type == pygame.QUIT or (evento.type == KEYDOWN and evento.key == K_ESCAPE):
                return True

        teclasPulsadas = pygame.key.get_pressed()
        self.jugador1.mover(teclasPulsadas, K_UP, K_DOWN, K_LEFT, K_RIGHT)
    
    def update(self, tiempo):
        self.center_target_camera(self.jugador1)
        self.grupoSpritesDinamicos.update(self.grupoObstaculos, tiempo)

        for sprite in iter(self.grupoObstaculos):
                sprite.establecerPosicionPantalla(self.offset)

        for sprite in iter(self.grupoObjetos):
                sprite.establecerPosicionPantalla(self.offset)

        for sprite in iter(self.grupoTiles):
                sprite.establecerPosicionPantalla(self.offset)

        for sprite in iter(self.grupoSprites):
                sprite.establecerPosicionPantalla(self.offset)
    

class Obstacle(MiSprite):
    def __init__(self,rectangulo):
        # Primero invocamos al constructor de la clase padre
        MiSprite.__init__(self)
        # Rectangulo con las coordenadas en pantalla que ocupara
        self.rect = rectangulo
        # Y lo situamos de forma global en esas coordenadas
        self.establecerPosicion((self.rect.left, self.rect.bottom))


class Object(MiSprite):
    def __init__(self,rectangulo, imagen):
        # Primero invocamos al constructor de la clase padre
        MiSprite.__init__(self)
        # Rectangulo con las coordenadas en pantalla que ocupara
        self.rect = rectangulo
        # Y lo situamos de forma global en esas coordenadas
        self.establecerPosicion((self.rect.left, self.rect.bottom))
        
        self.image = imagen