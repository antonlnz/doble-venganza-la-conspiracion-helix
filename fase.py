import pygame
import pytmx
from pygame.locals import *

from Puzzles.cardPuzzle import CardPuzzle
from Puzzles.keypadPuzzle import KeypadPuzzle
from ayuntamiento import Ayuntamiento
from Puzzles.sortingGridPuzzle import SortingGridPuzzle
from personajes import *
from settings import *


class Fase:
    def __init__(self):  
        self.ayuntamiento = Ayuntamiento()
        self.cardPuzle = CardPuzzle()
        self.keypadPuzzle = KeypadPuzzle()
        self.sorting = SortingGridPuzzle()

        self.jugador1 = Jugador()
        self.grupoJugadores = pygame.sprite.Group( self.jugador1)
        self.jugador1.establecerPosicion((200, 551))

        self.grupoSpritesDinamicos = pygame.sprite.Group( self.jugador1)
        self.grupoSprites = pygame.sprite.Group( self.jugador1)


    def dibujar(self, pantalla):
        self.ayuntamiento.dibujar(pantalla)
        self.cardPuzle.dibujar(pantalla)
        self.keypadPuzzle.dibujar(pantalla)
        self.grupoSprites.draw(pantalla)
        self.sorting.dibujar(pantalla)

    def update(self, tiempo):
        self.cardPuzle.update(tiempo)
        self.grupoSpritesDinamicos.update(self.ayuntamiento.grupoObstaculos, tiempo)

    def eventos(self, lista_eventos):
        # Miramos a ver si hay algun evento de salir del programa
        for evento in lista_eventos:
            # Si se sale del programa
            if evento.type == pygame.QUIT or (evento.type == KEYDOWN and evento.key == K_ESCAPE):
                return True

        # Indicamos la acción a realizar segun la tecla pulsada para cada jugador
        teclasPulsadas = pygame.key.get_pressed()
        self.cardPuzle.eventos(teclasPulsadas[K_SPACE])
        self.jugador1.mover(teclasPulsadas, K_UP, K_DOWN, K_LEFT, K_RIGHT)
        # if teclasPulsadas[K_SPACE]:
        #     self.indicadorColor = VERDE
        # else:
        #     self.indicadorColor = BLANCO
        # No se sale del programa
        return False





