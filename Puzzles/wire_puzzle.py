import pygame
from settings import *
import math
import os

class WirePuzzle:
    def __init__(self):
        # Obtener la ruta base del proyecto (carpeta raíz)
        self.base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        
        # Construir rutas a los recursos usando os.path.join
        resources_path = os.path.join(self.base_path, "resources", "images", "puzzles")
        panel_path = os.path.join(resources_path, "control_camera_panel.png")
        switch_path = os.path.join(resources_path, "switch.png")
        
        # Cargar imágenes
        self.panel_image = pygame.image.load(panel_path).convert_alpha()
        self.switch_down_image = pygame.image.load(switch_path).convert_alpha()
        
        # Obtener dimensiones originales del panel
        self.original_width = self.panel_image.get_width()
        self.original_height = self.panel_image.get_height()
        
        # Calcular factor de escala
        self.scale_factor = HEIGHT / self.original_height
        self.new_width = int(self.original_width * self.scale_factor)
        self.new_height = int(HEIGHT)
        
        # Escalar el panel
        self.panel_image = pygame.transform.scale(self.panel_image, (self.new_width, self.new_height))
        
        # Tamaño original de los interruptores
        switch_width = 150  # Ancho original del interruptor
        switch_height = 185  # Alto original del interruptor
        
        # Añadir variable para controlar la pausa del temporizador
        self.timer_paused = False
        
        # Escalar el interruptor usando el mismo factor de escala que el panel
        scaled_switch_width = int(switch_width * self.scale_factor)
        scaled_switch_height = int(switch_height * self.scale_factor)
        self.switch_down_image = pygame.transform.scale(self.switch_down_image, 
                                                      (scaled_switch_width, scaled_switch_height))
        
        # Posición del panel
        self.panel_x = (WIDTH - self.new_width) // 2
        self.panel_y = (HEIGHT - self.new_height) // 2
        
        # Coordenadas originales de los interruptores en la imagen (x, y)
        self.original_switch_positions = [ # Coordenadas de la imagen original
            # Interruptores fila A
            (1200, 1640), # Interruptor 1
            (1410, 1640), # Interruptor 2
            (1610, 1640), # Interruptor 3
            (1817, 1640), # Interruptor 4
            (2020, 1640), # Interruptor 5

            # Interruptores fila B
            (1200, 2320), # Interruptor 6
            (1410, 2320), # Interruptor 7
            (1610, 2320), # Interruptor 8
            (1817, 2320), # Interruptor 9
            (2020, 2320), # Interruptor 10

            # Interruptores fila C
            (1200, 3000), # Interruptor 11
            (1410, 3000), # Interruptor 12
            (1610, 3000), # Interruptor 13
            (1817, 3000), # Interruptor 14
            (2020, 3000), # Interruptor 15

            # Interruptores fila D
            (1200, 3680), # Interruptor 16
            (1410, 3680), # Interruptor 17
            (1610, 3680), # Interruptor 18
            (1817, 3680), # Interruptor 19
            (2020, 3680) # Interruptor 20
        ]
        
        self.switch_states = [False] * len(self.original_switch_positions)
        self.disabled_switches = [False] * len(self.original_switch_positions)  # Nueva lista para rastrear interruptores deshabilitados
        
        # Crear los rectángulos escalados
        self.switch_areas = []
        for orig_x, orig_y in self.original_switch_positions:
            # Escalar las coordenadas
            scaled_x = int(orig_x * self.scale_factor) + self.panel_x
            scaled_y = int(orig_y * self.scale_factor) + self.panel_y
            # Crear el rectángulo con las coordenadas escaladas
            self.switch_areas.append(
                pygame.Rect(scaled_x, scaled_y, scaled_switch_width, scaled_switch_height)
            )
        
        # Estado del puzzle
        self.puzzle_solved = False
        self.puzzle_failed = False
        self.show_message = False
        self.message_timer = 0
        
        # Contador de intentos
        self.attempts_left = 3
        self.game_over = False
        
        # Temporizador para el puzzle
        self.time_limit = 45000  # 45 segundos en milisegundos
        self.time_remaining = self.time_limit
        
        # Variables para animación de tiempo
        self.timer_alpha = 255
        self.timer_pulsing = False
        self.timer_pulse_speed = 0.01
        
        # Variables para el halo rojo
        self.red_halo_active = False
        self.halo_alpha = 0
        self.halo_max_alpha = 100
        
        # Respuesta correcta (C corresponde a la fila C - interruptores 11-15)
        self.correct_answer = 2  # índice 0:A, 1:B, 2:C, 3:D
        
        # Agrupar interruptores por filas
        self.rows = [
            [0, 1, 2, 3, 4],      # Fila A
            [5, 6, 7, 8, 9],      # Fila B
            [10, 11, 12, 13, 14], # Fila C
            [15, 16, 17, 18, 19]  # Fila D
        ]
        
        # Fuente para los mensajes
        self.font = pygame.font.SysFont('Arial', 40, bold=True)
        self.small_font = pygame.font.SysFont('Arial', 24, bold=True)

    def dibujar(self, pantalla):
        # Dibujar el panel
        pantalla.blit(self.panel_image, (self.panel_x, self.panel_y))
        
        # Para debug: dibujar un punto rojo en cada posición de interruptor
        #for i, area in enumerate(self.switch_areas):
            # Solo dibujar bordes rojos para los interruptores que no están deshabilitados
        #    if not self.disabled_switches[i]:
        #        pygame.draw.rect(pantalla, ROJO, area, 1)
        
        # Dibujar interruptores activados o deshabilitados
        for i in range(len(self.switch_states)):
            if self.switch_states[i] or self.disabled_switches[i]:
                pantalla.blit(self.switch_down_image, 
                            (self.switch_areas[i].x, self.switch_areas[i].y))
        
        # Mostrar información de intentos y tiempo restante
        if not self.puzzle_solved and not self.game_over:
            # Crear un fondo para los indicadores
            info_bg = pygame.Surface((200, 80), pygame.SRCALPHA)
            info_bg.fill((0, 0, 0, 180))  # Negro semitransparente
            pantalla.blit(info_bg, (40, 40))
            
            # Mostrar intentos restantes con color según cantidad
            attempts_text = f"Intentos: {self.attempts_left}"
            if self.attempts_left == 3:
                attempts_color = VERDE
            elif self.attempts_left == 2:
                attempts_color = NARANJA
            else:  # 1 intento
                attempts_color = ROJO
            
            # Dibujar textos de intentos y tiempo
            attempts_surface = self.small_font.render(attempts_text, True, attempts_color)
            pantalla.blit(attempts_surface, (50, 50))
            
            # Mostrar tiempo restante con efecto de parpadeo en los últimos 15 segundos
            seconds_left = max(0, int(self.time_remaining / 1000))
            time_text = f"Tiempo: {seconds_left}s"
            
            if seconds_left <= 15:  # Cambiado de 10 a 15 segundos
                # Crear una superficie con canal alfa para el parpadeo
                time_color = ROJO
                time_surface = self.small_font.render(time_text, True, time_color)
                time_surface_alpha = pygame.Surface(time_surface.get_size(), pygame.SRCALPHA)
                time_surface_alpha.fill((255, 0, 0, int(self.timer_alpha)))
                time_surface.blit(time_surface_alpha, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
            else:
                time_color = BLANCO
                time_surface = self.small_font.render(time_text, True, time_color)
            
            pantalla.blit(time_surface, (50, 90))
            
            question_width = WIDTH - 900  # Reducir ancho para no tapar contador
            question_height = 150  # Aumentar altura para añadir instrucciones
            question_y = 20  # Mantener arriba para evitar superposiciones
            question_x = WIDTH // 2 - question_width // 2  # Centrar el fondo
            
            # Crear un fondo negro semitransparente para la pregunta
            question_bg = pygame.Surface((question_width, question_height), pygame.SRCALPHA)
            question_bg.fill((0, 0, 0, 180))  # Negro semitransparente
            pantalla.blit(question_bg, (question_x, question_y))
            
            # Mostrar pregunta con una fuente más grande
            self.medium_font = pygame.font.SysFont('Arial', 28, bold=True)
            question_text = "¿Cuál es el siguiente número de esta serie: 3.829, 9.382, 2.938...?"
            question_surface = self.medium_font.render(question_text, True, BLANCO)
            pantalla.blit(question_surface, (WIDTH // 2 - question_surface.get_width() // 2, question_y + 20))
            
            # Mostrar opciones
            options_text = "A) 8.329   B) 8.239   C) 8.293   D) 8.932"
            options_surface = self.medium_font.render(options_text, True, BLANCO)
            pantalla.blit(options_surface, (WIDTH // 2 - options_surface.get_width() // 2, question_y + 60))
            
            # Instrucciones para resolver el puzzle
            self.small_font = pygame.font.SysFont('Arial', 20, bold=True)
            instruction_text = "Baja los interruptores de la fila correspondiente a la letra correcta (A, B, C o D)"
            instruction_surface = self.small_font.render(instruction_text, True, BLANCO)
            pantalla.blit(instruction_surface, (WIDTH // 2 - instruction_surface.get_width() // 2, question_y + 100))
            
            # Dibujar el halo rojo en los últimos 10 segundos
            if seconds_left <= 10 and self.red_halo_active:
                # Crear una superficie semitransparente para el halo
                halo_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
                
                # Crear un efecto de halo continuo al rededor del borde del panel
                border_size = 100  # Tamaño del borde donde se concentra el efecto
                
                # En lugar de dibujar líneas separadas, dibujamos un rectángulo con degradado
                for grosor in range(border_size):
                    # Calcular alfa basado en distancia al borde (más opaco en los bordes)
                    alpha = int((self.halo_alpha * (border_size - grosor) / border_size))
                    
                    # Dibujar un rectángulo completo (contorno) para cada nivel de opacidad
                    pygame.draw.rect(halo_surface, (255, 0, 0, alpha), 
                                    (grosor, grosor, WIDTH - 2 * grosor, HEIGHT - 2 * grosor), 1)
                
                pantalla.blit(halo_surface, (0, 0))
        
        # Mostrar mensaje si corresponde
        if self.show_message:
            if self.puzzle_solved:
                message = "¡Correcto! Has desactivado la cámara"
                color = VERDE
            elif self.game_over:
                if self.time_remaining <= 0:
                    message = "¡Se acabó el tiempo! Fallaste el puzzle"
                else:
                    message = "¡Sin intentos restantes! Fallaste el puzzle"
                color = ROJO
            else:
                message = f"¡Has fallado! Te quedan {self.attempts_left} intentos"
                color = ROJO
            
            text_surface = self.font.render(message, True, color)
            text_rect = text_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2))
            
            # Dibuja un fondo semitransparente para el mensaje
            banner_rect = text_rect.inflate(50, 20)
            banner_surface = pygame.Surface((banner_rect.width, banner_rect.height), pygame.SRCALPHA)
            banner_surface.fill((0, 0, 0, 180))
            pantalla.blit(banner_surface, banner_rect)
            
            # Dibuja el mensaje
            pantalla.blit(text_surface, text_rect)
    
    def resetear_interruptores_activos(self):
        # Resetear los interruptores que no están deshabilitados
        for i in range(len(self.switch_states)):
            if not self.disabled_switches[i]:
                self.switch_states[i] = False
    
    def eventos(self, mouse_click):
        if mouse_click and not self.show_message and not self.puzzle_solved and not self.game_over:
            mouse_pos = pygame.mouse.get_pos()
            
            # Verificar si se hizo clic en algún interruptor
            for i, area in enumerate(self.switch_areas):
                if area.collidepoint(mouse_pos) and not self.disabled_switches[i] and not self.switch_states[i]:
                    self.switch_states[i] = True
                    
                    # Encontrar a qué fila pertenece este interruptor
                    current_row = None
                    current_row_index = None
                    for row_index, row in enumerate(self.rows):
                        if i in row:
                            current_row = row
                            current_row_index = row_index
                            break
                    
                    # Solo verificar la fila actual si está completa
                    if current_row and all(self.switch_states[j] for j in current_row):
                        self.show_message = True
                        self.message_timer = 3000
                        
                        if current_row_index == self.correct_answer:
                            self.puzzle_solved = True
                        else:
                            self.puzzle_failed = True
                            self.attempts_left -= 1
                            
                            # Marcar los interruptores de esta fila como deshabilitados
                            for switch_index in current_row:
                                self.disabled_switches[switch_index] = True
                            
                            # Activar game over solo cuando no quedan intentos
                            if self.attempts_left <= 0:
                                self.game_over = True
                    break
    
    def _check_row_completion(self):
        # Comprobar si se ha completado alguna fila
        for row_index, row in enumerate(self.rows):
            if all(self.switch_states[i] for i in row):
                self.show_message = True
                self.message_timer = 3000  # 3 segundos
                
                # Comprobar si es la respuesta correcta (fila C)
                if row_index == self.correct_answer:
                    self.puzzle_solved = True
                else:
                    self.puzzle_failed = True
                    self.attempts_left -= 1
                    
                    print(f"Fallo. Intentos restantes: {self.attempts_left}") 
                    
                    # Marcar los interruptores de esta fila como deshabilitados
                    for switch_index in row:
                        self.disabled_switches[switch_index] = True
                    
                    if self.attempts_left == 0:
                        print("Game over activado")
                        self.game_over = True
    
    def update(self, tiempo):
        # Actualizar el temporizador del puzzle solo si el juego está activo y no está pausado
        if not self.puzzle_solved and not self.game_over and not self.timer_paused:
            self.time_remaining -= tiempo
            segundos_restantes = max(0, int(self.time_remaining / 1000))
            
            # Activar efectos de parpadeo en los últimos 15 segundos
            if segundos_restantes <= 15:
                self.timer_pulsing = True
                # Calcular valor de alfa para el parpadeo del temporizador (oscila entre 100 y 255)
                self.timer_alpha = 100 + 155 * (0.5 + 0.5 * math.sin(pygame.time.get_ticks() * self.timer_pulse_speed))
            else:
                self.timer_pulsing = False
                self.timer_alpha = 255
            
            # Activar el halo rojo en los últimos 10 segundos
            if segundos_restantes <= 10:
                self.red_halo_active = True
                # Calcular valor de alfa para el halo (oscila entre 0 y max_alpha)
                self.halo_alpha = self.halo_max_alpha * (0.5 + 0.5 * math.sin(pygame.time.get_ticks() * 0.005))
            else:
                self.red_halo_active = False
            
            # Verificar si se acabó el tiempo
            if self.time_remaining <= 0:
                self.time_remaining = 0
                self.game_over = True
                self.show_message = True
                self.message_timer = 3000
                self.timer_paused = True
        
        # Actualizar el temporizador del mensaje si está visible
        if self.show_message and self.message_timer > 0:
            self.timer_paused = True  # Pausar temporizador mientras se muestra el mensaje
            self.message_timer -= tiempo
            if self.message_timer <= 0:
                self.show_message = False
                self.timer_paused = False  # Reanudar temporizador cuando desaparece el mensaje
                # Si el puzzle no está resuelto y no se acabó el juego, resetear interruptores activos
                if not self.puzzle_solved and not self.game_over:
                    self.resetear_interruptores_activos()
                    self.puzzle_failed = False