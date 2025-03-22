import os
import pygame
import sys
from almacen import Almacen
from escena import *

WIDTH = 1920
HEIGHT = 1080
RESOLUCION = (WIDTH, HEIGHT)
ALTURA_DESEADA = 900

class Periodico_Ayuntamiento(Escena):
    def __init__(self, director):
        Escena.__init__(self, director)
        self.titulo = "Noticias de la Fábrica"
        os.environ['SDL_VIDEO_CENTERED'] = '1'
        self.contenido = []
        self.fondo = pygame.Surface(RESOLUCION)
        self.fondo.fill((0, 0, 0))
        original = pygame.image.load('imagenes/Periodico/Periodico_ayuntamiento.png').convert_alpha()
        ratio = ALTURA_DESEADA / original.get_height()
        nuevo_ancho = int(original.get_width() * ratio)
        self.imagen_periodico = pygame.transform.smoothscale(original, (nuevo_ancho, ALTURA_DESEADA))
        self.alpha = 255
        self.fadeout = False
        self.fade_speed = 5
        self.overlay = pygame.Surface(RESOLUCION)
        self.overlay.fill((0, 0, 0))
        self.tiempo_transcurrido = 0
        self.mostrar_mensaje = False
        self.fuente = pygame.font.Font(None, 36)
        self.texto = self.fuente.render("Toca cualquier tecla para continuar", True, (0, 0, 0))
        self.texto_rect = self.texto.get_rect()
        self.texto_rect.centerx = WIDTH // 2
        self.texto_rect.bottom = HEIGHT - 120
        self.tiempo_parpadeo = 0
        self.texto_visible = True
        self.velocidad_parpadeo = 300

        self.siguienteMapa = Almacen(director)
    
    def eventos(self, eventos):
        for evento in eventos:
            if evento.type == pygame.QUIT:
                self.director.salirEscena()
            if evento.type == pygame.KEYDOWN:
                self.fadeout = True
    
    def update(self, tiempo):
        if not self.fadeout:
            self.alpha = max(0, self.alpha - self.fade_speed)
            if self.alpha == 0:
                self.tiempo_transcurrido += tiempo
                if self.tiempo_transcurrido >= 2000:
                    self.mostrar_mensaje = True
            if self.mostrar_mensaje:
                self.tiempo_parpadeo += tiempo
                if self.tiempo_parpadeo >= self.velocidad_parpadeo:
                    self.texto_visible = not self.texto_visible
                    self.tiempo_parpadeo = 0
        else:
            self.alpha = min(255, self.alpha + self.fade_speed)
            if self.alpha >= 255:
                self.director.cambiarEscena(self.siguienteMapa)
    
    def dibujar(self, pantalla):
        pantalla.blit(self.fondo, (0, 0))
        x = (WIDTH - self.imagen_periodico.get_width()) // 2
        y = (HEIGHT - self.imagen_periodico.get_height()) // 2
        pantalla.blit(self.imagen_periodico, (x, y))
        self.overlay.set_alpha(self.alpha)
        pantalla.blit(self.overlay, (0, 0))
        if self.mostrar_mensaje and self.texto_visible:
            pantalla.blit(self.texto, self.texto_rect)

