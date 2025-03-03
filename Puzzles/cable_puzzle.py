import pygame
from settings import *
import math
import os
import random

# Se trata del puzzle de cables para desactivar la cámara del almacén
class CablePuzzle:
    def __init__(self):
        # Obtener la ruta base del proyecto
        self.base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        
        # Panel
        self.panel_width = WIDTH * 0.9
        self.panel_height = HEIGHT * 0.9
        self.panel_x = (WIDTH - self.panel_width) // 2
        self.panel_y = (HEIGHT - self.panel_height) // 2
        self.panel = pygame.Surface((self.panel_width, self.panel_height))
        self.panel.fill((40, 40, 40))  # Color oscuro para el panel
        
        # Patrones complejos para los conectores
        self.patterns = [
            "circuito",
            "engranaje", 
            "átomo", 
            "cruz", 
            "triángulo",
            "hexágono", 
            "espiral", 
            "diamante"
        ]
        
        # Colores para los cables y sus patrones de rayas 
        self.cable_colors = [
            [(255, 0, 0), (0, 0, 255), (255, 255, 0)],      # Rojo-Azul-Amarillo
            [(0, 255, 0), (255, 0, 255), (0, 255, 255)],    # Verde-Magenta-Cian
            [(255, 128, 0), (0, 0, 255), (255, 255, 255)],  # Naranja-Azul-Blanco
            [(255, 0, 0), (255, 255, 255), (0, 0, 255)]     # Rojo-Blanco-Azul
        ]
        
        # Crear conectores de inicio (izquierda)
        self.start_connectors = []
        self.start_patterns = []
        for i in range(4):
            y_pos = self.panel_y + (i + 1) * (self.panel_height / 5)
            connector = pygame.Rect(self.panel_x + 50, y_pos - 15, 40, 40)
            pattern = random.choice(self.patterns)
            self.start_connectors.append(connector)
            self.start_patterns.append(pattern)
        
        # Crear conectores de fin (derecha) - mismo patrón pero en orden aleatorio
        self.end_connectors = []
        self.end_patterns = self.start_patterns.copy()
        random.shuffle(self.end_patterns)
        
        # Crear trozos de cable distractores en los conectores de fin
        self.distractor_cables = []
        used_colors = []
        self.connection_radius = 25
        
        for i in range(4):
            y_pos = self.panel_y + (i + 1) * (self.panel_height / 5)
            connector = pygame.Rect(self.panel_x + self.panel_width - 90, y_pos - 15, 40, 40)
            self.end_connectors.append(connector)
            
            # Seleccionar un color de cable distinto para cada distractor
            color_index = i
            while color_index in used_colors:
                color_index = random.randint(0, 3)
            used_colors.append(color_index)
            
            # El punto de conexión será el inicio del cable distractor
            connection_point = (connector.left - 40, connector.centery)
            
            # Crear un pequeño trozo de cable distractor
            distractor = {
                "start": connection_point,
                "end": connector.center,
                "color_pattern": self.cable_colors[color_index],
                "connection_point": connection_point
            }
            self.distractor_cables.append(distractor)
        
        # Cables principales y sus estados
        self.cables = []
        self.selected_cable = None
        self.dragging = False
        for i in range(4):
            start_x, start_y = self.start_connectors[i].center
            
            cable = {
                "start": (start_x, start_y),
                "end": (start_x + 60, start_y),  # Posición inicial cerca del comienzo
                "color_pattern": self.cable_colors[i],  # Patrón de color para rayas
                "connected": False,
                "start_pattern": self.start_patterns[i],  # Patrón del conector inicial
                "connection": None,  # A qué conector final está conectado
            }
            self.cables.append(cable)
        
        # Estado del puzzle
        self.puzzle_solved = False
        self.puzzle_failed = False
        self.show_message = False
        self.message_timer = 0
        self.attempts_left = 3
        self.game_over = False
        
        # Temporizador
        self.time_limit = 60000
        self.time_remaining = self.time_limit
        self.timer_paused = False
        
        # Efectos visuales
        self.timer_alpha = 255
        self.timer_pulsing = False
        self.timer_pulse_speed = 0.01
        self.red_halo_active = False
        self.halo_alpha = 0
        self.halo_max_alpha = 100
        
        # Fuentes
        self.font = pygame.font.SysFont('Arial', 40, bold=True)
        self.small_font = pygame.font.SysFont('Arial', 24, bold=True)
        self.medium_font = pygame.font.SysFont('Arial', 28, bold=True)
        
    def draw_pattern(self, pantalla, pattern, rect, color=(255, 255, 255)):
        """Dibuja un patrón complejo dentro del rectángulo dado"""
        x, y = rect.center
        radius = min(rect.width, rect.height) // 2 - 2
        
        if pattern == "circuito":
            # Dibujar un patrón de circuito
            pygame.draw.circle(pantalla, color, (x, y), radius, 2)
            pygame.draw.line(pantalla, color, (x - radius, y), (x - radius//2, y), 2)
            pygame.draw.line(pantalla, color, (x + radius//2, y), (x + radius, y), 2)
            pygame.draw.line(pantalla, color, (x, y - radius), (x, y - radius//2), 2)
            pygame.draw.line(pantalla, color, (x, y + radius//2), (x, y + radius), 2)
            pygame.draw.circle(pantalla, color, (x, y), radius//3, 0)
            
        elif pattern == "engranaje":
            # Dibujar un engranaje
            tooth_length = radius // 4
            num_teeth = 8
            inner_radius = radius - tooth_length
            
            for i in range(num_teeth):
                angle = 2 * math.pi * i / num_teeth
                cos_val = math.cos(angle)
                sin_val = math.sin(angle)
                
                inner_x = x + inner_radius * cos_val
                inner_y = y + inner_radius * sin_val
                outer_x = x + radius * cos_val
                outer_y = y + radius * sin_val
                
                pygame.draw.line(pantalla, color, (inner_x, inner_y), (outer_x, outer_y), 2)
            
            pygame.draw.circle(pantalla, color, (x, y), inner_radius, 1)
            pygame.draw.circle(pantalla, color, (x, y), radius//3, 0)
            
        elif pattern == "átomo":
            # Dibujar un átomo (círculo con órbitas elípticas)
            pygame.draw.circle(pantalla, color, (x, y), radius//3, 0)
            
            for rotation in [0, math.pi/3, 2*math.pi/3]:
                ellipse_rect = pygame.Rect(x - radius, y - radius//2, radius*2, radius)
                surface = pygame.Surface((radius*2, radius), pygame.SRCALPHA)
                pygame.draw.ellipse(surface, color, (0, 0, radius*2, radius), 1)
                
                rotated_surface = pygame.transform.rotozoom(surface, math.degrees(rotation), 1)
                rotated_rect = rotated_surface.get_rect(center=(x, y))
                pantalla.blit(rotated_surface, rotated_rect)
                
        elif pattern == "cruz":
            # Dibujar una cruz compleja
            thickness = 2
            arm_length = radius * 0.7
            
            pygame.draw.line(pantalla, color, (x - arm_length, y), (x + arm_length, y), thickness)
            pygame.draw.line(pantalla, color, (x, y - arm_length), (x, y + arm_length), thickness)
            
            # Añadir detalles a la cruz
            small_radius = radius // 3
            pygame.draw.circle(pantalla, color, (x, y), small_radius, 1)
            
        elif pattern == "triángulo":
            # Dibujar un triángulo con detalles
            points = [
                (x, y - radius),
                (x - radius * 0.866, y + radius * 0.5),
                (x + radius * 0.866, y + radius * 0.5)
            ]
            pygame.draw.polygon(pantalla, color, points, 2)
            
            # Añadir círculo interior
            pygame.draw.circle(pantalla, color, (x, y), radius // 2, 1)
            
            # Añadir líneas interiores
            center = (x, y)
            for point in points:
                pygame.draw.line(pantalla, color, center, point, 1)
                
        elif pattern == "hexágono":
            # Dibujar un hexágono con detalles
            points = []
            for i in range(6):
                angle = 2 * math.pi * i / 6 + math.pi/6
                px = x + radius * math.cos(angle)
                py = y + radius * math.sin(angle)
                points.append((px, py))
            
            pygame.draw.polygon(pantalla, color, points, 2)
            
            # Añadir detalles internos
            for i in range(0, 6, 2):
                pygame.draw.line(pantalla, color, points[i], points[(i+3)%6], 1)
                
        elif pattern == "espiral":
            # Dibujar una espiral
            a = radius / 10  # Factor de expansión
            num_points = 100
            prev_point = None
            
            for i in range(num_points):
                theta = 0.1 * i
                r = a * theta
                if r > radius:
                    break
                    
                px = x + r * math.cos(theta)
                py = y + r * math.sin(theta)
                
                if prev_point:
                    pygame.draw.line(pantalla, color, prev_point, (px, py), 2)
                prev_point = (px, py)
                
        elif pattern == "diamante":
            # Dibujar un diamante con detalles internos
            points = [
                (x, y - radius),
                (x + radius, y),
                (x, y + radius),
                (x - radius, y)
            ]
            pygame.draw.polygon(pantalla, color, points, 2)
            
            # Añadir líneas diagonales
            pygame.draw.line(pantalla, color, points[0], points[2], 1)
            pygame.draw.line(pantalla, color, points[1], points[3], 1)
            
            # Añadir círculo central
            pygame.draw.circle(pantalla, color, (x, y), radius // 3, 1)
    
    def draw_striped_cable(self, pantalla, start_pos, end_pos, color_pattern, thickness=5, stripe_width=15):
        """Dibuja un cable con una secuencia de colores que se repite"""
        # Calcular longitud y ángulo del cable
        dx = end_pos[0] - start_pos[0]
        dy = end_pos[1] - start_pos[1]
        length = math.sqrt(dx*dx + dy*dy)
        angle = math.atan2(dy, dx)
        
        # Calcular segmentos basados en la secuencia de colores
        segment_length = stripe_width * len(color_pattern)
        num_full_patterns = int(length / segment_length)
        
        # Dibujar los segmentos completos
        for pattern in range(num_full_patterns + 1):
            for i, color in enumerate(color_pattern):
                start_dist = pattern * segment_length + i * stripe_width
                if start_dist >= length:
                    break
                    
                end_dist = min(start_dist + stripe_width, length)
                
                # Calcular puntos de inicio y fin del segmento
                start_x = start_pos[0] + math.cos(angle) * start_dist
                start_y = start_pos[1] + math.sin(angle) * start_dist
                end_x = start_pos[0] + math.cos(angle) * end_dist
                end_y = start_pos[1] + math.sin(angle) * end_dist
                
                # Dibujar el segmento de color
                pygame.draw.line(pantalla, color, (start_x, start_y), (end_x, end_y), thickness)
    
    def dibujar(self, pantalla):
        # Dibujar panel de fondo
        pantalla.blit(self.panel, (self.panel_x, self.panel_y))
        pygame.draw.rect(pantalla, BLANCO, (self.panel_x, self.panel_y, self.panel_width, self.panel_height), 3)
        
        # Dibujar conectores de inicio (izquierda)
        for i, connector in enumerate(self.start_connectors):
            pygame.draw.rect(pantalla, GRIS, connector)
            pygame.draw.rect(pantalla, BLANCO, connector, 2)
            self.draw_pattern(pantalla, self.start_patterns[i], connector)
        
        # Dibujar cables distractores y conectores de fin (derecha)
        for i, (connector, distractor) in enumerate(zip(self.end_connectors, self.distractor_cables)):
            # Dibujar el cable distractor primero
            self.draw_striped_cable(pantalla, distractor["start"], distractor["end"], distractor["color_pattern"])
            
            # Dibujar un círculo en el punto de conexión para hacerlo más visible
            # pygame.draw.circle(pantalla, GRIS, distractor["connection_point"], self.connection_radius, 2)
            
            # Luego dibujar el conector
            pygame.draw.rect(pantalla, GRIS, connector)
            pygame.draw.rect(pantalla, BLANCO, connector, 2)
            self.draw_pattern(pantalla, self.end_patterns[i], connector)
        
        # Dibujar cables principales
        for cable in self.cables:
            self.draw_striped_cable(pantalla, cable["start"], cable["end"], cable["color_pattern"])
        
        # Mostrar instrucciones y estado del juego
        if not self.puzzle_solved and not self.game_over:
            # Información de intentos y tiempo
            info_bg = pygame.Surface((200, 80), pygame.SRCALPHA)
            info_bg.fill((0, 0, 0, 180))
            pantalla.blit(info_bg, (40, 40))
            
            # Intentos restantes con color según cantidad
            attempts_text = f"Intentos: {self.attempts_left}"
            if self.attempts_left == 3:
                attempts_color = VERDE
            elif self.attempts_left == 2:
                attempts_color = NARANJA
            else:
                attempts_color = ROJO
            
            attempts_surface = self.small_font.render(attempts_text, True, attempts_color)
            pantalla.blit(attempts_surface, (50, 50))
            
            # Tiempo restante
            seconds_left = max(0, int(self.time_remaining / 1000))
            time_text = f"Tiempo: {seconds_left}s"
            
            if seconds_left <= 15:
                time_color = ROJO
                time_surface = self.small_font.render(time_text, True, time_color)
                time_surface_alpha = pygame.Surface(time_surface.get_size(), pygame.SRCALPHA)
                time_surface_alpha.fill((255, 0, 0, int(self.timer_alpha)))
                time_surface.blit(time_surface_alpha, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
            else:
                time_color = BLANCO
                time_surface = self.small_font.render(time_text, True, time_color)
            
            pantalla.blit(time_surface, (50, 90))
            
            # Panel de instrucciones
            instruction_width = WIDTH - 600
            instruction_height = 120
            instruction_y = 20
            instruction_x = WIDTH // 2 - instruction_width // 2
            
            instruction_bg = pygame.Surface((instruction_width, instruction_height), pygame.SRCALPHA)
            instruction_bg.fill((0, 0, 0, 180))
            pantalla.blit(instruction_bg, (instruction_x, instruction_y))
            
            # Mostrar Instrucciones
            title_text = "Sistema de Desactivación de Cámaras"
            title_surface = self.medium_font.render(title_text, True, BLANCO)
            pantalla.blit(title_surface, (WIDTH // 2 - title_surface.get_width() // 2, instruction_y + 15))
            
            instr_text = "Arrastra los cables del panel izquierdo a los cables del derecho"
            instr_surface = self.small_font.render(instr_text, True, BLANCO)
            pantalla.blit(instr_surface, (WIDTH // 2 - instr_surface.get_width() // 2, instruction_y + 55))
            
            tip_text = "Estudia detenidamente el sistema para encontrar el patrón correcto de conexiones. Pista: fíjate en los conectores"
            tip_surface = self.small_font.render(tip_text, True, NARANJA)
            pantalla.blit(tip_surface, (WIDTH // 2 - tip_surface.get_width() // 2, instruction_y + 85))
            
            # Efecto rojo en los últimos 10 segundos
            if seconds_left <= 10 and self.red_halo_active:
                halo_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
                border_size = 100
                
                for grosor in range(border_size):
                    alpha = int((self.halo_alpha * (border_size - grosor) / border_size))
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
            
            banner_rect = text_rect.inflate(50, 20)
            banner_surface = pygame.Surface((banner_rect.width, banner_rect.height), pygame.SRCALPHA)
            banner_surface.fill((0, 0, 0, 180))
            pantalla.blit(banner_surface, banner_rect)
            
            pantalla.blit(text_surface, text_rect)
    
    def eventos(self, evento):
        if self.show_message or self.puzzle_solved or self.game_over:
            return
            
        if evento.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            # Verificar si se hizo clic en un extremo de cable
            for i, cable in enumerate(self.cables):
                if not cable["connected"]:
                    end_x, end_y = cable["end"]
                    distance = math.sqrt((mouse_pos[0] - end_x)**2 + (mouse_pos[1] - end_y)**2)
                    if distance < 15:
                        self.selected_cable = i
                        self.dragging = True
                        break
                        
        elif evento.type == pygame.MOUSEMOTION and self.dragging:
            self.cables[self.selected_cable]["end"] = pygame.mouse.get_pos()
            
        elif evento.type == pygame.MOUSEBUTTONUP:
            if self.dragging and self.selected_cable is not None:
                mouse_pos = pygame.mouse.get_pos()
                cable = self.cables[self.selected_cable]
                
                # Verificar si el cable se soltó cerca de un punto de conexión de distractor
                connected = False
                for i, distractor in enumerate(self.distractor_cables):
                    connection_point = distractor["connection_point"]
                    distance = math.sqrt((mouse_pos[0] - connection_point[0])**2 + 
                                    (mouse_pos[1] - connection_point[1])**2)
                    
                    if distance < self.connection_radius:  # Usar el nuevo radio de detección
                        # Ajustar el cable al punto de conexión del distractor
                        cable["end"] = connection_point
                        cable["connected"] = True
                        cable["connection"] = i
                        connected = True
                        break
                
                # Si no se conectó, volver a la posición inicial
                if not connected:
                    start_x, start_y = cable["start"]
                    cable["end"] = (start_x + 60, start_y)
                    cable["connected"] = False
                    cable["connection"] = None
                
                # Verificar si todos los cables están conectados
                if all(c["connected"] for c in self.cables):
                    self._check_connections()
                
                self.dragging = False
                self.selected_cable = None
    
    def _check_connections(self):
        """Verificar si los cables están correctamente conectados"""
        correct_connections = True
        
        for cable in self.cables:
            if cable["connected"] and cable["connection"] is not None:
                # El cable está conectado correctamente si el símbolo del conector de inicio 
                # coincide con el símbolo del conector al que está conectado el distractor
                start_pattern = cable["start_pattern"]
                end_pattern = self.end_patterns[cable["connection"]]
                
                if start_pattern != end_pattern:
                    correct_connections = False
                    break
        
        self.show_message = True
        self.message_timer = 3000
        
        if correct_connections:
            self.puzzle_solved = True
        else:
            self.puzzle_failed = True
            self.attempts_left -= 1
            
            # Restaurar cables a su posición inicial
            for cable in self.cables:
                start_x, start_y = cable["start"]
                cable["end"] = (start_x + 60, start_y)
                cable["connected"] = False
                cable["connection"] = None
            
            if self.attempts_left <= 0:
                self.game_over = True
    
    def update(self, tiempo):
        # Actualizar el temporizador si el juego está activo y no está pausado
        if not self.puzzle_solved and not self.game_over and not self.timer_paused:
            self.time_remaining -= tiempo
            segundos_restantes = max(0, int(self.time_remaining / 1000))
            
            # Efectos visuales para el tiempo
            if segundos_restantes <= 15:
                self.timer_pulsing = True
                self.timer_alpha = 100 + 155 * (0.5 + 0.5 * math.sin(pygame.time.get_ticks() * self.timer_pulse_speed))
            else:
                self.timer_pulsing = False
                self.timer_alpha = 255
            
            # Halo rojo en los últimos 10 segundos
            if segundos_restantes <= 10:
                self.red_halo_active = True
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
        
        # Actualizar el temporizador del mensaje
        if self.show_message and self.message_timer > 0:
            self.timer_paused = True
            self.message_timer -= tiempo
            if self.message_timer <= 0:
                self.show_message = False
                self.timer_paused = False
                self.puzzle_failed = False