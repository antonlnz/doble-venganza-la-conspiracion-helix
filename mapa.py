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

        self.mision = Mision()

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
          self.objetoCambiado = False

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

        self.objetoCambiado = True          
        # grupoSprites.add(self.objetoFinal)
        # grupoDepuesPersonaje.add(self.objetoFinal)

class GrupoObjetosParaCambiar():
    def __init__(self):
          self.objetosIniciales = []
          self.objetosFinales = []
          self.objetoCambiado = False

    def establecerObjeto(self, object, gruposParaAñadir):
        
        obj = Object(pygame.Rect(object.x, object.y, object.width, object.height), object.image)

        if object.name == "Inicial":
            self.objetosIniciales.append(obj)
            for grupo in gruposParaAñadir:
                grupo.add(obj)
                        
        elif object.name == "Final":
            self.objetosFinales.append(obj)

    def cambiar(self, gruposParaAñadir):
        for objInicial in self.objetosIniciales:
            for grupo in objInicial.groups():
                grupo.remove(objInicial)

        for objFinal in self.objetosFinales:
            for grupo in gruposParaAñadir:
                grupo.add(objFinal)  

        self.objetoCambiado = True

    # def objetosInicialesAñadirGrupos(self, gruposParaAñadir):
    #     for objInicial in self.objetosIniciales:
    #         for grupo in gruposParaAñadir:
    #             grupo.add(objInicial)  

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

    def cambiarTarget(self, target):
        self.target = target

class PosicionamientoInteraccion():
    def __init__(self, escena, posicion, textoMision):
        self.escena = escena
        self.posicion = posicion
        self.textoMision = textoMision
        self.scroll = (0, 0)

    def update(self, scroll):
        self.scroll = scroll

    def puedeActivar(self, target):
        (posx, posy) = self.posicion
        (scrollx, scrolly) = self.scroll
        return(abs((posx - scrollx) - target.rect.centerx) < 48 and abs((posy - scrolly) - target.rect.centery) < 48)
    
    def establecerPosicion(self, posicion):
        self.posicion = posicion
        
    

class PosicionamientoInteraccionRobo():
    def __init__(self, robo, posicion):
        self.robo = robo
        self.posicion = posicion
        self.scroll = (0, 0)

    def update(self, scroll):
        self.scroll = scroll

    def puedeActivar(self, target):
        (posx, posy) = self.posicion
        (scrollx, scrolly) = self.scroll
        return (abs((posx - scrollx) - target.rect.centerx) < 48 and abs((posy - scrolly) - target.rect.centery) < 48) and not self.robo.objetoCambiado
    

class Mision():
    def __init__(self):
        self.texto = "Texto por defecto no cambiado"
        self.medium_font = pygame.font.SysFont('Arial', 22, bold=True)

        self.actualizar_dimensiones()

    def actualizar_dimensiones(self):
        """Calcula el tamaño de la caja según el texto actual"""
        lineas = self.texto.split("\n")
        max_ancho = max(self.medium_font.size(linea)[0] for linea in lineas) + 20  # Margen
        total_alto = len(lineas) * (self.medium_font.get_height() + 5) + 20  # Espaciado

        self.mision_width = max_ancho
        self.mision_height = total_alto
        self.mision_x = WIDTH - self.mision_width - 10  # Ajustar posición
        self.mision_y = 10  # Mantener arriba

    def dibujar(self, pantalla):
        
        
        # Crear un fondo negro semitransparente para la pregunta
        mision_bg = pygame.Surface((self.mision_width, self.mision_height), pygame.SRCALPHA)
        mision_bg.fill((0, 0, 0, 180))  # Negro semitransparente
        pantalla.blit(mision_bg, (self.mision_x, self.mision_y))
        
        # Mostrar pregunta con una fuente más grande
        

        self.dibujar_texto_con_saltos(pantalla)
        # mision_surface = self.medium_font.render(self.texto, True, BLANCO)
        # pantalla.blit(mision_surface, (self.mision_x + 20, self.mision_y + 20))
  
    def dibujar_texto_con_saltos(self, pantalla):
        # """Dibuja un texto en la pantalla manejando los saltos de línea (\n)"""
        lineas = self.texto.split("\n")  # Divide el texto en líneas
        y_offset = 0  # Desplazamiento vertical entre líneas
        for linea in lineas:
            superficie_texto = self.medium_font.render(linea, True, BLANCO)
            pantalla.blit(superficie_texto, (self.mision_x + 10, self.mision_y + 10 + y_offset))
            y_offset += self.medium_font.get_height() + 5  # Espaciado entre líneas

    def establecerTexto(self, texto):
        self.texto = texto
        self.actualizar_dimensiones()