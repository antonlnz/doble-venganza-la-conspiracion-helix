import pygame
import math
import random
from settings import *

class ConcentricCirclesPuzzle:
    def __init__(self):
        # Configuración general del puzzle
        self.center_x = WIDTH // 2
        self.center_y = HEIGHT // 2
        self.num_circles = 6
        self.circle_spacing = 30  # Espacio entre anillos
        self.notch_width = 60  # Ancho de la muesca
        
        # Configuración de los anillos
        self.circles = []
        base_radius = 100
        for i in range(self.num_circles):
            radius = base_radius + (i * self.circle_spacing)
            # Ángulo aleatorio para la muesca (en radianes)
            angle = random.random() * 2 * math.pi
            self.circles.append({
                'radius': radius,
                'angle': angle,  # Ángulo de la muesca
                'color': (150 + i * 20, 150 + i * 10, 200 - i * 10)  # Colores distintos
            })
        
        # Ángulo objetivo (donde deben alinearse todas las muescas)
        self.target_angle = math.pi / 2  # Hacia abajo
        
        # Estado del puzzle
        self.last_mouse_angle = None
        self.selected_circle = None
        self.time_remaining = 45000  # 45 segundos en milisegundos
        self.completado = False
        self.game_over = False
        self.show_message = False
        self.message_timer = 0
        self.mensaje = ""
        self.solved_time = 0
        
        # Animación de la llave
        self.key_animation = False
        self.key_progress = 0  # 0 a 1 para la animación
        
        # Efectos visuales
        self.timer_alpha = 255
        self.timer_pulse_speed = 0.005
        self.red_halo_active = False
        self.halo_alpha = 0
        
        # Fuentes
        self.font = pygame.font.Font(None, 48)
        self.small_font = pygame.font.Font(None, 36)
        
        # Cerradura en el centro
        self.lock_image = self._create_lock_image()
        
        # Imágenes para llave
        self.key_image = self._create_key_image()

    def _create_lock_image(self):
        # Crear una superficie para la cerradura
        size = 40
        surface = pygame.Surface((size, size), pygame.SRCALPHA)
        
        # Dibujar un círculo negro para la base de la cerradura
        pygame.draw.circle(surface, (50, 50, 50), (size//2, size//2), size//2)
        # Dibujar un círculo más pequeño en el centro (el hueco de la cerradura)
        pygame.draw.circle(surface, (20, 20, 20), (size//2, size//2), size//4)
        # Dibujar una ranura debajo del círculo central
        pygame.draw.rect(surface, (20, 20, 20), (size//2 - 5, size//2, 10, size//2 - 5))
        
        return surface

    def _create_key_image(self):
        # Crear una superficie para la llave
        width, height = 20, 60
        surface = pygame.Surface((width, height), pygame.SRCALPHA)
        
        # Dibujar el mango de la llave (círculo)
        pygame.draw.circle(surface, (200, 200, 0), (width//2, height//5), width//2)
        
        # Dibujar el cuerpo de la llave (rectángulo)
        pygame.draw.rect(surface, (200, 200, 0), (width//2 - 3, height//5, 6, 2*height//3))
        
        # Dibujar los dientes de la llave
        for i in range(3):
            pygame.draw.rect(surface, (200, 200, 0), 
                            (width//2 - 3, height - 20 + i*5, 10, 3))
        
        return surface

    def dibujar(self, pantalla):
        # Fondo
        pantalla.fill((30, 30, 50))  # Fondo azul oscuro
        
        # Dibujar los anillos concéntricos
        for i, circle in enumerate(self.circles):
            radius = circle['radius']
            angle = circle['angle']
            color = circle['color']
            
            self._draw_circle_with_notch(pantalla, self.center_x, self.center_y, 
                                        radius, angle, self.notch_width, color)
        
        # Dibujar la cerradura en el centro
        lock_rect = self.lock_image.get_rect(center=(self.center_x, self.center_y))
        pantalla.blit(self.lock_image, lock_rect)
        
        # Instrucciones en la parte superior
        if not self.completado and not self.game_over:
            instruction_text = "Alinea las muescas hacia abajo para abrir la cerradura. Clica y arrastra para girar los anillos."
            instruction_surface = self.small_font.render(instruction_text, True, BLANCO)
            instruction_rect = instruction_surface.get_rect(center=(WIDTH//2, 30))
            pantalla.blit(instruction_surface, instruction_rect)
            
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
        
        # Mostrar mensaje si corresponde
        if self.show_message:
            if self.completado and not self.game_over:
                message = "¡Correcto! Has abierto la cerradura"
                color = VERDE
            elif self.game_over:
                message = "¡Se acabó el tiempo! Fallaste el puzzle"
                color = ROJO
            
            text_surface = self.font.render(message, True, color)
            text_rect = text_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2))
            
            banner_rect = text_rect.inflate(50, 20)
            banner_surface = pygame.Surface((banner_rect.width, banner_rect.height), pygame.SRCALPHA)
            banner_surface.fill((0, 0, 0, 180))
            pantalla.blit(banner_surface, banner_rect)
            
            pantalla.blit(text_surface, text_rect)
            
            # Guardar el mensaje por si se necesita para la logica del juego
            self.mensaje = message
            
        # Si el puzzle está resuelto, mostrar la animación de la llave
        if self.key_animation:
            self._draw_key_animation(pantalla)

    def _draw_circle_with_notch(self, surface, x, y, radius, notch_angle, notch_width, color):
        # Crear una superficie temporal con transparencia
        temp_surface = pygame.Surface((radius*2 + 10, radius*2 + 10), pygame.SRCALPHA)
        
        # Dibujar un anillo completo
        pygame.draw.circle(temp_surface, color, (radius + 5, radius + 5), radius, 5)
        
        # Calcular puntos para crear la muesca (usando coordenadas polares)
        notch_radius = min(radius * 0.9, radius - 20)  # La muesca no llega hasta el centro
        
        # Ángulo de inicio y fin de la muesca
        notch_half_angle = math.atan2(notch_width/2, radius)
        start_angle = notch_angle - notch_half_angle
        end_angle = notch_angle + notch_half_angle
        
        # Puntos para el polígono que "borrará" parte del anillo
        points = []
        points.append((radius + 5 + math.cos(notch_angle) * (radius + 5), 
                      radius + 5 + math.sin(notch_angle) * (radius + 5)))
        
        # Añadir puntos del arco exterior en sentido antihorario
        for angle in [start_angle, end_angle]:
            points.append((radius + 5 + math.cos(angle) * (radius + 5), 
                          radius + 5 + math.sin(angle) * (radius + 5)))
        
        # Añadir puntos del arco interior en sentido horario
        for angle in [end_angle, start_angle]:
            points.append((radius + 5 + math.cos(angle) * notch_radius, 
                          radius + 5 + math.sin(angle) * notch_radius))
        
        # "Borrar" la muesca dibujando un polígono con el color de fondo
        pygame.draw.polygon(temp_surface, (30, 30, 50), points)
        
        # Blit la superficie temporal a la superficie principal
        surface.blit(temp_surface, (x - radius - 5, y - radius - 5))

    def _draw_key_animation(self, pantalla):
        if self.key_progress < 0.8:  # La llave se mueve por la muesca
            # Distancia inicial de la llave
            outer_radius = self.circles[0]['radius'] + 200
            current_radius = outer_radius * (1 - self.key_progress / 0.8)
            
            key_x = self.center_x + math.cos(self.target_angle) * current_radius
            key_y = self.center_y + math.sin(self.target_angle) * current_radius
            
            rotated_key = pygame.transform.rotate(self.key_image, 
                                               math.degrees(-self.target_angle) - 90)
        else:  # La llave gira en el centro
            key_x = self.center_x
            key_y = self.center_y
            
            # Calcular ángulo de rotación
            rotation_progress = (self.key_progress - 0.8) / 0.2  # 0 a 1 para esta fase
            rotation_angle = math.degrees(-self.target_angle) - 90 + (rotation_progress * 180)
            
            rotated_key = pygame.transform.rotate(self.key_image, rotation_angle)
        
        # Dibujar la llave
        key_rect = rotated_key.get_rect(center=(key_x, key_y))
        pantalla.blit(rotated_key, key_rect)

    def eventos(self, mouse_click):
        if self.completado or self.game_over:
            return
            
        if self.show_message:
            self.message_timer -= 16
            if self.message_timer <= 0:
                self.show_message = False
            return
            
        mouse_pos = pygame.mouse.get_pos()
        
        if pygame.mouse.get_pressed()[0]:  # Botón izquierdo presionado
            # Calcular el ángulo actual del ratón
            dx = mouse_pos[0] - self.center_x
            dy = mouse_pos[1] - self.center_y
            current_mouse_angle = math.atan2(dy, dx)
            
            if self.selected_circle is None:
                # Verificar si se hizo clic en algún anillo
                for i, circle in enumerate(self.circles):
                    distance = math.sqrt(dx**2 + dy**2)
                    inner_radius = circle['radius'] - 10
                    outer_radius = circle['radius'] + 10
                    if inner_radius <= distance <= outer_radius:
                        self.selected_circle = i
                        self.last_mouse_angle = current_mouse_angle  # Guardar el ángulo inicial
                        break
            else:
                # Calcular la diferencia de ángulo desde el último frame
                if self.last_mouse_angle is not None:
                    # Calcular el cambio en el ángulo
                    angle_diff = current_mouse_angle - self.last_mouse_angle
                    
                    # Normalizar la diferencia de ángulo
                    if angle_diff > math.pi:
                        angle_diff -= 2 * math.pi
                    elif angle_diff < -math.pi:
                        angle_diff += 2 * math.pi
                    
                    # Actualizar el ángulo del anillo sumando la diferencia
                    self.circles[self.selected_circle]['angle'] += angle_diff
                
                self.last_mouse_angle = current_mouse_angle
                
        else:  # Botón no está presionado
            if self.selected_circle is not None:
                self.selected_circle = None
                self.last_mouse_angle = None  # Resetear el último ángulo
                self._check_puzzle_completion()

    def _check_puzzle_completion(self):
        # Verificar que todas las muescas estén alineadas con el objetivo
        all_aligned = True
        tolerance = 0.15  # Tolerancia en radianes
        
        for circle in self.circles:
            # Normalizar ángulos entre 0 y 2π
            angle = circle['angle'] % (2 * math.pi)
            target = self.target_angle % (2 * math.pi)
            
            # Verificar si están alineados con tolerancia
            angle_diff = min(abs(angle - target), abs(2 * math.pi - abs(angle - target)))
            if angle_diff > tolerance:
                all_aligned = False
                break
        
        if all_aligned:
            # Puzzle resuelto
            self.completado = True
            self.key_animation = True
            self.show_message = True
            self.message_timer = 3000  # 3 segundos
            self.solved_time = pygame.time.get_ticks()

    def update(self, tiempo):
        if self.completado and not self.game_over:
            # Actualizar la animación de la llave
            if self.key_animation:
                # La animación completa dura 2 segundos
                time_since_solved = pygame.time.get_ticks() - self.solved_time
                self.key_progress = min(1.0, time_since_solved / 2000)
        
        # Actualizar el temporizador si el juego sigue activo
        elif not self.game_over and not self.show_message:
            self.time_remaining -= tiempo * 1000  # Convertir a milisegundos
            
            if self.time_remaining <= 0:
                self.time_remaining = 0
                self.game_over = True
                self.show_message = True
            
            # Efectos para el temporizador bajo
            segundos_restantes = max(0, int(self.time_remaining / 1000))
            
            if segundos_restantes <= 15:
                self.timer_alpha = 100 + 155 * (0.5 + 0.5 * math.sin(pygame.time.get_ticks() * self.timer_pulse_speed))
            else:
                self.timer_alpha = 255
            
            # Activar el halo rojo en los últimos 10 segundos
            if segundos_restantes <= 10:
                self.red_halo_active = True
                # Hacer que el halo parpadee
                self.halo_alpha = 40 + 40 * math.sin(pygame.time.get_ticks() * 0.003)
            else:
                self.red_halo_active = False