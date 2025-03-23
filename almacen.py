from Puzzles.cable_puzzle import CablePuzzle
from Puzzles.cardPuzzle import CardPuzzle
from Puzzles.keypadPuzzle import KeypadPuzzle
from Puzzles.printPuzzle import Huella
from Puzzles.sortingGridPuzzle import SortingGridPuzzle
from Puzzles.switch_puzzle import SwitchPuzzle
from Puzzles.tarjetaPuzzle import Tarjeta
from Puzzles.wire_puzzle import WirePuzzle
from Puzzles.tuberiasPuzzle import Pipe
from periodico_almacen import Periodico_Almacen
from personajes import *
from pisoMedioBanco import PisoMedioBanco
from settings import *
from escena import *
from mapa import *


class Almacen(Mapa):
    def __init__(self, director):

        Mapa.__init__(self, director, "Mapas/almacen48x48.tmx")

        self.inicializarTextosMisiones()

        self.puzle = SortingGridPuzzle(director)
        self.puzle2 = SwitchPuzzle(director)
        self.puzle3 = Pipe(director)
        self.puzle4 = Huella(director) 
        self.puzle5 = CablePuzzle(director)
        self.siguienteMapa = Periodico_Almacen(director)

        self.posicionamientoInteraccion = PosicionamientoInteraccion(self.puzle, (216, 1200), self.textoMision)
        self.posicionamientoInteraccion2 = PosicionamientoInteraccion(self.puzle2, (1368, 144), self.textoMision2)
        self.posicionamientoInteraccion3 = PosicionamientoInteraccion(self.puzle3, (216, 528), self.textoMision3)
        self.posicionamientoInteraccion4 = PosicionamientoInteraccion(self.puzle4, (1056, 576), self.textoMision4)
        self.posicionamientoInteraccion5 = PosicionamientoInteraccion(self.puzle5, (1392, 1032), self.textoMision5)
        self.posicionamientoInteraccionHuida = PosicionamientoInteraccion(self.siguienteMapa, (720, 144), self.textoMisionHuida)

        self.posicionamientoInteracciones = [self.posicionamientoInteraccion, self.posicionamientoInteraccion2, 
                                                self.posicionamientoInteraccion3, self.posicionamientoInteraccion4, 
                                                self.posicionamientoInteraccion5, self.posicionamientoInteraccionHuida]

        self.posicionamientoInteraccionActual = 0

        self.personajeMovido = False

        self.huida = False

        # self.tmxdata = pytmx.load_pygame("Mapas/ayuntamiento48x48v2.tmx")

        self.puertaAlmacen = ObjetoParaCambiar()
        self.puertaSala = ObjetoParaCambiar()
        self.camara = ObjetoParaCambiar()
        self.cajaFuerte = ObjetoParaCambiar()

        self.jugador1 = Jugador('Eddie.png','coordEddie.txt', [7, 10, 5])
        self.grupoJugadores = pygame.sprite.Group(self.jugador1)

        self.grupoSpritesDinamicos.add(self.jugador1)

        self.jugador1.establecerPosicion((408, 1368))

        self.teclaInteraccion = TeclaInteraccion(self.jugador1)

        self.center_target_camera(self.jugador1)

        self.guardia = GuardiaBanco()
        self.guardia.establecerPosicion((1056, 576))
        self.grupoSpritesDinamicos.add(self.guardia)

        for objectGroup in self.tmxdata.objectgroups:
            if objectGroup.name == "Obstaculos":
                for object in objectGroup:
                    self.grupoObstaculos.add(Obstacle(pygame.Rect(object.x, object.y, object.width, object.height)))

            elif objectGroup.name == "ObjetosSinColision" or objectGroup.name == "Estanterias" or objectGroup.name == "EstanteriasArriba":
                for object in objectGroup: 
                    obj = Object(pygame.Rect(object.x, object.y, object.width, object.height), object.image)
                    # self.grupoObjetos.add(obj)
                    # self.grupoDespuesPersonaje.add(obj)
                    self.grupoSprites.add(obj)
            elif objectGroup.name == "PuertaAlmacen":
                 for object in objectGroup:
                    self.puertaAlmacen.establecerObjeto(object, [self.grupoObstaculos, self.grupoSprites])
            elif objectGroup.name == "PuertaSala":
                 for object in objectGroup:
                    self.puertaSala.establecerObjeto(object, [self.grupoObstaculos, self.grupoSprites])
            elif objectGroup.name == "Camara":
                 for object in objectGroup:
                    self.camara.establecerObjeto(object, [self.grupoSprites])
            elif objectGroup.name == "CajaFuerte":
                 for object in objectGroup:
                    self.cajaFuerte.establecerObjeto(object, [self.grupoSprites])
            else:
                for object in objectGroup: 
                    obj = Object(pygame.Rect(object.x, object.y, object.width, object.height), object.image)
                    self.grupoObstaculos.add(obj)
                    # self.grupoObjetos.add(obj)
                    self.grupoSprites.add(obj)

        self.grupoObstaculos.add(self.guardia)
        self.grupoSprites.add(self.guardia)
        self.grupoSprites.add(self.jugador1)

    def inicializarTextosMisiones(self):
        self.textoMision = "Abre la puerta para acceder al almacen"
        self.textoMision2 = "Encuentra la caja de fusibles\n para desactivar la camara"
        self.textoMision3 = "Abre la puerta de la sala en\n donde se encuentra la caja fuerte"
        self.textoMision4 = "Noquea al guardia y llevalo hasta\n la caja fuerta para abrirla con su huella"
        self.textoMision5 = "Coloca una de las bombas conseguidas\n en la esquina inferior derecha del almacen\n para crear una distraccion al huir"
        self.textoMisionHuida = "Huye por el conducto de ventilacion"
        

    def dibujar(self,pantalla):
        pantalla.fill((0,0,0))
        self.grupoSprites.draw(pantalla)
        self.grupoJugadores.draw(pantalla)
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
                        if self.posicionamientoInteraccionActual == 3 and not self.guardia.noqueado:
                            self.guardia.noquear()
                            self.grupoObstaculos.remove(self.guardia)
                        else:
                            self.director.apilarEscena(self.posicionamientoInteracciones[self.posicionamientoInteraccionActual].escena)

            if evento.type == KEYDOWN and evento.key == K_q:
                self.puertaAlmacen.cambiar([self.grupoDespuesPersonaje, self.grupoSprites])
                self.puertaSala.cambiar([self.grupoDespuesPersonaje, self.grupoSprites])
                

            if evento.type == KEYDOWN and evento.key == K_f:
                self.teclaInteraccion.mostrar()
                self.camara.cambiar([self.grupoDespuesPersonaje, self.grupoSprites])
                self.cajaFuerte.cambiar([self.grupoDespuesPersonaje, self.grupoSprites])

            if evento.type == KEYDOWN and evento.key == K_r:
                self.teclaInteraccion.ocultar()
            
        teclasPulsadas = pygame.key.get_pressed()
        self.jugador1.mover(teclasPulsadas, K_UP, K_DOWN, K_LEFT, K_RIGHT)
    
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

        if self.puzle.completado and not self.puertaAlmacen.objetoCambiado:
            self.puertaAlmacen.cambiar([self.grupoDespuesPersonaje, self.grupoSprites])

        if self.puzle2.completado and not self.camara.objetoCambiado:
            self.camara.cambiar([self.grupoDespuesPersonaje, self.grupoSprites])

        if self.puzle3.completado and not self.puertaSala.objetoCambiado:
            self.puertaSala.cambiar([self.grupoDespuesPersonaje, self.grupoSprites])
        
        if self.puzle4.completado and not self.cajaFuerte.objetoCambiado:
            self.cajaFuerte.cambiar([self.grupoSprites])
            self.jugador1.establecerPosicion((120, 168))
            self.guardia.establecerPosicion((60, 168))

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

        self.posicionamientoInteracciones[self.posicionamientoInteraccionActual].update(self.offset)