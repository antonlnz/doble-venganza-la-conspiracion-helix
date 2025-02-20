
import pygame

from settings import *


     
class CardPuzzle:
    def __init__(self):
        self.lineaPequeñaX = WIDTH*0.1
        self.lineaPequeñaY = HEIGHT*0.05
        self.lineaGrandeX = WIDTH*0.8
        self.lineaGrandeY = HEIGHT*0.05
        self.indicadorWidth = WIDTH*0.01
        self.indicadorHeight = HEIGHT*0.08
        self.velocidadIndicadorX = 2
        self.indicadorX = WIDTH/2
        self.indicadorY = HEIGHT*0.46
        self.indicadorColor = BLANCO
        self.indicadorActivado = False
        

    def dibujar(self,pantalla): 
        
        pygame.draw.rect(pantalla, ROJO, (WIDTH*0.1, HEIGHT*0.475, self.lineaGrandeX, self.lineaGrandeY))
        pygame.draw.rect(pantalla, VERDE, (WIDTH*0.45, HEIGHT*0.475, self.lineaPequeñaX, self.lineaPequeñaY))
        pygame.draw.rect(pantalla, self.indicadorColor, (self.indicadorX, self.indicadorY, self.indicadorWidth, self.indicadorHeight))
        
    def update(self, tiempo):

        

        # teclasPulsadas = pygame.key.get_pressed()
        # if teclasPulsadas[K_SPACE]:
        #     self.indicadorColor = VERDE
        # else:
        #     self.indicadorColor = BLANCO
        if self.indicadorActivado:
            if self.indicadorX >= (WIDTH*0.45 - self.indicadorWidth/2) and self.indicadorX <= (WIDTH*0.45 + self.lineaPequeñaX - self.indicadorWidth/2):
                self.indicadorColor = ROJO
            else:
                self.indicadorColor = VERDE
        else:
            self.indicadorColor = BLANCO
        if self.indicadorX <= WIDTH*0.1:
            self.velocidadIndicadorX = -self.velocidadIndicadorX

        if self.indicadorX >= (WIDTH*0.1 + self.lineaGrandeX - self.indicadorWidth):
            self.velocidadIndicadorX = -self.velocidadIndicadorX

        self.indicadorX += self.velocidadIndicadorX

    def eventos(self, activado):
        self.indicadorActivado = activado