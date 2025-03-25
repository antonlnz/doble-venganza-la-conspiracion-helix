import pygame
import pytmx

from Puzzles.cardPuzzle import CardPuzzle
from Puzzles.hackPuzzle import Hack
from Puzzles.tarjetaPuzzle import Tarjeta
from Puzzles.keypadPuzzle import KeypadPuzzle
from periodico_ayuntamiento import Periodico_Ayuntamiento
from personajes import *
from settings import *
from escena import *
from mapa import *


class Ayuntamiento(Mapa):
    def __init__(self, director):

        Mapa.__init__(self, director, "Mapas/ayuntamiento48x48v2.tmx")

        self.inicializarTextosMisiones()

        self.puzle = Tarjeta(director)
        self.puzle2 = KeypadPuzzle(director)
        self.puzle3 = Hack(director)
        self.siguienteMapa = Periodico_Ayuntamiento(director)

        self.posicionamientoInteraccion = PosicionamientoInteraccion(self.puzle, (950, 625), self.textoMision)
        self.posicionamientoInteraccion2 = PosicionamientoInteraccion(self.puzle2, (288, 672), self.textoMision2)
        self.posicionamientoInteraccion3 = PosicionamientoInteraccion(self.puzle3, (192, 240), self.textoMision3)
        self.posicionamientoInteraccionHuida = PosicionamientoInteraccion(self.siguienteMapa, (960, 528), self.textoMisionHuida)

        self.posicionamientoInteracciones = [self.posicionamientoInteraccion, self.posicionamientoInteraccion2, self.posicionamientoInteraccion3, self.posicionamientoInteraccionHuida]

        self.posicionamientoInteraccionActual = 0

        self.huida = False

        # self.tmxdata = pytmx.load_pygame("Mapas/ayuntamiento48x48v2.tmx")

        self.puertaAlcalde = ObjetoParaCambiar()

        self.jugador1 = Jugador('Vince.png','coordVince.txt', [7, 10, 5])
        self.grupoJugadores = pygame.sprite.Group(self.jugador1)
        self.npc = NPC_Ayuntamiento("Guardia.png", "coordGuardia.txt", [7, 7, 4], 750, 950)
        self.grupoSprites.add(self.npc)
        self.grupoSpritesDinamicos.add(self.npc) #Modificar la logica de los grupos para poder añadir el npc solo al grupo dinamico y
                                                    #que no se mueva con el personaje. 
        self.grupoSpritesDinamicos.add(self.jugador1)

        # self.jugador1.establecerPosicion((WIDTH//2, HEIGHT//2))
        self.jugador1.establecerPosicion((2184, 1320))

        self.teclaInteraccion = TeclaInteraccion(self.jugador1)

        self.center_target_camera(self.jugador1)
        

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
            elif objectGroup.name == "PuertaAlcalde":
                 for object in objectGroup:
                    self.puertaAlcalde.establecerObjeto(object, [self.grupoObstaculos, self.grupoSprites])

            else:
                for object in objectGroup: 
                    obj = Object(pygame.Rect(object.x, object.y, object.width, object.height), object.image)
                    self.grupoObstaculos.add(obj)
                    # self.grupoObjetos.add(obj)
                    self.grupoSprites.add(obj)
           
        self.grupoSprites.add(self.jugador1)
        
    def inicializarTextosMisiones(self):
        self.textoMision = "Roba la tarjeta de acceso al guardia"
        self.textoMision2 = "Usa el código de la tarjeta (789456123) para\n entrar en la oficina del alcalde"
        self.textoMision3 = "Descifra los planos que se encuentrar en la mesa del alcalde"
        self.textoMisionHuida = "Huye por la ventana de la sala contigua"

    def dibujar(self,pantalla):
        pantalla.fill((0,0,0))
        self.grupoSprites.draw(pantalla)
        self.grupoSpritesDinamicos.draw(pantalla)
        self.grupoDespuesPersonaje.draw(pantalla)
        self.teclaInteraccion.dibujar(pantalla)
        self.mision.dibujar(pantalla)
        

    def eventos(self, lista_eventos):
        for evento in lista_eventos:
            # Si se sale del programa
            if evento.type == pygame.QUIT or (evento.type == KEYDOWN and evento.key == K_ESCAPE):
                self.director.salirEscena()

            if evento.type == KEYDOWN and evento.key == K_e:
                if self.posicionamientoInteracciones[self.posicionamientoInteraccionActual].puedeActivar(self.jugador1):
                    if self.huida:
                        self.director.cambiarEscena(self.posicionamientoInteracciones[self.posicionamientoInteraccionActual].escena)
                    else:
                        self.director.apilarEscena(self.posicionamientoInteracciones[self.posicionamientoInteraccionActual].escena)
            
        teclasPulsadas = pygame.key.get_pressed()
        self.jugador1.mover(teclasPulsadas, K_w, K_s, K_a, K_d)
    
    def update(self, tiempo):

        
        
        if not self.huida:
            if self.posicionamientoInteracciones[self.posicionamientoInteraccionActual].escena.completado:
                self.posicionamientoInteraccionActual += 1

                if self.posicionamientoInteraccionActual == (len(self.posicionamientoInteracciones) - 1):
                    self.huida = True
            
        if self.posicionamientoInteracciones[self.posicionamientoInteraccionActual].puedeActivar(self.jugador1) :
            self.teclaInteraccion.mostrar()
        else:
            self.teclaInteraccion.ocultar()

        self.mision.establecerTexto(self.posicionamientoInteracciones[self.posicionamientoInteraccionActual].textoMision)

        if self.puzle2.completado and not self.puertaAlcalde.objetoCambiado:
            self.puertaAlcalde.cambiar([self.grupoDespuesPersonaje, self.grupoSprites])

            for grupo in self.npc.groups():
                grupo.remove(self.npc)

        self.center_target_camera(self.jugador1)
        self.grupoSpritesDinamicos.update(self.grupoObstaculos, tiempo)

        for sprite in iter(self.grupoObstaculos):
                sprite.establecerPosicionPantalla(self.offset)

        # for sprite in iter(self.grupoObjetos):
        #         sprite.establecerPosicionPantalla(self.offset)

        # for sprite in iter(self.grupoTiles):
        #         sprite.establecerPosicionPantalla(self.offset)

        for sprite in iter(self.grupoSprites):
                sprite.establecerPosicionPantalla(self.offset)

        self.posicionamientoInteraccion.establecerPosicion(self.npc.posicion)
        self.posicionamientoInteracciones[self.posicionamientoInteraccionActual].update(self.offset)   