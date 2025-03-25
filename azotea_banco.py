from Puzzles.laserPuzzle import LaserPuzzle
from personajes import *
from settings import *
from escena import *
from mapa import *
import math

# Clase auxiliar para manejar la aparición de la puerta final
class ObjetoParaCambiar:
    def __init__(self):
        self.objeto = None
        self.grupos = []
        self.visible = False

    def cambiar(self, grupos=None):
        if not self.visible and self.objeto:
            if grupos:
                for grupo in grupos:
                    grupo.add(self.objeto)
            elif self.grupos:
                for grupo in self.grupos:
                    grupo.add(self.objeto)
            self.visible = True

# Agregar al inicio del archivo
class PosicionamientoInteraccion(PosicionamientoInteraccion):
    def __init__(self, escena, posicion, textoMision="", radio_interaccion=80):
        super().__init__(escena, posicion, textoMision)
        self.radio_interaccion = radio_interaccion
    
    def puedeActivar(self, jugador):
        dx = jugador.rect.centerx - self.posicion[0]
        dy = jugador.rect.centery - self.posicion[1]
        distancia = math.sqrt(dx*dx + dy*dy)
        return distancia <= self.radio_interaccion

class TeclaInteraccion(TeclaInteraccion):
    def __init__(self, jugador, posicion_interaccion=None):
        super().__init__(jugador)
        self.posicion_interaccion = posicion_interaccion
        self.visible = False
        
    def dibujar(self, pantalla):
        if self.visible:
            if self.posicion_interaccion:
                # Usamos la posición del punto de interacción en lugar de la del jugador
                pantalla.blit(self.imagen, 
                        (self.posicion_interaccion[0] - self.imagen.get_width() / 2,
                         self.posicion_interaccion[1] - 60))  # Dibujar encima del punto de interacción
            else:
                # Comportamiento original con la posición del jugador
                pantalla.blit(self.imagen, 
                        (self.jugador.rect.centerx - self.imagen.get_width() / 2,
                         self.jugador.rect.top - 40))
    
    # Agregamos los métodos para mostrar y ocultar explícitamente
    def mostrar(self):
        self.visible = True
        
    def ocultar(self):
        self.visible = False

