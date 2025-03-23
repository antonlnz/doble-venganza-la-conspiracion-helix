import pygame
import pytmx

from Puzzles.SimonDicePuzzle import SimonDice
from Puzzles.cardPuzzle import CardPuzzle
from Puzzles.concentric_circles_puzzle import ConcentricCirclesPuzzle
from Puzzles.door_lock_puzzle import DoorLockPuzzle
from Puzzles.guardiasPuzzle import Guardia
from Puzzles.hackPuzzle_little import Hack
from Puzzles.tarjetaPuzzle import Tarjeta
from Puzzles.keypadPuzzle import KeypadPuzzle
# from almacen import Almacen
from periodico import Periodico_Banco
from personajes import *
from pisoCajaFuerte import PisoCajaFuerte
from settings import *
from escena import *
from mapa import *


class PisoMedioBanco(Mapa):
    def __init__(self, director):

        Mapa.__init__(self, director, "Mapas/pisoMedioBanco48x48.tmx")

        self.inicializarTextosMisiones()

        self.puzle = ConcentricCirclesPuzzle(director)
        self.puzle2 = DoorLockPuzzle(director)
        self.puzle3 = SimonDice(director)
        self.puzle4 = Guardia(director)
        self.siguienteMapa = PisoCajaFuerte(director, self)
        # self.siguienteMapa = Periodico_Banco(director)

        self.posicionamientoInteraccion = PosicionamientoInteraccion(self.puzle, (864, 432), self.textoMision)
        self.posicionamientoInteraccion2 = PosicionamientoInteraccion(self.puzle2, (1368, 576), self.textoMision2)
        self.posicionamientoInteraccion3 = PosicionamientoInteraccion(self.puzle3, (1368, 240), self.textoMision3)
        self.posicionamientoInteraccion4 = PosicionamientoInteraccion(self.puzle4, (864, 840), self.textoMision4)
        self.posicionamientoInteraccionHuida = PosicionamientoInteraccion(self.puzle3, (960, 528), self.textoMisionHuida)
        
        self.posicionamientoInteracciones = [self.posicionamientoInteraccion, self.posicionamientoInteraccion2, self.posicionamientoInteraccion3, self.posicionamientoInteraccion4, self.posicionamientoInteraccionHuida]

        self.posicionamientoInteraccionActual = 0

        self.bajarPiso = PosicionamientoInteraccion(self.siguienteMapa, (1512, 1368), self.textoMisionSiguienteMapa)

        self.huida = False

        self.llego = False

        # self.tmxdata = pytmx.load_pygame("Mapas/ayuntamiento48x48v2.tmx")

        self.puertaAcceso = ObjetoParaCambiar()
        self.puertaSalaSeguridad = ObjetoParaCambiar()

        self.jugador1 = Jugador('Vince.png','coordVince.txt', [7, 10, 5])
        self.grupoJugadores = pygame.sprite.Group(self.jugador1)

        self.grupoSpritesDinamicos.add(self.jugador1)

        # self.jugador1.establecerPosicion((WIDTH//2, HEIGHT//2))
        self.jugador1.establecerPosicion((380, 240))

        self.jugador2 = Jugador('Eddie.png','coordEddie.txt', [7, 10, 5])
        self.grupoJugadores = pygame.sprite.Group(self.jugador2)

        self.grupoSpritesDinamicos.add(self.jugador2)

        self.jugador2.establecerPosicion((864, 336))

        self.jugadorActual = self.jugador1

        self.teclaInteraccion = TeclaInteraccion(self.jugadorActual)

        self.center_target_camera(self.jugadorActual)

        self.guardia1 = GuardiaBanco()
        self.guardia1.establecerPosicion((790, 912))
        self.grupoSpritesDinamicos.add(self.guardia1)

        self.guardia2 = GuardiaBanco()
        self.guardia2.establecerPosicion((864, 912))
        self.grupoSpritesDinamicos.add(self.guardia2)

        self.guardia3 = GuardiaBanco()
        self.guardia3.establecerPosicion((938, 912))
        self.grupoSpritesDinamicos.add(self.guardia3)
        

        for objectGroup in self.tmxdata.objectgroups:
            if objectGroup.name == "Obstaculos":
                for object in objectGroup:
                    self.grupoObstaculos.add(Obstacle(pygame.Rect(object.x, object.y, object.width, object.height)))

            elif objectGroup.name == "ObjetosSinColision":
                for object in objectGroup: 
                    obj = Object(pygame.Rect(object.x, object.y, object.width, object.height), object.image)
                    # self.grupoObjetos.add(obj)
                    # self.grupoDespuesPersonaje.add(obj)
                    self.grupoSprites.add(obj)
            elif objectGroup.name == "PuertaAcceso":
                 for object in objectGroup:
                    self.puertaAcceso.establecerObjeto(object, [self.grupoObstaculos, self.grupoSprites])

            elif objectGroup.name == "PuertaSalaSeguridad":
                 for object in objectGroup:
                    self.puertaSalaSeguridad.establecerObjeto(object, [self.grupoObstaculos, self.grupoSprites])

            else:
                for object in objectGroup: 
                    obj = Object(pygame.Rect(object.x, object.y, object.width, object.height), object.image)
                    self.grupoObstaculos.add(obj)
                    # self.grupoObjetos.add(obj)
                    self.grupoSprites.add(obj)

        self.grupoSprites.add(self.jugador1)
        self.grupoSprites.add(self.jugador2)

    def inicializarTextosMisiones(self):
        self.textoMision = "Abre la puerta para poder avanzar"
        self.textoMision2 = "Abre la puerta de la sala de seguridad\n para acceder a la misma"
        self.textoMision3 = "Desarma los sistemas de seguridad desde\n el ordenador que se encuentra en la sala de seguridad"
        self.textoMision4 = "Defiende a Vince de los guardias mientras termina de desarmar la seguridad"
        self.textoMisionSiguienteMapa = "Baja hasta el piso de la caja fuerte"
        self.textoMisionHuida = "Huye hasta la azotea donde te espera Vince"
        
    def cambiarJugador(self, jugador):
        self.jugadorActual = jugador

    def dibujar(self,pantalla):
        pantalla.fill((0,0,0))
        self.grupoSprites.draw(pantalla)
        self.grupoDespuesPersonaje.draw(pantalla)
        self.teclaInteraccion.dibujar(pantalla)
        self.mision.dibujar(pantalla)
        

    def eventos(self, lista_eventos):
        for evento in lista_eventos:
            # Si se sale del programa
            if evento.type == pygame.QUIT or (evento.type == KEYDOWN and evento.key == K_ESCAPE):
                self.director.salirEscena()

            if evento.type == KEYDOWN and evento.key == K_e:
                if self.posicionamientoInteracciones[self.posicionamientoInteraccionActual].puedeActivar(self.jugadorActual):
                    if self.huida:
                        self.director.cambiarEscena(self.posicionamientoInteracciones[self.posicionamientoInteraccionActual].escena)
                    else:
                        self.director.apilarEscena(self.posicionamientoInteracciones[self.posicionamientoInteraccionActual].escena)

                if self.bajarPiso.puedeActivar(self.jugador2):
                        self.director.apilarEscena(self.bajarPiso.escena)

            if evento.type == KEYDOWN and evento.key == K_q:
                self.cambiarJugador(self.jugador2)

            if evento.type == KEYDOWN and evento.key == K_f:
                self.cambiarJugador(self.jugador1)

            if evento.type == KEYDOWN and evento.key == K_r:
                self.jugador1.noquear()

            if evento.type == KEYDOWN and evento.key == K_t:
                self.puertaAcceso.cambiar([self.grupoDespuesPersonaje, self.grupoSprites])
            
            if evento.type == KEYDOWN and evento.key == K_z:
                self.mostrarGuardias()
            
            if evento.type == KEYDOWN and evento.key == K_x:
                self.noquearGuardias()
            
        teclasPulsadas = pygame.key.get_pressed()
        self.jugadorActual.mover(teclasPulsadas, K_UP, K_DOWN, K_LEFT, K_RIGHT)
    
    def update(self, tiempo):
        
        if not self.huida:
            if self.posicionamientoInteracciones[self.posicionamientoInteraccionActual].escena.completado:
                self.posicionamientoInteraccionActual += 1

                if self.posicionamientoInteraccionActual == (len(self.posicionamientoInteracciones) - 1):
                    self.huida = True
            
        if self.posicionamientoInteracciones[self.posicionamientoInteraccionActual].puedeActivar(self.jugadorActual) or (self.bajarPiso.puedeActivar(self.jugador2) and not self.siguienteMapa.huida):
            self.teclaInteraccion.mostrar()
        else:
            self.teclaInteraccion.ocultar()

        self.mision.establecerTexto(self.posicionamientoInteracciones[self.posicionamientoInteraccionActual].textoMision)

        if self.puzle.completado: 
            if not self.puertaAcceso.objetoCambiado:
                self.puertaAcceso.cambiar([self.grupoDespuesPersonaje, self.grupoSprites])
            if not self.llego:
                self.llego = self.jugador2.moverEnYHasta(720, 20)

        if self.puzle2.completado and not self.puertaSalaSeguridad.objetoCambiado:
            self.puertaSalaSeguridad.cambiar([self.grupoDespuesPersonaje, self.grupoSprites])

        if self.puzle3.completado:
            self.cambiarJugador(self.jugador2)
            self.mostrarGuardias()

        if self.puzle4.completado:
            self.noquearGuardias()

        self.center_target_camera(self.jugadorActual)
        self.grupoSpritesDinamicos.update(self.grupoObstaculos, tiempo)

        for sprite in iter(self.grupoObstaculos):
                sprite.establecerPosicionPantalla(self.offset)

        # for sprite in iter(self.grupoObjetos):
        #         sprite.establecerPosicionPantalla(self.offset)

        # for sprite in iter(self.grupoTiles):
        #         sprite.establecerPosicionPantalla(self.offset)

        for sprite in iter(self.grupoSprites):
                sprite.establecerPosicionPantalla(self.offset)

        self.posicionamientoInteracciones[self.posicionamientoInteraccionActual].update(self.offset)   
        self.bajarPiso.update(self.offset)  


    def mostrarGuardias(self):
        self.grupoObstaculos.add(self.guardia1) 
        self.grupoSprites.add(self.guardia1) 

        self.grupoObstaculos.add(self.guardia2) 
        self.grupoSprites.add(self.guardia2) 

        self.grupoObstaculos.add(self.guardia3) 
        self.grupoSprites.add(self.guardia3)   

    def noquearGuardias(self):
        self.guardia1.noquear()
        self.grupoObstaculos.remove(self.guardia1)

        self.guardia2.establecerPosicion((864, 930))
        self.guardia2.noquear()
        self.grupoObstaculos.remove(self.guardia2)

        self.guardia3.noquear()
        self.grupoObstaculos.remove(self.guardia3)