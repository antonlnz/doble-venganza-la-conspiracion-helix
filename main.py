#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Importar modulos

import pygame
from director import *
from periodico_fabrica import Periodico_Fabrica
from settings import *



if __name__ == '__main__':

    # Inicializamos la libreria de pygame
    pygame.init()
    # Creamos el director
    director = Director()
    # Creamos la escena con la pantalla inicial
    escena = Periodico_Fabrica(director)
    # Le decimos al director que apile esta escena
    director.apilarEscena(escena)
    # Y ejecutamos el juego
    director.ejecutar()
    # Cuando se termine la ejecución, finaliza la librería
    pygame.quit()


