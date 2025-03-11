import pygame
import math
import random
from settings import *
from escena import Escena

class DoorLockPuzzle(Escena):
    def __init__(self, director):
        
        Escena.__init__(self, director)
        
        # Configuración general del puzzle
        self.center_x = WIDTH // 2
        self.center_y = HEIGHT // 2
        
        # Cargar imágenes
        self.background_image = pygame.image.load("resources/images/puzzles/lock_background.jpeg")
        # Guardar dimensiones originales antes de escalar
        self.original_bg_width = self.background_image.get_width()
        self.original_bg_height = self.background_image.get_height()
        
        # Escalar el fondo para que se ajuste a la pantalla
        self.background_image = pygame.transform.scale(self.background_image, (WIDTH, HEIGHT))
        
        # Calcular factor de escala entre la imagen original y la escalada
        self.scale_x = WIDTH / self.original_bg_width
        self.scale_y = HEIGHT / self.original_bg_height
        
        # Cargar imagen del perno y mantener la original antes de escalar
        self.perno_original = pygame.image.load("resources/images/puzzles/perno.png")
        
        self.original_pin_width = self.perno_original.get_width()
        self.original_pin_height = self.perno_original.get_height()
        
        # Escalar el perno según los mismos factores que el fondo
        self.pin_width = int(self.original_pin_width * self.scale_x)
        self.pin_height = int(self.original_pin_height * self.scale_y)
        
        # Si el perno es muy pequeño, establecemos un tamaño mínimo
        if self.pin_width < 25:
            self.pin_width = 25
        if self.pin_height < 80:
            self.pin_height = 80
            
        # Escalar la imagen del perno
        self.perno_image = pygame.transform.scale(self.perno_original, (self.pin_width, self.pin_height))
        
        # Coordenadas específicas para los pernos (en la imagen original)
        self.original_pin_coords = [(181, 93), (207, 93), (232, 93), (258, 93), (284, 93)]
        
        # Configuración de los pernos
        self.num_pins = len(self.original_pin_coords)
        
        # Marca de posición correcta
        self.mark_height = max(3, int(3 * self.scale_y))  # Escalamos también la marca
        
        # Información de los pernos
        self.pins = []
        for i in range(self.num_pins):
            # Escalar las coordenadas originales al tamaño actual de la pantalla
            pin_x = int(self.original_pin_coords[i][0] * self.scale_x)
            pin_y = int(self.original_pin_coords[i][1] * self.scale_y)
            
            # La posición correcta varía para cada perno (entre 20% y 70% de la altura)
            correct_position = random.randint(int(self.pin_height * 0.2), int(self.pin_height * 0.7))
            
            self.pins.append({
                'x': pin_x,
                'y': pin_y + self.pin_height,  # Posición base del perno (abajo del todo)
                'height': self.pin_height,
                'current_position': 0,  # Posición actual (0 = abajo, pin_height = arriba)
                'correct_position': correct_position,  # Posición correcta para este perno
                'color': (180, 180, 180),
                'mark_color': (220, 160, 40),
                'selected': False
            })
        
        # Herramienta de ganzúa
        self.lockpick = {
            'width': int(16 * self.scale_x),
            'height': int(4 * self.scale_y),
            'x': 0,
            'y': 0,
            'color': (100, 100, 100),
            'tip_color': (220, 220, 220)
        }
        
        # Estado del puzzle
        self.time_remaining = 20000
        self.completado = False
        self.game_over = False
        self.show_message = False
        self.message_timer = 0
        self.mensaje = ""
        self.solved_time = 0
        
        # Efectos visuales
        self.timer_alpha = 255
        self.timer_pulse_speed = 0.005
        self.red_halo_active = False
        self.halo_alpha = 0
        self.halo_max_alpha = 100
        
        # Fuentes
        self.font = pygame.font.Font(None, 48)
        self.small_font = pygame.font.Font(None, 36)
        
        # Animación
        self.animation_active = False
        self.animation_progress = 0

    def dibujar(self, pantalla):
        # Dibujar la imagen de fondo
        pantalla.blit(self.background_image, (0, 0))
        
        # Dibujar las marcas de posición correcta para cada perno
        for pin in self.pins:
            # Dibujar la marca de posición correcta
            mark_y = pin['y'] - pin['correct_position']
            pygame.draw.rect(pantalla, pin['mark_color'], 
                           (pin['x'] - 3, mark_y - self.mark_height // 2, 
                            self.pin_width + 6, self.mark_height))
        
        # Dibujar los pernos
        for pin in self.pins:
            # Color de selección si está seleccionado
            if pin['selected']:
                highlight_surface = pygame.Surface((self.pin_width, self.pin_height), pygame.SRCALPHA)
                highlight_surface.fill((255, 255, 0, 100))
                pantalla.blit(highlight_surface, (pin['x'], pin['y'] - pin['current_position'] - self.pin_height))
            
            # Dibujar la imagen del perno en su posición actual
            pantalla.blit(self.perno_image, 
                         (pin['x'], pin['y'] - pin['current_position'] - self.pin_height))
        
        # Dibujar la ganzúa
        mouse_pos = pygame.mouse.get_pos()
        self.lockpick['x'] = mouse_pos[0] - self.lockpick['width'] // 2
        self.lockpick['y'] = mouse_pos[1] - 5
        
        # Cuerpo de la ganzúa
        pygame.draw.rect(pantalla, self.lockpick['color'], 
                       (self.lockpick['x'], self.lockpick['y'], 
                        self.lockpick['width'], self.lockpick['height']))
        
        # Punta de la ganzúa
        tip_width = max(2.5, int(5 * self.scale_x))
        tip_height = self.lockpick['height'] + int(4 * self.scale_y)
        pygame.draw.rect(pantalla, self.lockpick['tip_color'], 
                       (self.lockpick['x'] - tip_width//2, self.lockpick['y'] - 3,
                        tip_width, tip_height))
        
        # Instrucciones en la parte superior
        if not self.completado and not self.game_over:
            instruction_text = "Usa la ganzúa para mover los pernos a la altura marcada. Haz clic para hacer palanca."
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
            
            # Guardar el mensaje por si se necesita para la lógica del juego
            self.mensaje = message

    def eventos(self, lista_eventos):
        if self.completado or self.game_over:
            return
                
        if self.show_message:
            self.message_timer -= 16
            if self.message_timer <= 0:
                self.show_message = False
            return
        
        mouse_pos = pygame.mouse.get_pos()
        mouse_click = False
        
        # Procesar eventos
        for evento in lista_eventos:
            if evento.type == pygame.MOUSEBUTTONDOWN:
                mouse_click = True
        
        # Desmarcar todos los pernos
        for pin in self.pins:
            pin['selected'] = False
        
        # Verificar si la ganzúa está sobre algún perno
        for i, pin in enumerate(self.pins):
            pin_rect = pygame.Rect(pin['x'], pin['y'] - pin['current_position'] - self.pin_height, 
                                self.pin_width, self.pin_height)
            
            # Verificar si la punta de la ganzúa está tocando este perno
            tip_width = max(5, int(5 * self.scale_x))
            tip_height = self.lockpick['height'] + int(4 * self.scale_y)
            lockpick_tip_rect = pygame.Rect(self.lockpick['x'] - tip_width//2, 
                                        self.lockpick['y'] - 3, 
                                        tip_width, tip_height)
            
            if pin_rect.colliderect(lockpick_tip_rect):
                # Marcar este perno como seleccionado
                pin['selected'] = True
                
                # Si se hace clic, mover el perno
                if mouse_click:
                    # Calcular cuánto mover el perno (depende de dónde se haga clic)
                    click_y = mouse_pos[1]
                    pin_top_y = pin['y'] - pin['current_position'] - self.pin_height
                    
                    # Si el clic está en la parte superior del perno, lo empujamos hacia arriba
                    # Si está en la parte inferior, lo empujamos menos
                    click_position = 1.0 - (click_y - pin_top_y) / pin['height']
                    move_amount = 5 + int(15 * click_position)  # Entre 5 y 20 píxeles
                    
                    # Aplicar escala al movimiento
                    move_amount = int(move_amount * self.scale_y)
                    
                    # Limitar el movimiento al rango válido
                    pin['current_position'] = min(pin['height'], 
                                                pin['current_position'] + move_amount)
                    
                    # Verificar si este perno está en la posición correcta
                    self._check_pin_position(i)
        
        # Verificar si todos los pernos están en posición correcta
        if mouse_click:
            self._check_puzzle_completion()

    def _check_pin_position(self, pin_index):
        pin = self.pins[pin_index]
        # Un perno está en posición correcta si está dentro de un rango de tolerancia
        tolerance = int(5 * self.scale_y)  # Escalar la tolerancia
        
        if abs(pin['current_position'] - pin['correct_position']) <= tolerance:
            # Ajustar exactamente a la posición correcta
            pin['current_position'] = pin['correct_position']
            # Cambiar color para dar feedback (esto se reflejará en un efecto visual)
            pin['color'] = (100, 200, 100)
        else:
            # Si no está en posición correcta, mantener color normal
            pin['color'] = (180, 180, 180)

    def _check_puzzle_completion(self):
        # Verificar si todos los pernos están en la posición correcta
        all_correct = True
        tolerance = int(5 * self.scale_y)  # Escalar la tolerancia
        
        for pin in self.pins:
            if abs(pin['current_position'] - pin['correct_position']) > tolerance:
                all_correct = False
                break
        
        if all_correct:
            # Puzzle resuelto
            self.completado = True
            self.animation_active = True
            self.show_message = True
            self.message_timer = 3000  # 3 segundos
            self.solved_time = pygame.time.get_ticks()

    def update(self, tiempo):
        if self.completado and not self.game_over:
            # Actualizar animación si está activa
            if self.animation_active:
                time_since_solved = pygame.time.get_ticks() - self.solved_time
                self.animation_progress = min(1.0, time_since_solved / 2000)
                
                # Efecto de pernos que bajan juntos
                if self.animation_progress > 0.3:
                    drop_factor = (self.animation_progress - 0.3) / 0.7
                    for pin in self.pins:
                        pin['current_position'] = pin['correct_position'] * (1 - drop_factor)
                    if drop_factor >= 1.0:  # Cuando la animación termina
                        self.director.salirEscena()
        
        # Actualizar el temporizador si el juego sigue activo
        elif not self.game_over and not self.show_message:
            self.time_remaining -= tiempo  # Convertir a milisegundos
            
            if self.time_remaining <= 0:
                self.time_remaining = 0
                self.game_over = True
                self.show_message = True
                self.director.salirEscena()
            
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
                
        # Añadir efecto de gravedad - los pernos bajan lentamente cuando no se interactúa con ellos
        if not self.completado and not self.game_over:
            for pin in self.pins:
                if not pin['selected'] and pin['current_position'] > 0:
                    # Si el perno no está seleccionado y no está en el fondo, aplicar gravedad
                    gravity_factor = 0.5 * self.scale_y  # Escalar también la gravedad
                    pin['current_position'] = max(0, pin['current_position'] - gravity_factor)
                    # Verificar si el perno sigue estando en posición correcta después de aplicar gravedad
                    tolerance = int(5 * self.scale_y)
                    if abs(pin['current_position'] - pin['correct_position']) <= tolerance:
                        pin['current_position'] = pin['correct_position']
                        pin['color'] = (100, 200, 100)
                    else:
                        pin['color'] = (180, 180, 180)