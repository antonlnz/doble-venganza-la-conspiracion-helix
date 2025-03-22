from Puzzles.cardPuzzle import CardPuzzle
from Puzzles.keypadPuzzle import KeypadPuzzle
from Puzzles.sortingGridPuzzle import SortingGridPuzzle
from Puzzles.switch_puzzle import SwitchPuzzle
from Puzzles.tarjetaPuzzle import Tarjeta
from Puzzles.wire_puzzle import WirePuzzle
from Puzzles.tuberiasPuzzle import Pipe
from personajes import *
from settings import *
from escena import *
from mapa import *


class PisoCajaFuerte(Mapa):
    def __init__(self, director, anteriorMapa):

        Mapa.__init__(self, director, "Mapas/pisoCajaFuerte48x48.tmx")

    
        self.anteriorMapa = anteriorMapa

        # self.posicionamientoInteraccionHuida = PosicionamientoInteraccion(self.siguienteMapa, (720, 144))
        
        self.subirPiso = PosicionamientoInteraccion(self.anteriorMapa, (1272, 720))
        # self.bajarPiso = PosicionamientoInteraccion(self.siguienteMapa, (720, 144))

        self.posicionamientoPuzleActual = 0

        self.personajeMovido = False

        self.huida = False

        # self.tmxdata = pytmx.load_pygame("Mapas/ayuntamiento48x48v2.tmx")

        self.reliquia = ObjetoParaCambiar()
        self.interaccionRoboReliquia = PosicionamientoInteraccionRobo(self.reliquia, (312, 192))

        self.grupoCajasFuerte1 = GrupoObjetosParaCambiar()
        self.interaccionRobo1 = PosicionamientoInteraccionRobo(self.grupoCajasFuerte1, (120, 432))

        self.grupoCajasFuerte2 = GrupoObjetosParaCambiar()
        self.interaccionRobo2 = PosicionamientoInteraccionRobo(self.grupoCajasFuerte2, (504, 432))

        self.grupoCajasFuerte3 = GrupoObjetosParaCambiar()
        self.interaccionRobo3 = PosicionamientoInteraccionRobo(self.grupoCajasFuerte3, (112, 144))

        self.grupoCajasFuerte4 = GrupoObjetosParaCambiar()
        self.interaccionRobo4 = PosicionamientoInteraccionRobo(self.grupoCajasFuerte4, (512, 144))

        self.jugador1 = Jugador('Eddie.png','coordEddie.txt', [7, 10, 5])
        self.grupoJugadores = pygame.sprite.Group(self.jugador1)

        self.grupoSpritesDinamicos.add(self.jugador1)

        self.jugador1.establecerPosicion((1272, 744))

        self.teclaInteraccion = TeclaInteraccion(self.jugador1)

        self.center_target_camera(self.jugador1)

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
            elif objectGroup.name == "Reliquia":
                 for object in objectGroup:
                    self.reliquia.establecerObjeto(object, [self.grupoObstaculos, self.grupoSprites])
            elif objectGroup.name == "GrupoCajasFuerte1":
                 for object in objectGroup:
                    self.grupoCajasFuerte1.establecerObjeto(object, [self.grupoSprites])
            elif objectGroup.name == "GrupoCajasFuerte2":
                 for object in objectGroup:
                    self.grupoCajasFuerte2.establecerObjeto(object, [self.grupoSprites])
            elif objectGroup.name == "GrupoCajasFuerte3":
                 for object in objectGroup:
                    self.grupoCajasFuerte3.establecerObjeto(object, [self.grupoSprites])
            elif objectGroup.name == "GrupoCajasFuerte4":
                 for object in objectGroup:
                    self.grupoCajasFuerte4.establecerObjeto(object, [self.grupoSprites])
            else:
                for object in objectGroup: 
                    obj = Object(pygame.Rect(object.x, object.y, object.width, object.height), object.image)
                    self.grupoObstaculos.add(obj)
                    # self.grupoObjetos.add(obj)
                    self.grupoSprites.add(obj)
           
        self.grupoSprites.add(self.jugador1)
        

    def dibujar(self,pantalla):
        pantalla.fill((0,0,0))
        self.grupoSprites.draw(pantalla)
        self.grupoJugadores.draw(pantalla)
        self.grupoDespuesPersonaje.draw(pantalla)
        self.teclaInteraccion.dibujar(pantalla)
        

    def eventos(self, lista_eventos):
        for evento in lista_eventos:
            # Si se sale del programa
            if evento.type == pygame.QUIT or (evento.type == KEYDOWN and evento.key == K_ESCAPE):
                self.director.salirEscena()

            if evento.type == KEYDOWN and evento.key == K_e:
                if self.subirPiso.puedeActivar(self.jugador1):
                    self.director.salirEscena()

                if self.cajasFuerteRobadas() and self.interaccionRoboReliquia.puedeActivar(self.jugador1):
                    self.reliquia.cambiar([self.grupoSprites])

                if self.interaccionRobo1.puedeActivar(self.jugador1):
                    self.grupoCajasFuerte1.cambiar([self.grupoSprites])

                if self.interaccionRobo2.puedeActivar(self.jugador1):
                    self.grupoCajasFuerte2.cambiar([self.grupoSprites])

                if self.interaccionRobo3.puedeActivar(self.jugador1):
                    self.grupoCajasFuerte3.cambiar([self.grupoSprites])

                if self.interaccionRobo4.puedeActivar(self.jugador1):
                    self.grupoCajasFuerte4.cambiar([self.grupoSprites])

            if evento.type == KEYDOWN and evento.key == K_q:
                self.reliquia.cambiar([self.grupoSprites])
                

            if evento.type == KEYDOWN and evento.key == K_f:
                self.grupoCajasFuerte1.cambiar([self.grupoSprites])

            if evento.type == KEYDOWN and evento.key == K_g:
                self.grupoCajasFuerte2.cambiar([self.grupoSprites])

            if evento.type == KEYDOWN and evento.key == K_r:
                self.grupoCajasFuerte3.cambiar([self.grupoSprites])

            if evento.type == KEYDOWN and evento.key == K_t:
                self.grupoCajasFuerte4.cambiar([self.grupoSprites])
            
        teclasPulsadas = pygame.key.get_pressed()
        self.jugador1.mover(teclasPulsadas, K_UP, K_DOWN, K_LEFT, K_RIGHT)
    
    def update(self, tiempo):
        
        if self.reliquia.objetoCambiado:
            self.huida = True

        self.altenarTeclaInteraccion()

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

        self.interaccionRoboReliquia.update(self.offset)
        self.interaccionRobo1.update(self.offset)
        self.interaccionRobo2.update(self.offset)
        self.interaccionRobo3.update(self.offset)
        self.interaccionRobo4.update(self.offset)
        self.subirPiso.update(self.offset)  

    def altenarTeclaInteraccion(self):
        if self.subirPiso.puedeActivar(self.jugador1) or self.puedeRobar(self.jugador1) or (self.cajasFuerteRobadas() and self.interaccionRoboReliquia.puedeActivar(self.jugador1)):
            self.teclaInteraccion.mostrar()
        else:
            self.teclaInteraccion.ocultar()

    def cajasFuerteRobadas(self):
        return self.grupoCajasFuerte1.objetoCambiado and self.grupoCajasFuerte2.objetoCambiado and self.grupoCajasFuerte3.objetoCambiado and self.grupoCajasFuerte4.objetoCambiado
    
    def puedeRobar(self, target):
        return self.interaccionRobo1.puedeActivar(target) or  self.interaccionRobo2.puedeActivar(target) or self.interaccionRobo3.puedeActivar(target) or self.interaccionRobo4.puedeActivar(target) 