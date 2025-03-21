import pygame
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
            {"texto": "La noche era fría y oscura...", "fondo": "noche", "retrato": "comentarios", "personajes": []},
            {"texto": "¿Qué tenemos aquí?", "fondo": "noche", "retrato": "eddie", "mostrar_soldados": True, "soldados_estaticos": True, "personajes": ["eddie"]},
            {"texto": "¡Alto ahí!", "fondo": "noche", "retrato": "otros", "mostrar_soldados": True, "soldados_disparo": True, "personajes": ["eddie"]},
            {"texto": "Todo se volvió negro...", "fondo": "negro", "retrato": "eddie", "personajes": []},
            {"texto": "No puede ser...", "fondo": "callejon", "retrato": "vince", "personajes": ["eddie", "vince"]},
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
                        self.director.salirEscena()
                    else:
                        self.dialogo_actual += 1
            elif evento.type == pygame.QUIT:
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
                    texto = self.fuente.render(dialogo["texto"], True, NEGRO)
                    texto_pos = (dialogo_pos[0] + 40, dialogo_pos[1] + caja.get_height()//3)
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