class AzoteaBanco(Mapa):
    def __init__(self, director):
        # Inicializamos la clase padre
        Mapa.__init__(self, director, "Mapas/azotea_banco48x48.tmx")

        # Inicializamos la cámara
        self.camera = pygame.Rect(0, 0, WIDTH, HEIGHT)

        # Inicializamos los grupos de sprites
        self.grupoSprites = pygame.sprite.Group()
        self.grupoSpritesDinamicos = pygame.sprite.Group()
        self.grupoObstaculos = pygame.sprite.Group()
        self.grupoCaminos = pygame.sprite.Group()  # Añadimos esta línea

        # Configuramos el puzzle y su posición de interacción
        self.puzzle = LaserPuzzle(director)
        # Actualizamos la posición para que coincida con el DoorPannel (ID 141)
        panel_pos = None
        for objectGroup in self.tmxdata.objectgroups:
            if objectGroup.name == "ObjetosAzoteas":
                for obj in objectGroup:
                    if hasattr(obj, 'id') and obj.id == 141:
                        panel_pos = (obj.x, obj.y)
                        break

        if panel_pos:
            self.posicionamientoInteraccion = PosicionamientoInteraccion(self.puzzle, panel_pos, "Hackea el sistema para desbloquear la puerta y acceder al banco")
        else:
            self.posicionamientoInteraccion = PosicionamientoInteraccion(self.puzzle, (216, 528), "Hackea el sistema para desbloquear la puerta y acceder al banco")
        
        # Creamos el jugador
        self.jugador1 = Jugador('Eddie.png', 'coordEddie.txt', [7, 10, 5])
        self.jugador1.establecerPosicion((2350, 550))
        self.grupoJugadores = pygame.sprite.Group(self.jugador1)
        self.grupoSpritesDinamicos.add(self.jugador1)

        # Configuramos la tecla de interacción usando la posición del panel
        self.teclaInteraccion = TeclaInteraccion(self.jugador1, self.posicionamientoInteraccion.posicion)

        # Centramos la cámara en el jugador
        self.center_target_camera(self.jugador1)

        # Objeto para la puerta que cambiará de estado
        self.puertaFinal = ObjetoParaCambiar()
        
        # Añadimos una referencia a la puerta inicial que queremos ocultar
        self.puertaInicial = None

        # Procesamos las capas del mapa TMX
        for objectGroup in self.tmxdata.objectgroups:
            if objectGroup.name == "Bordillos":
                for object in objectGroup:
                    # Determinamos si el bordillo está en la azotea pequeña (derecha)
                    if object.x > 2000:  # Ajusta este valor según la posición exacta
                        rect = pygame.Rect(object.x, object.y, object.width, object.height)
                    else:
                        rect = pygame.Rect(object.x, object.y, object.width, object.height)
                    
                    # Usar la imagen original
                    obj = Object(rect, object.image)
                    self.grupoObstaculos.add(obj)  # Para colisiones
                    self.grupoSprites.add(obj)     # Para dibujar
                    
                    # Solo para debug, crear una superficie adicional
                    if DEBUG_MODE:
                        surface = pygame.Surface((object.width, object.height))
                        surface.set_alpha(128)  # Semitransparente
                        surface.fill((255, 0, 0))  # Rojo
                        obstaculo = Obstacle(rect)
                        obstaculo.image = surface
                        self.grupoObstaculos.add(obstaculo)

                # Añadimos límites invisibles para la azotea pequeña
                limites_azoteas = [
                    # Límite derecho de la azotea pequeña
                    pygame.Rect(2450, 80, 25, 800),  # Zona derecha de la azotea pequeña
                    pygame.Rect(2255, 130, 25, 250), # Zona izquierda superior de la azotea pequeña
                    pygame.Rect(2255, 429, 25, 388), # Zona izquierda inferior de la azotea pequeña
                    pygame.Rect(1050, 335, 1220, 50),  # Zona supeior de la cuerda
                    pygame.Rect(1050, 430, 1220, 50),  # Zona inferior de la cuerda
                ]

                for limite in limites_azoteas:
                    surface = pygame.Surface((limite.width, limite.height))
                    surface.set_alpha(128)
                    surface.fill((0, 255, 0))  # Verde para distinguirlo en modo debug
                    
                    obstaculo = Obstacle(limite)
                    obstaculo.image = surface
                    self.grupoObstaculos.add(obstaculo)
            
            elif objectGroup.name == "ObjetosAzoteas":
                for object in objectGroup:
                    if object.name == "Inicial" or object.name == "Final":
                        rect = pygame.Rect(object.x, object.y, object.width, object.height)
                        if hasattr(object, 'image') and object.image:
                            if object.name == "Inicial":
                                # Creamos y mostramos la puerta inicial
                                puerta = Object(rect, object.image)
                                self.grupoSprites.add(puerta)
                                # Guardamos referencia a la puerta inicial
                                if hasattr(object, 'id') and object.id == 144:
                                    self.puertaInicial = puerta
                            elif object.name == "Final":
                                # Creamos la puerta final pero no la añadimos aún al grupo
                                puerta = Object(rect, object.image)
                                # La establecemos como objeto que cambiará
                                self.puertaFinal.objeto = puerta
                                # Establecemos los grupos donde se añadirá
                                self.puertaFinal.grupos = [self.grupoSprites]
                    else:
                        obj = Object(pygame.Rect(object.x, object.y, object.width, object.height), object.image)
                        self.grupoObstaculos.add(obj)
                        self.grupoSprites.add(obj)
            
            elif objectGroup.name == "Cuerdas":
                for object in objectGroup:
                    obj = Object(pygame.Rect(object.x, object.y, object.width, object.height), object.image)
                    self.grupoSprites.add(obj)
                    # Las cuerdas son caminos por los que sí se puede pasar
                    self.grupoCaminos.add(obj)
                    
    def center_target_camera(self, target):
        # Centramos la cámara en el objetivo (jugador)
        self.camera.x = target.rect.centerx - WIDTH // 2
        self.camera.y = target.rect.centery - HEIGHT // 2

        # Limitamos la cámara al tamaño del mapa
        self.camera.x = max(0, min(self.camera.x, self.tmxdata.width * self.tmxdata.tilewidth - WIDTH))
        self.camera.y = max(0, min(self.camera.y, self.tmxdata.height * self.tmxdata.tileheight - HEIGHT))

    def eventos(self, lista_eventos):
        for evento in lista_eventos:
            # Salir del juego
            if evento.type == pygame.QUIT or (evento.type == KEYDOWN and evento.key == K_ESCAPE):
                self.director.salirEscena()
    
            # Activar puzzle
            if evento.type == KEYDOWN and evento.key == K_e:
                if self.posicionamientoInteraccion.puedeActivar(self.jugador1):
                    self.director.apilarEscena(self.posicionamientoInteraccion.escena)
    
            # Mostrar/ocultar tecla de interacción
            if evento.type == KEYDOWN and evento.key == K_f:
                self.teclaInteraccion.mostrar()
            if evento.type == KEYDOWN and evento.key == K_r:
                self.teclaInteraccion.ocultar()
    
        # Movimiento del jugador
        teclasPulsadas = pygame.key.get_pressed()
        self.jugador1.mover(teclasPulsadas, K_UP, K_DOWN, K_LEFT, K_RIGHT)

    def update(self, tiempo):
        # Para cada sprite en el grupo, actualizamos manualmente
        for sprite in self.grupoSpritesDinamicos:
            if isinstance(sprite, Personaje):
                sprite.update(self.grupoObstaculos, tiempo)  
            else:
                sprite.update(tiempo)
        
        self.center_target_camera(self.jugador1)
        
        # Actualizamos la visibilidad de la tecla de interacción
        if self.posicionamientoInteraccion.puedeActivar(self.jugador1):
            self.teclaInteraccion.mostrar()
        else:
            self.teclaInteraccion.ocultar()
        
        # Comprobamos si el puzzle se ha completado
        if self.puzzle.completado and not self.puertaFinal.visible:
            # Primero eliminamos la puerta inicial si existe
            if self.puertaInicial:
                self.grupoSprites.remove(self.puertaInicial)
                self.puertaInicial = None  # Limpiamos la referencia
            
            # Ahora mostramos la puerta final
            self.puertaFinal.cambiar()

    def dibujar(self, pantalla):
        # Rellenamos el fondo
        pantalla.fill((0, 0, 0))
        
        # 1. Dibujamos las capas del TMX (fondo y bordillos)
        for layer in self.tmxdata.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, gid in layer:
                    tile = self.tmxdata.get_tile_image_by_gid(gid)
                    if tile:
                        pantalla.blit(tile, (x * self.tmxdata.tilewidth - self.camera.x, 
                                           y * self.tmxdata.tileheight - self.camera.y))

        # 2. Dibujamos los objetos (cuerdas, etc)
        for sprite in self.grupoSprites:
            if hasattr(sprite, 'image') and sprite.image:
                pantalla.blit(sprite.image, 
                            (sprite.rect.x - self.camera.x, 
                             sprite.rect.y - self.camera.y))

        # 3. En modo debug, dibujamos las zonas de colisión
        if DEBUG_MODE:
            for sprite in self.grupoObstaculos:
                if hasattr(sprite, 'image') and sprite.image:
                    pantalla.blit(sprite.image, 
                                (sprite.rect.x - self.camera.x, 
                                 sprite.rect.y - self.camera.y))

        # 4. Dibujamos los sprites dinámicos (jugador) al final para que aparezca siempre encima
        for sprite in self.grupoSpritesDinamicos:
            if hasattr(sprite, 'image') and sprite.image:
                pantalla.blit(sprite.image, 
                            (sprite.rect.x - self.camera.x, 
                             sprite.rect.y - self.camera.y))

        # 5. Dibujamos la tecla de interacción si es necesario
        if self.teclaInteraccion.visible:
            # Ajustamos la posición con respecto a la cámara
            pos_x = self.posicionamientoInteraccion.posicion[0] - self.camera.x
            pos_y = self.posicionamientoInteraccion.posicion[1] - self.camera.y - 60  # Ajustado para que aparezca encima del panel
            pantalla.blit(self.teclaInteraccion.image, 
                      (pos_x - self.teclaInteraccion.image.get_width() / 2, pos_y))