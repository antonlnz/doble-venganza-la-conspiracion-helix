import pygame
import math
from settings import *
from escena import Escena

class WirePuzzle(Escena):
    def __init__(self, director):
        Escena.__init__(self, director)
        
        # Variables de tiempo y efectos visuales
        self.total_time = 45000  # 45 segundos en milisegundos
        self.time_remaining = self.total_time
        
        # Variables para controlar el inicio del temporizador
        self.timer_started = False
        self.start_time = 0
        self.timer_paused = False  # Variable para pausar el temporizador

        self.mensaje_timer = 0
        self.mensaje_duracion = 2000  # 2 segundos en milisegundos
        self.esperando_mensaje = False
        
        # Variables de tiempo y efectos visuales
        self.timer_alpha = 255
        self.timer_pulse_speed = 0.005
        self.red_halo_active = False
        self.halo_alpha = 0
        self.halo_max_alpha = 100
        
        # Dimensiones y posiciones de los cables
        self.wire_width = WIDTH * 0.3
        self.wire_height = HEIGHT * 0.01
        self.spacing = HEIGHT * 0.1
        # Centramos los cables horizontalmente
        self.start_x = (WIDTH - self.wire_width) / 2
        self.start_y = HEIGHT * 0.4  # Bajamos un poco los cables
        
        # Colores de los cables
        self.wire_colors = [
            (255, 0, 0),    # Rojo
            (0, 255, 0),    # Verde
            (0, 0, 255),    # Azul
            (255, 255, 0)   # Amarillo
        ]
        
        # Letras para cada cable
        self.wire_letters = ['A', 'B', 'C', 'D']
        
        # Estado del puzzle
        self.intentos = 3
        self.wire_correcto = 2
        self.cables_cortados = []
        self.completado = False
        self.mensaje = ""
        
        # Fuente para el texto
        self.font = pygame.font.Font(None, 36)
            
        # Añadir variables para la banda
        self.banda_height = HEIGHT * 0.1  # Altura de la banda
        self.banda_y = HEIGHT * 0.45  # Posición Y de la banda
        self.banda_color = VERDE  # Color del banner horizontal
        
    def dibujar(self, pantalla):
        # Si el temporizador no ha comenzado, iniciarlo al mostrar la primera vez
        if not self.timer_started:
            self.start_time = pygame.time.get_ticks()
            self.timer_started = True
            
        # Dibujar el acertijo
        pregunta = self.font.render("¿Cuál es el siguiente número de esta serie: 3.829, 9.382, 2.938…", True, BLANCO)
        opcionA = self.font.render("A) 8.329", True, BLANCO)
        opcionB = self.font.render("B) 8.239", True, BLANCO)
        opcionC = self.font.render("C) 8.293", True, BLANCO)
        opcionD = self.font.render("D) 8.932", True, BLANCO)
        
        # Posicionar cada línea
        pregunta_rect = pregunta.get_rect()
        pregunta_rect.centerx = WIDTH / 2
        pregunta_rect.y = HEIGHT * 0.1
        
        opcionA_rect = opcionA.get_rect()
        opcionA_rect.centerx = WIDTH / 2
        opcionA_rect.y = HEIGHT * 0.15
        
        opcionB_rect = opcionB.get_rect()
        opcionB_rect.centerx = WIDTH / 2
        opcionB_rect.y = HEIGHT * 0.2
        
        opcionC_rect = opcionC.get_rect()
        opcionC_rect.centerx = WIDTH / 2
        opcionC_rect.y = HEIGHT * 0.25
        
        opcionD_rect = opcionD.get_rect()
        opcionD_rect.centerx = WIDTH / 2
        opcionD_rect.y = HEIGHT * 0.3
        
        # Dibujar cada línea
        pantalla.blit(pregunta, pregunta_rect)
        pantalla.blit(opcionA, opcionA_rect)
        pantalla.blit(opcionB, opcionB_rect)
        pantalla.blit(opcionC, opcionC_rect)
        pantalla.blit(opcionD, opcionD_rect)
        
        # Dibujar los cables y sus letras
        for i in range(4):
            if i not in self.cables_cortados:
                y = self.start_y + (i * self.spacing)
                # Dibujar el cable
                pygame.draw.rect(pantalla, self.wire_colors[i], 
                               (self.start_x, y, self.wire_width, self.wire_height))
                
                # Dibujar la letra centrada con el cable
                letra = self.font.render(self.wire_letters[i], True, BLANCO)
                letra_rect = letra.get_rect()
                letra_rect.right = self.start_x - 10  # 10 píxeles de separación
                letra_rect.centery = y + self.wire_height/2
                pantalla.blit(letra, letra_rect)
        
        if self.completado:
            # Crear y dibujar la banda
            banda = pygame.Surface((WIDTH, self.banda_height))
            if self.mensaje == "¡Correcto! Has desactivado la cámara":
                banda.fill(VERDE)
                color_texto = NEGRO
            else:  # Para "¡Has fallado! La alarma se ha activado"
                banda.fill(ROJO)
                color_texto = NEGRO
            pantalla.blit(banda, (0, self.banda_y))
            
            # Dibujar el mensaje en la banda
            texto_mensaje = self.font.render(self.mensaje, True, color_texto)
            texto_rect = texto_mensaje.get_rect()
            texto_rect.center = (WIDTH/2, self.banda_y + self.banda_height/2)
            pantalla.blit(texto_mensaje, texto_rect)
            
        elif self.mensaje:  # Solo para el mensaje de "Cable incorrecto"
            texto_estado = self.font.render(self.mensaje, True, NARANJA)
            texto_estado_rect = texto_estado.get_rect()
            texto_estado_rect.centerx = WIDTH / 2
            texto_estado_rect.y = HEIGHT * 0.8
            pantalla.blit(texto_estado, texto_estado_rect)
            
        # Dibujar el tiempo restante si el puzzle no está completado
        if not self.completado:
            seconds_left = max(0, int(self.time_remaining / 1000))
            time_text = f"Tiempo: {seconds_left}s"
            
            if seconds_left <= 15:
                time_color = ROJO
                time_surface = self.font.render(time_text, True, time_color)
                time_surface_alpha = pygame.Surface(time_surface.get_size(), pygame.SRCALPHA)
                time_surface_alpha.fill((255, 0, 0, int(self.timer_alpha)))
                time_surface.blit(time_surface_alpha, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
            else:
                time_color = BLANCO
                time_surface = self.font.render(time_text, True, time_color)
            
            pantalla.blit(time_surface, (50, 50))
            
            # Efecto de halo rojo en los últimos 10 segundos
            if seconds_left <= 10 and self.red_halo_active:
                halo_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
                border_size = 100
                
                for grosor in range(border_size):
                    alpha = int((self.halo_alpha * (border_size - grosor) / border_size))
                    pygame.draw.rect(halo_surface, (255, 0, 0, alpha), 
                                    (grosor, grosor, WIDTH - 2 * grosor, HEIGHT - 2 * grosor), 1)
                
                pantalla.blit(halo_surface, (0, 0))
            
        # Dibujar intentos restantes en la esquina superior derecha
        texto_intentos = self.font.render(f"Intentos: {self.intentos}", True, BLANCO)
        texto_intentos_rect = texto_intentos.get_rect()
        texto_intentos_rect.right = WIDTH - 20  # 20 píxeles de margen
        texto_intentos_rect.top = 20  # 20 píxeles desde arriba
        pantalla.blit(texto_intentos, texto_intentos_rect)

    def eventos(self, lista_eventos):
        if not self.completado and self.intentos > 0:
            for evento in lista_eventos:
                if evento.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = evento.pos
                    
                    # Verificar si se hizo clic en algún cable
                    for i in range(4):
                        if i not in self.cables_cortados:
                            y = self.start_y + (i * self.spacing)
                            cable_rect = pygame.Rect(self.start_x, y, self.wire_width, self.wire_height)
                            
                            if cable_rect.collidepoint(mouse_pos):
                                if i == self.wire_correcto:
                                    self.mensaje = "¡Correcto! Has desactivado la cámara"
                                    self.completado = True
                                    self.esperando_mensaje = True
                                    self.mensaje_timer = pygame.time.get_ticks()
                                    self.timer_paused = True  # Pausar el temporizador al completar
                                else:
                                    self.cables_cortados.append(i)
                                    self.intentos -= 1
                                    if self.intentos > 0:
                                        self.mensaje = f"Cable incorrecto. Te quedan {self.intentos} intentos"
                                    else:
                                        self.mensaje = "¡Has fallado! La alarma se ha activado"
                                        self.completado = True
                                        self.esperando_mensaje = True
                                        self.mensaje_timer = pygame.time.get_ticks()
                                        self.timer_paused = True  # Pausar el temporizador al fallar
                                break

    def update(self, tiempo):
        if not self.completado and self.timer_started and not self.timer_paused:
            # Calcular tiempo transcurrido desde el inicio
            current_time = pygame.time.get_ticks()
            elapsed_time = current_time - self.start_time
            self.time_remaining = max(0, self.total_time - elapsed_time)
            
            if self.time_remaining <= 0:
                self.time_remaining = 0
                self.completado = True
                self.mensaje = "¡Has fallado! La alarma se ha activado"
                self.esperando_mensaje = True
                self.mensaje_timer = pygame.time.get_ticks()
                self.timer_paused = True  # Pausar el temporizador al acabarse el tiempo
                self.director.salirEscena()
            
            # Efectos para el temporizador bajo
            segundos_restantes = self.time_remaining / 1000  # Convertir a segundos
            
            if segundos_restantes <= 15:
                self.timer_alpha = 100 + 155 * (0.5 + 0.5 * math.sin(current_time * self.timer_pulse_speed))
            else:
                self.timer_alpha = 255
            
            # Activar el halo rojo en los últimos 10 segundos
            if segundos_restantes <= 10:
                self.red_halo_active = True
                self.halo_alpha = 40 + 40 * math.sin(current_time * 0.003)
            else:
                self.red_halo_active = False
                
        # Comprobar si el tiempo del mensaje ha terminado
        if self.esperando_mensaje:
            tiempo_actual = pygame.time.get_ticks()
            if tiempo_actual - self.mensaje_timer >= self.mensaje_duracion:
                self.esperando_mensaje = False
                self.director.salirEscena()