from Puzzles.laserPuzzle import LaserPuzzle
from personajes import *
from settings import *
from escena import *
from mapa import *

class AzoteaBanco(Mapa):
    def __init__(self, director):
        # Inicializamos la clase padre
        Mapa.__init__(self, director, "Mapas/azotea_banco48x48.tmx")

        # Inicializamos la cámara
        self.camera = pygame.Rect(0, 0, WIDTH, HEIGHT)

        # Inicializamos los grupos de sprites
        self.grupoSprites = pygame.sprite.Group()

        # Inicializamos los grupos de sprites
        self.grupoSprites = pygame.sprite.Group()
        self.grupoSpritesDinamicos = pygame.sprite.Group()
        self.grupoObstaculos = pygame.sprite.Group()
        self.grupoCaminos = pygame.sprite.Group()  # Añadimos esta línea

        # Configuramos el puzzle
        self.puzzle = LaserPuzzle(director)
        self.posicionamientoInteraccion = PosicionamientoInteraccion(self.puzzle, (216, 528))
        self.posicionamientoInteracciones = [self.posicionamientoInteraccion]
        self.posicionamientoPuzleActual = 0
        
        # Creamos el jugador
        self.jugador1 = Jugador('Eddie.png', 'coordEddie.txt', [7, 10])
        self.jugador1.establecerPosicion((2350, 550))  # Cambiamos la coordenada X de 408 a 600
        self.grupoJugadores = pygame.sprite.Group(self.jugador1)
        self.grupoSpritesDinamicos.add(self.jugador1)

        # Configuramos la tecla de interacción
        self.teclaInteraccion = TeclaInteraccion(self.jugador1)

        # Centramos la cámara en el jugador
        self.center_target_camera(self.jugador1)

        # Objeto para la puerta que cambiará de estado
        self.puertaFinal = ObjetoParaCambiar()

        # Procesamos las capas del mapa TMX
        for objectGroup in self.tmxdata.objectgroups:
            if objectGroup.name == "Bordillos":
                for object in objectGroup:
                    # Determinamos si el bordillo está en la azotea pequeña (derecha)
                    if object.x > 2000:  # Ajusta este valor según la posición exacta
                        rect = pygame.Rect(object.x, object.y, object.width, object.height)
                    else:
                        rect = pygame.Rect(object.x, object.y, object.width, object.height)
                    
                    # Usar la imagen original en lugar de una superficie de debug
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
                            elif object.name == "Final":
                                # Creamos la puerta final pero no la añadimos aún al grupo
                                puerta = Object(rect, object.image)
                                # La establecemos como objeto que cambiará
                                self.puertaFinal.objeto = puerta
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
                if self.posicionamientoInteracciones[self.posicionamientoPuzleActual].puedeActivar(self.jugador1):
                    self.director.apilarEscena(self.posicionamientoInteracciones[self.posicionamientoPuzleActual].escena)

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
                # El grupo de colisiones debe ir después del tiempo
                sprite.update(self.grupoObstaculos, tiempo)  
            else:
                sprite.update(tiempo)
        
        self.center_target_camera(self.jugador1)
        
        # Comprobamos si el puzzle se ha completado
        if self.puzzle.completado:
            self.puertaFinal.cambiar([self.grupoSprites])

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
        self.teclaInteraccion.dibujar(pantalla)