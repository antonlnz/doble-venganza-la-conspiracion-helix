# -*- coding: utf-8 -*-

import pygame, sys, os
from pygame.locals import *
from gestorRecursos import *

# -------------------------------------------------
# -------------------------------------------------
# Constantes
# -------------------------------------------------
# -------------------------------------------------

# Movimientos
QUIETO = 0
IZQUIERDA = 1
DERECHA = 2
ARRIBA = 3
ABAJO = 4
ARRIBA_IZQUIERDA = 5
ARRIBA_DERECHA = 6
ABAJO_IZQUIERDA = 7
ABAJO_DERECHA = 8

#Posturas
SPRITE_QUIETO = 0
SPRITE_ANDANDO = 1

# Velocidades de los distintos personajes
VELOCIDAD_JUGADOR = 0.2 # Pixeles por milisegundo
VELOCIDAD_SALTO_JUGADOR = 0.3 # Pixeles por milisegundo
RETARDO_ANIMACION_JUGADOR = 5 # updates que durará cada imagen del personaje
                              # debería de ser un valor distinto para cada postura


# -------------------------------------------------
# -------------------------------------------------
# Funciones auxiliares
# -------------------------------------------------
# -------------------------------------------------


# -------------------------------------------------
# -------------------------------------------------
# Clases de los objetos del juego
# -------------------------------------------------
# -------------------------------------------------


# -------------------------------------------------
# Clase MiSprite
class MiSprite(pygame.sprite.Sprite):
    "Los Sprites que tendra este juego"
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.posicion = (0, 0)
        self.velocidad = (0, 0)
        self.scroll   = (0, 0)

    def establecerPosicion(self, posicion):
        self.posicion = posicion
        self.rect.left = self.posicion[0] - self.scroll[0]
        self.rect.bottom = self.posicion[1] - self.scroll[1]

    def establecerPosicionPantalla(self, scrollDecorado):
        self.scroll = scrollDecorado;
        (scrollx, scrolly) = self.scroll;
        (posx, posy) = self.posicion;
        self.rect.left = posx - scrollx;
        self.rect.bottom = posy - scrolly;

    def incrementarPosicion(self, incremento):
        (posx, posy) = self.posicion
        (incrementox, incrementoy) = incremento
        self.establecerPosicion((posx+incrementox, posy+incrementoy))

    def update(self, tiempo):
        incrementox = self.velocidad[0]*tiempo
        incrementoy = self.velocidad[1]*tiempo
        self.incrementarPosicion((incrementox, incrementoy))



# -------------------------------------------------
# Clases Personaje

