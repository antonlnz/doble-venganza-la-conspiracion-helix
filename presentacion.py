import pygame
from ayuntamiento import Ayuntamiento
from escena import Escena
from settings import *

class Presentacion(Escena):
    def __init__(self, director):
        Escena.__init__(self, director)
        self.estado = "FADE_IN"
        self.alpha = 255
        self.tiempo = 0
        self.dialogo_actual = 0
        self.next_background = None

        self.siguienteEscena = Ayuntamiento(director)
        

        self.fondo_noche = pygame.transform.scale(
            pygame.image.load("imagenes/Dialogos/fondo_noche.png"), 
            (WIDTH, HEIGHT)
        )
        self.fondo_callejon = pygame.transform.scale(
            pygame.image.load("imagenes/Dialogos/fondo_callejon.jpg"), 
            (WIDTH, HEIGHT)
        )

        self.soldados_estaticos = [
            pygame.transform.scale(
                pygame.image.load("imagenes/Dialogos/soldado1_estatico.png"),
                (WIDTH//4, HEIGHT//2)
            ),
            pygame.transform.scale(
                pygame.image.load("imagenes/Dialogos/soldado2_estatico.png"),
                (WIDTH//4, HEIGHT//2)
            )
        ]
        
        self.soldados_disparo = [
            pygame.transform.scale(
                pygame.image.load("imagenes/Dialogos/soldado1_disparo.png"),
                (WIDTH//4, HEIGHT//2)
            ),
            pygame.transform.scale(
                pygame.image.load("imagenes/Dialogos/soldado2_disparo.png"),
                (WIDTH//4, HEIGHT//2)
            )
        ]
        

        personaje_altura = HEIGHT//2.2
        self.eddie_imagen = pygame.transform.scale(
            pygame.image.load("imagenes/Dialogos/eddie_imagen.png"),
            (WIDTH//4, personaje_altura)
        )
        self.eddie_imagen = pygame.transform.flip(self.eddie_imagen, True, False)
        
        self.eddie_silueta = self.eddie_imagen.copy()
        self.eddie_silueta.fill((0, 0, 0, 255), special_flags=pygame.BLEND_RGBA_MULT)

        self.vince_imagen = pygame.transform.scale(
            pygame.image.load("imagenes/Dialogos/vince_imagen.png"),
            (WIDTH//5, personaje_altura) 
        )
        
        self.retratos = {
            'comentarios': pygame.image.load("imagenes/Dialogos/comentarios.png"),
            'vince': pygame.image.load("imagenes/Dialogos/vince.png"),
            'otros': pygame.image.load("imagenes/Dialogos/otros.png"),
            'eddie': pygame.image.load("imagenes/Dialogos/eddie.png")
        }
        

        self.fade_surface = pygame.Surface((WIDTH, HEIGHT))
        self.fade_surface.fill(NEGRO)
        
        self.dialogos = [
            {"texto": "Noche cerrada sobre el ayuntamiento de Ironridge", "fondo": "noche", "retrato": "comentarios", "personajes": []},
            {"texto": "Mientras en el ayuntamiento se lleva a cabo una gala, \n fuera de él las cosas se ponen tensas", "fondo": "noche", "retrato": "comentarios", "personajes": []},
            {"texto": "Por favor dispérsense", "fondo": "noche", "retrato": "otros", "mostrar_soldados": True, 
             "soldados_estaticos": True, "personajes": ["eddie"], "siluetas": True},
            {"texto": "Solo queremos hablar con el presidente de Helix", "fondo": "noche", "retrato": "eddie", "mostrar_soldados": True, 
             "soldados_estaticos": True, "personajes": ["eddie"], "siluetas": True},
            {"texto": "Si no se dispersan tendremos que abrir fuego", "fondo": "noche", "retrato": "otros", "mostrar_soldados": True, 
             "soldados_estaticos": True, "personajes": ["eddie"], "siluetas": True},
            {"texto": "No es necesario, solo queremos \n explicaciones del accidente de la fábrica", "fondo": "noche", "retrato": "eddie", "mostrar_soldados": True, 
             "soldados_estaticos": True, "personajes": ["eddie"], "siluetas": True},
            {"texto": "Esto es una manifestación pacífica no estamos haciendo daño a nadie", "fondo": "noche", "retrato": "eddie", "mostrar_soldados": True, 
             "soldados_estaticos": True, "personajes": ["eddie"], "siluetas": True},
            {"texto": "Es la última advertencia, dispérsense", "fondo": "noche", "retrato": "otros", "mostrar_soldados": True, 
             "soldados_estaticos": True, "personajes": ["eddie"], "siluetas": True},
            {"texto": "Señor, le repito que...", "fondo": "noche", "retrato": "eddie", "mostrar_soldados": True, 
             "soldados_estaticos": True, "personajes": ["eddie"], "siluetas": True},
            {"texto": "Apunten", "fondo": "noche", "retrato": "otros", "mostrar_soldados": True, 
             "soldados_estaticos": True, "personajes": ["eddie"], "siluetas": True},
            {"texto": "¡POR FAVOR ESPERE NO..!", "fondo": "noche", "retrato": "eddie", "mostrar_soldados": True, 
             "soldados_estaticos": True, "personajes": ["eddie"], "siluetas": True},
            {"texto": "¡FUEGO!", "fondo": "noche", "retrato": "otros", "mostrar_soldados": True, 
             "soldados_disparo": True, "personajes": ["eddie"], "siluetas": True},
            {"texto": "¡NO!", "fondo": "noche", "retrato": "eddie", "mostrar_soldados": True, 
             "soldados_disparo": True, "personajes": ["eddie"], "siluetas": True},
            {"texto": "Ven conmigo...", "fondo": "negro", "retrato": "vince", "personajes": []},
            {"texto": "Parece que no han ido bien las cosas", "fondo": "callejon", "retrato": "vince", "personajes": ["eddie", "vince"]},
            {"texto": " *respirando con dificultad* Gracias.", "fondo": "callejon", "retrato": "eddie", "personajes": ["eddie", "vince"]},
            {"texto": "No hay por qué darlas", "fondo": "callejon", "retrato": "vince", "personajes": ["eddie", "vince"]},
            {"texto": "Igualmente...", "fondo": "callejon", "retrato": "eddie", "personajes": ["eddie", "vince"]},
            {"texto": "¿Y tú quién eres?", "fondo": "callejon", "retrato": "eddie", "personajes": ["eddie", "vince"]},
            {"texto": "Me llamo Vince y soy quien tiene tu billete para salir de aquí", "fondo": "callejon", "retrato": "vince", "personajes": ["eddie", "vince"]},
            {"texto": "JaJaJa, ¿y por qué querría salir de aquí?", "fondo": "callejon", "retrato": "eddie", "personajes": ["eddie", "vince"]},
            {"texto": "Eddie, por favor no te tengo que decir todo", "fondo": "callejon", "retrato": "vince", "personajes": ["eddie", "vince"]},
            {"texto": "Espera, ¿Cómo sabes mi nombre?", "fondo": "callejon", "retrato": "eddie", "personajes": ["eddie", "vince"]},
            {"texto": "Necesito un compañero y tú cumplías lo requerido", "fondo": "callejon", "retrato": "vince", "personajes": ["eddie", "vince"]},
            {"texto": "¿Compañero de qué?", "fondo": "callejon", "retrato": "eddie", "personajes": ["eddie", "vince"]},
            {"texto": "Compañero para asaltar el banco de Ironridge", "fondo": "callejon", "retrato": "vince", "personajes": ["eddie", "vince"]},
            {"texto": "Tu estas demente", "fondo": "callejon", "retrato": "eddie", "personajes": ["eddie", "vince"]},
            {"texto": "Eddie tú sabes que la vida aquí para ti y tu familia no es segura", "fondo": "callejon", "retrato": "vince", "personajes": ["eddie", "vince"]},
            {"texto": "Y sabes que Helix Global no te ayuda para mantenerla", "fondo": "callejon", "retrato": "vince", "personajes": ["eddie", "vince"]},
            {"texto": "Mira lo que ocurrió con tu hijo", "fondo": "callejon", "retrato": "vince", "personajes": ["eddie", "vince"]},
            {"texto": "Ni se te ocurra volver a nombrar a Max", "fondo": "callejon", "retrato": "eddie", "personajes": ["eddie", "vince"]},
            {"texto": "Esta bien, pero sabes que lo que digo es cierto", "fondo": "callejon", "retrato": "vince", "personajes": ["eddie", "vince"]},
            {"texto": "Y sabes que Helix nunca se hara responsable de lo ocurrido", "fondo": "callejon", "retrato": "vince", "personajes": ["eddie", "vince"]},
            {"texto": "Si quieres cobrar lo que te corresponde escúchame", "fondo": "callejon", "retrato": "vince", "personajes": ["eddie", "vince"]},
            {"texto": "Y cómo esperas robar el banco", "fondo": "callejon", "retrato": "eddie", "personajes": ["eddie", "vince"]},
            {"texto": "Tú tranquilo, ya te explico el plan y cómo escaparemos después, incluida tu familia", "fondo": "callejon", "retrato": "vince", "personajes": ["eddie", "vince"]},
            {"texto": "Así que vamos a tomar algo y te cuento", "fondo": "callejon", "retrato": "vince", "personajes": ["eddie", "vince"]},
            {"texto": "Te escucho, pero no he aceptado todavía", "fondo": "callejon", "retrato": "eddie", "personajes": ["eddie", "vince"]},
            {"texto": "Bueno eso lo veremos...", "fondo": "callejon", "retrato": "vince", "personajes": ["eddie", "vince"]},
        ]

        self.cajas_dialogo = {
            'comentarios': pygame.transform.scale(
                pygame.image.load("imagenes/Dialogos/comentarios.png"),
                (WIDTH * 0.6, HEIGHT * 0.2) 
            ),
            'vince': pygame.transform.scale(
                pygame.image.load("imagenes/Dialogos/vince.png"),
                (WIDTH * 0.6, HEIGHT * 0.2)
            ),
            'otros': pygame.transform.scale(
                pygame.image.load("imagenes/Dialogos/otros.png"),
                (WIDTH * 0.6, HEIGHT * 0.2)
            ),
            'eddie': pygame.transform.scale(
                pygame.image.load("imagenes/Dialogos/eddie.png"),
                (WIDTH * 0.6, HEIGHT * 0.2)
            )
        }
        
        self.nombres_hablantes = {
            'comentarios': 'Narrador',
            'vince': 'Vince',
            'otros': 'Jefe de Policia',
            'eddie': 'Eddie'
        }

        self.fuente = pygame.font.Font(None, 36)
        self.mostrar_triangulo = True
        self.tiempo_parpadeo = 0

    def update(self, tiempo):
        if self.estado == "FADE_IN":
            self.alpha = max(0, self.alpha - 2)
            if self.alpha <= 0:
                self.estado = "DIALOGO"
        elif self.estado == "FADE_OUT":
            self.alpha = min(255, self.alpha + 2)
            if self.alpha >= 255:
                self.dialogo_actual += 1
                self.estado = "FADE_IN"
        
        self.tiempo += tiempo
        self.tiempo_parpadeo += tiempo
        if self.tiempo_parpadeo >= 300:
            self.mostrar_triangulo = not self.mostrar_triangulo
            self.tiempo_parpadeo = 0

    def eventos(self, lista_eventos):
        for evento in lista_eventos:
            if evento.type == pygame.KEYDOWN:
                if self.estado == "DIALOGO":
                    if self.dialogo_actual >= len(self.dialogos) - 1:
                        self.completado = True
                        self.director.cambiarEscena(self.siguienteEscena)
                    else:
                        self.dialogo_actual += 1
            elif evento.type == pygame.QUIT or (evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE):
                self.director.salirEscena()

    def dibujar(self, pantalla):
        if self.dialogo_actual < len(self.dialogos):
            dialogo = self.dialogos[self.dialogo_actual]
            
            if dialogo["fondo"] == "noche":
                pantalla.blit(self.fondo_noche, (0,0))
            elif dialogo["fondo"] == "callejon":
                pantalla.blit(self.fondo_callejon, (0,0))
            elif dialogo["fondo"] == "negro":
                pantalla.fill(NEGRO)
            
            if dialogo.get("mostrar_soldados", False):
                if dialogo.get("soldados_estaticos", False):
                    for i, soldado in enumerate(self.soldados_estaticos):
                        pos_x = WIDTH//8 + (i * WIDTH//6)
                        pos_y = HEIGHT//2 - soldado.get_height()//2
                        pantalla.blit(soldado, (pos_x, pos_y))
                
                if dialogo.get("soldados_disparo", False):
                    for i, soldado in enumerate(self.soldados_disparo):
                        pos_x = WIDTH//8 + (i * WIDTH//6)
                        pos_y = HEIGHT//2 - soldado.get_height()//2
                        pantalla.blit(soldado, (pos_x, pos_y))

            if dialogo.get("siluetas", False):
                siluetas_posiciones = [
                    (WIDTH * 0.5, HEIGHT//2 - self.eddie_silueta.get_height()//2 - 30), 
                    (WIDTH * 0.7, HEIGHT//2 - self.eddie_silueta.get_height()//2 - 15),  
                    (WIDTH * 0.45, HEIGHT//2 - self.eddie_silueta.get_height()//2 + 30),  
                    (WIDTH * 0.65, HEIGHT//2 - self.eddie_silueta.get_height()//2 + 20), 
                    (WIDTH * 0.75, HEIGHT//2 - self.eddie_silueta.get_height()//2),     
                    (WIDTH * 0.55, HEIGHT//2 - self.eddie_silueta.get_height()//2 + 10), 
                ]
                
                for pos in siluetas_posiciones:
                    pantalla.blit(self.eddie_silueta, pos)

            if "personajes" in dialogo:
                if "eddie" in dialogo["personajes"]:
                    eddie_pos = (WIDTH * 0.6, HEIGHT//2 - self.eddie_imagen.get_height()//2)
                    pantalla.blit(self.eddie_imagen, eddie_pos)
                if "vince" in dialogo["personajes"]:
                    vince_pos = (WIDTH * 0.2, HEIGHT//2 - self.vince_imagen.get_height()//2 + 30)
                    pantalla.blit(self.vince_imagen, vince_pos)

            if self.estado == "DIALOGO":
                if "retrato" in dialogo:
                    caja = self.cajas_dialogo[dialogo["retrato"]]
                    dialogo_pos = (
                        (WIDTH - caja.get_width()) // 2, 
                        HEIGHT * 0.65  
                    )
                    pantalla.blit(caja, dialogo_pos)
                    
                    nombre = self.nombres_hablantes[dialogo["retrato"]]
                    nombre_texto = self.fuente.render(nombre, True, NEGRO)
                    nombre_rect = nombre_texto.get_rect()
                    
                    
                    nombre_box_pos = (
                        dialogo_pos[0] - 10,  
                        dialogo_pos[1] - nombre_rect.height//2  
                    )
                    
                    
                    nombre_box_rect = pygame.Rect(
                        nombre_box_pos[0],
                        nombre_box_pos[1],
                        nombre_rect.width + 20,  
                        nombre_rect.height + 10   
                    )
                    pygame.draw.rect(pantalla, BLANCO, nombre_box_rect)  
                    pygame.draw.rect(pantalla, NEGRO, nombre_box_rect, 2)  
                    
                   
                    nombre_pos = (
                        nombre_box_pos[0] + 10, 
                        nombre_box_pos[1] + 5    
                    )
                    pantalla.blit(nombre_texto, nombre_pos)
                    
                    
                    lineas = dialogo["texto"].split('\n')
                    for i, linea in enumerate(lineas):
                        texto = self.fuente.render(linea.strip(), True, NEGRO)
                        texto_pos = (
                            dialogo_pos[0] + 40, 
                            dialogo_pos[1] + caja.get_height()//3 + (i * 30)
                        )
                        pantalla.blit(texto, texto_pos)
                    
                    if self.mostrar_triangulo:
                        triangulo_pos = [
                            (dialogo_pos[0] + caja.get_width() - 40, dialogo_pos[1] + caja.get_height() - 20), 
                            (dialogo_pos[0] + caja.get_width() - 20, dialogo_pos[1] + caja.get_height() - 40),  
                            (dialogo_pos[0] + caja.get_width() - 60, dialogo_pos[1] + caja.get_height() - 40)   
                        ]
                        pygame.draw.polygon(pantalla, NEGRO, triangulo_pos)

        if self.estado in ["FADE_IN", "FADE_OUT"]:
            self.fade_surface.set_alpha(self.alpha)
            pantalla.blit(self.fade_surface, (0,0))
