import pygame
import pytmx

from personajes import *
from settings import *
from escena import *
from mapa import *

class Mapa(Escena):
    def __init__(self, director, mapa):
        super().__init__(director)
        self.offset = pygame.math.Vector2()
        self.half_w = WIDTH//2
        self.half_h = HEIGHT//2

        self.grupoSpritesDinamicos = pygame.sprite.Group()
        self.grupoSprites = pygame.sprite.Group()

        self.grupoObstaculos = pygame.sprite.Group()
        # self.grupoObjetos = pygame.sprite.Group()
        # self.grupoTiles = pygame.sprite.Group()
        self.grupoDespuesPersonaje = pygame.sprite.Group()

        self.tmxdata = pytmx.load_pygame(mapa)

        for layer in self.tmxdata.visible_layers:
            if hasattr(layer,'data'):
                if layer.name == "DespuesPersonaje":  
                    for x, y, surf, in layer.tiles():
                        obj = Object(pygame.Rect(x * self.tmxdata.tilewidth, y * self.tmxdata.tileheight, self.tmxdata.tilewidth, self.tmxdata.tileheight), surf)
                        # self.grupoTiles.add(obj)
                        self.grupoDespuesPersonaje.add(obj)
                        self.grupoSprites.add(obj)
                else:
                     for x, y, surf, in layer.tiles():
                        obj = Object(pygame.Rect(x * self.tmxdata.tilewidth, y * self.tmxdata.tileheight, self.tmxdata.tilewidth, self.tmxdata.tileheight), surf)
                        # self.grupoTiles.add(obj)
                        self.grupoSprites.add(obj)

    def center_target_camera(self, target):
        (posx, posy) = target.posicion
        self.offset.x = posx - WIDTH//2
        self.offset.y = posy - HEIGHT//2

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

class ObjetoParaCambiar():
    def __init__(self):
          self.objetoInicial = None
          self.objetoFinal = None

    def establecerObjeto(self, object, gruposParaAñadir):
        
        obj = Object(pygame.Rect(object.x, object.y, object.width, object.height), object.image)

        if object.name == "Inicial":
            self.objetoInicial = obj
            for grupo in gruposParaAñadir:
                grupo.add(self.objetoInicial)
                        
        elif object.name == "Final":
            self.objetoFinal = obj

    def cambiar(self, gruposParaAñadir):
        for grupo in self.objetoInicial.groups():
             grupo.remove(self.objetoInicial)

        for grupo in gruposParaAñadir:
                grupo.add(self.objetoFinal)            
        # grupoSprites.add(self.objetoFinal)
        # grupoDepuesPersonaje.add(self.objetoFinal)

class TeclaInteraccion(MiSprite):
    def __init__(self, target):
        MiSprite.__init__(self)
        self.image = GestorRecursos.CargarImagen('E.png', -1)  
        self.image = pygame.transform.scale(self.image, (48, 48))
        self.target = target
        self.rect = self.image.get_rect()
        self.pintar = False

        self.establecerPosicion((WIDTH//2 + 40, HEIGHT//2 - 70))

    def update(self):
        # self.establecerPosicion((self.target.posicion[0] + 5, self.target.posicion[1] + 5))
        print(self.pintar)

    def dibujar(self, pantalla):
        if self.pintar:
            pantalla.blit(self.image, self.rect)

    def mostrar(self):
        self.pintar = True
    
    def ocultar(self):
        self.pintar = False

class PosicionamientoInteraccion():
    def __init__(self, escena, posicion):
        self.escena = escena
        self.posicion = posicion
        self.scroll = (0, 0)

    def update(self, scroll):
        self.scroll = scroll

    def puedeActivar(self, target):
        (posx, posy) = self.posicion
        (scrollx, scrolly) = self.scroll
        return(abs((posx - scrollx) - target.rect.centerx) < 48 and abs((posy - scrolly) - target.rect.centery) < 48)