#class Personaje(pygame.sprite.Sprite):
class Personaje(MiSprite):
    "Cualquier personaje del juego"

    # Parametros pasados al constructor de esta clase:
    #  Archivo con la hoja de Sprites
    #  Archivo con las coordenadoas dentro de la hoja
    #  Numero de imagenes en cada postura
    #  Velocidad de caminar y de salto
    #  Retardo para mostrar la animacion del personaje
    def __init__(self, archivoImagen, archivoCoordenadas, numImagenes, velocidad, retardoAnimacion):

        # Primero invocamos al constructor de la clase padre
        MiSprite.__init__(self);

        # Se carga la hoja
        self.hoja = GestorRecursos.CargarImagen(archivoImagen, -1)

        self.hoja = self.hoja.convert_alpha()
        # El movimiento que esta realizando
        self.movimiento = QUIETO
        # Lado hacia el que esta mirando
        self.mirando = IZQUIERDA

        # Leemos las coordenadas de un archivo de texto
        datos = GestorRecursos.CargarArchivoCoordenadas(archivoCoordenadas)
        datos = datos.split()
        self.numPostura = 1;
        self.numImagenPostura = 0;
        cont = 0;
        self.coordenadasHoja = [];
        for linea in range(0, 2):
            self.coordenadasHoja.append([])
            tmp = self.coordenadasHoja[linea]
            for postura in range(1, numImagenes[linea]+1):
                tmp.append(pygame.Rect((int(datos[cont]), int(datos[cont+1])), (int(datos[cont+2]), int(datos[cont+3]))))
                cont += 4

        # El retardo a la hora de cambiar la imagen del Sprite (para que no se mueva demasiado rápido)
        self.retardoMovimiento = 0;

        # En que postura esta inicialmente
        self.numPostura = QUIETO

        # El rectangulo del Sprite
        self.rect = pygame.Rect(100,100,self.coordenadasHoja[self.numPostura][self.numImagenPostura][2],self.coordenadasHoja[self.numPostura][self.numImagenPostura][3])
        
        # Las velocidades de caminar y salto
        self.velocidadX = velocidad
        self.velocidadY = velocidad
        self.velocidadDiagonal = velocidad * 0.707

        # El retardo en la animacion del personaje (podria y deberia ser distinto para cada postura)
        self.retardoAnimacion = retardoAnimacion

        # Y actualizamos la postura del Sprite inicial, llamando al metodo correspondiente
        self.actualizarPostura()


    # Metodo base para realizar el movimiento: simplemente se le indica cual va a hacer, y lo almacena
    def mover(self, movimiento):
            self.movimiento = movimiento


    def actualizarPostura(self):
        self.retardoMovimiento -= 1
        # Miramos si ha pasado el retardo para dibujar una nueva postura
        if (self.retardoMovimiento < 0):
            self.retardoMovimiento = self.retardoAnimacion
            # Si ha pasado, actualizamos la postura
            self.numImagenPostura += 1
            if self.numImagenPostura >= len(self.coordenadasHoja[self.numPostura]):
                self.numImagenPostura = 0;
            if self.numImagenPostura < 0:
                self.numImagenPostura = len(self.coordenadasHoja[self.numPostura])-1
            self.image = self.hoja.subsurface(self.coordenadasHoja[self.numPostura][self.numImagenPostura])

            # Si esta mirando a la izquiera, cogemos la porcion de la hoja
            if self.mirando == DERECHA:
                self.image = self.hoja.subsurface(self.coordenadasHoja[self.numPostura][self.numImagenPostura])
            #  Si no, si mira a la derecha, invertimos esa imagen
            elif self.mirando == IZQUIERDA:
                self.image = pygame.transform.flip(self.hoja.subsurface(self.coordenadasHoja[self.numPostura][self.numImagenPostura]), 1, 0)


    def update(self, grupoObstaculos, tiempo):

        # Las velocidades a las que iba hasta este momento
        (velocidadx, velocidady) = self.velocidad

        # Si vamos a la izquierda o a la derecha  

        # Si no se ha pulsado ninguna tecla
        if self.movimiento == QUIETO:
            velocidadx = 0
            velocidady = 0
        else:
            if self.movimiento == ARRIBA_IZQUIERDA:
                self.mirando = IZQUIERDA
                velocidadx = -self.velocidadDiagonal
                velocidady = -self.velocidadDiagonal

            elif self.movimiento == ARRIBA_DERECHA:
                self.mirando = DERECHA
                velocidadx = self.velocidadDiagonal
                velocidady = -self.velocidadDiagonal

            elif self.movimiento == ABAJO_IZQUIERDA:
                self.mirando = IZQUIERDA
                velocidadx = -self.velocidadDiagonal
                velocidady = self.velocidadDiagonal

            elif self.movimiento == ABAJO_DERECHA:
                self.mirando = DERECHA
                velocidadx = self.velocidadDiagonal
                velocidady = self.velocidadDiagonal

            elif self.movimiento == IZQUIERDA:
                self.mirando = self.movimiento
                velocidadx = -self.velocidadX
                velocidady = 0

            elif self.movimiento == DERECHA:
                self.mirando = self.movimiento
                velocidadx = self.velocidadX
                velocidady = 0

            elif self.movimiento == ARRIBA:
                velocidadx = 0
                velocidady = -self.velocidadY

            elif self.movimiento == ABAJO:
                velocidadx = 0
                velocidady = self.velocidadY

            hits = pygame.sprite.spritecollide(self, grupoObstaculos, False)
            for hit in hits:
                if hit:
                    if abs(hit.rect.top - self.rect.bottom) < 10 and velocidady > 0:
                        velocidady = 0
                        
                    if abs(hit.rect.bottom - self.rect.bottom) < 10 and velocidady < 0:
                        velocidady = 0

                    if abs(hit.rect.right - self.rect.left) < 10 and velocidadx < 0 and hit.rect.bottom > self.rect.bottom and (hit.rect.top + 10) < self.rect.bottom:
                        velocidadx = 0

                    if abs(hit.rect.left - self.rect.right) < 10 and velocidadx > 0 and hit.rect.bottom > self.rect.bottom and (hit.rect.top + 10) < self.rect.bottom:
                        velocidadx = 0

        if (velocidadx == 0) and (velocidady == 0):
            self.numPostura = SPRITE_QUIETO
        else:
            self.numPostura = SPRITE_ANDANDO

        # Actualizamos la imagen a mostrar
        self.actualizarPostura()

        # Aplicamos la velocidad en cada eje      
        self.velocidad = (velocidadx, velocidady)

        # Y llamamos al método de la superclase para que, según la velocidad y el tiempo
        #  calcule la nueva posición del Sprite
        MiSprite.update(self, tiempo)
        
        return



# -------------------------------------------------
# Clase Jugador

class Jugador(Personaje):
    "Cualquier personaje del juego"
    def __init__(self, archivoImagen, archivoCoordenadas, numImagenes):
        # Invocamos al constructor de la clase padre con la configuracion de este personaje concreto
        Personaje.__init__(self, archivoImagen, archivoCoordenadas, numImagenes, VELOCIDAD_JUGADOR, RETARDO_ANIMACION_JUGADOR)


    def mover(self, teclasPulsadas, arriba, abajo, izquierda, derecha):
        # Indicamos la acción a realizar segun la tecla pulsada para el jugador
        if teclasPulsadas[arriba] and teclasPulsadas[izquierda]:
            Personaje.mover(self,ARRIBA_IZQUIERDA)
        elif teclasPulsadas[arriba] and teclasPulsadas[derecha]:
            Personaje.mover(self,ARRIBA_DERECHA)
        elif teclasPulsadas[abajo] and teclasPulsadas[izquierda]:
            Personaje.mover(self,ABAJO_IZQUIERDA)
        elif teclasPulsadas[abajo] and teclasPulsadas[derecha]:
            Personaje.mover(self,ABAJO_DERECHA)
        elif teclasPulsadas[arriba]:
            Personaje.mover(self,ARRIBA)
        elif teclasPulsadas[izquierda]:
            Personaje.mover(self,IZQUIERDA)
        elif teclasPulsadas[derecha]:
            Personaje.mover(self,DERECHA)
        elif teclasPulsadas[abajo]:
            Personaje.mover(self,ABAJO)
        else:
            Personaje.mover(self,QUIETO)

    def moverEnYHasta(self, y, variacion):
        (posx, posy) = self.posicion
        if(posy < (y-variacion)):
            velocidady = 1
            self.movimiento = ABAJO
            return False
        elif(posy > (y + variacion)):
            velocidady = -1
            self.movimiento = ARRIBA
            return False
        else:
            velocidady = 0
            self.movimiento = QUIETO
            return True

