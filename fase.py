import pygame
import pytmx
from pygame.locals import *

from Puzzles.cardPuzzle import CardPuzzle
from Puzzles.keypadPuzzle import KeypadPuzzle
from ayuntamiento import Ayuntamiento


class Fase:
    def __init__(self):  
        self.ayuntamiento = Ayuntamiento()
        self.cardPuzle = CardPuzzle()
        self.keypadPuzzle = KeypadPuzzle()



    def dibujar(self, pantalla):
        self.ayuntamiento.dibujar(pantalla)
        self.cardPuzle.dibujar(pantalla)
        #self.keypadPuzzle.dibujar(pantalla)

    def update(self, tiempo):
        self.cardPuzle.update(tiempo)

    def eventos(self, lista_eventos):
        # Miramos a ver si hay algun evento de salir del programa
        for evento in lista_eventos:
            # Si se sale del programa
            if evento.type == pygame.QUIT or (evento.type == KEYDOWN and evento.key == K_ESCAPE):
                return True
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if evento.button == 1:
                    self.keypadPuzzle.eventos(evento.pos)

        # Indicamos la acción a realizar segun la tecla pulsada para cada jugador
        teclasPulsadas = pygame.key.get_pressed()
        self.cardPuzle.eventos(teclasPulsadas[K_SPACE])
        # if teclasPulsadas[K_SPACE]:
        #     self.indicadorColor = VERDE
        # else:
        #     self.indicadorColor = BLANCO
        # No se sale del programa
        return False





