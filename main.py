#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Importar modulos

import sys
import pygame
from fase import *
from settings import *



if __name__ == '__main__':

    # Inicializar pygame
    pygame.init()

    # Crear la pantalla
    pantalla = pygame.display.set_mode((WIDTH,HEIGHT))

    # Creamos el objeto reloj para sincronizar el juego
    reloj = pygame.time.Clock()

    # Creamos la fase
    
    fase = Fase()


    # El bucle de eventos
    while True:

        # Sincronizar el juego a 60 fps
        tiempo_pasado = reloj.tick(60)

        # Coge la lista de eventos y se la pasa a la escena
        # Devuelve si se debe parar o no el juego
        # if (fase.eventos(pygame.event.get())):
        #     pygame.quit()
        #     sys.exit()

        # Actualiza la escena
        # Devuelve si se debe parar o no el juego
        # if (fase.update(tiempo_pasado)):
        #     pygame.quit()
        #     sys.exit()


        if (fase.eventos(pygame.event.get())):
            pygame.quit()
            sys.exit()
        # for evento in pygame.event.get():

        #         # Si el evento es la pulsación de la tecla Escape
        #         if evento.type == KEYDOWN and evento.key == K_ESCAPE:
        #                 # Se sale del programa
        #                 pygame.quit()
        #                 sys.exit()
        #         if evento.type == KEYDOWN and evento.key == K_SPACE:
        #             # self.indicadorColor = VERDE
        #             print("ENTRO")

        # for event in pygame.event.get():
            
        # Se dibuja en pantalla
        pantalla.fill((0,0,0))

        fase.update(tiempo_pasado)
        
        fase.dibujar(pantalla)
        pygame.display.flip()

