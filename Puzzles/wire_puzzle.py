import pygame
from settings import *

class WirePuzzle:
    def __init__(self):
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
                color_texto = BLANCO  # Cambiamos el color del texto a BLANCO
            else:  # Para "¡Has fallado! La alarma se ha activado"
                banda.fill(ROJO)
                color_texto = BLANCO  # Cambiamos el color del texto a BLANCO
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
            
        # Dibujar intentos restantes en la esquina superior derecha
        texto_intentos = self.font.render(f"Intentos: {self.intentos}", True, BLANCO)
        texto_intentos_rect = texto_intentos.get_rect()
        texto_intentos_rect.right = WIDTH - 20  # 20 píxeles de margen
        texto_intentos_rect.top = 20  # 20 píxeles desde arriba
        pantalla.blit(texto_intentos, texto_intentos_rect)

    def eventos(self, mouse_click):
        if mouse_click and not self.completado and self.intentos > 0:
            mouse_pos = pygame.mouse.get_pos()
            
            # Verificar si se hizo clic en algún cable
            for i in range(4):
                if i not in self.cables_cortados:  # Solo verifica los cables que no han sido cortados
                    y = self.start_y + (i * self.spacing)
                    cable_rect = pygame.Rect(self.start_x, y, self.wire_width, self.wire_height)
                    
                    if cable_rect.collidepoint(mouse_pos):
                        if i == self.wire_correcto:
                            self.mensaje = "¡Correcto! Has desactivado la cámara"
                            self.completado = True
                        else:
                            self.cables_cortados.append(i)  # Añade el cable a la lista de cortados
                            self.intentos -= 1
                            if self.intentos > 0:
                                self.mensaje = f"Cable incorrecto. Te quedan {self.intentos} intentos"
                            else:
                                self.mensaje = "¡Has fallado! La alarma se ha activado"
                                self.completado = True
                        break

    def update(self, tiempo):
        # Lógica de actualización si es necesaria
        pass