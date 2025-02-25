import pygame
import sys

pygame.init()

#Cosntantes 
TILE_SIZE = 200
GRID_SIZE = 3
SCREEN_WIDTH = TILE_SIZE * GRID_SIZE
SCREEN_HEIGHT = TILE_SIZE * GRID_SIZE
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Creamos un fondo en negro
blank_surface = pygame.Surface((TILE_SIZE * GRID_SIZE, TILE_SIZE * GRID_SIZE))
blank_surface.fill(BLACK)

# Creamos las letras de HG (Puse 600 para que ocupen toda la pantalla, pero se pueden poner entre 400 y 600, menos no que no cubren todo)
font = pygame.font.Font(None, 600)  # Increase font size
text = font.render("HG", True, WHITE)
text_rect = text.get_rect(center=(TILE_SIZE * GRID_SIZE // 2, TILE_SIZE * GRID_SIZE // 2))
blank_surface.blit(text, text_rect)

# Orden inicial del puzzle y orden final. El inicial lo puse muy sencillo hay que buscar uno mas complicado
predefined_order = [0, 1, 2, 3, 4, 5, 6, 8, 7]
final_order = list(range(9))  

# Creamos las piezas (tiles)
tiles = []
for y in range(GRID_SIZE):
    for x in range(GRID_SIZE):
        if not (x == GRID_SIZE - 1 and y == GRID_SIZE - 1):  # Nos saltamos la última que sería el espacio en blanco
            rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
            tile = blank_surface.subsurface(rect).copy()
            pygame.draw.rect(tile, WHITE, tile.get_rect(), 5)
            tiles.append(tile)

# CCreamos la pieza "libre" (la que se puede mover)
tiles.append(pygame.Surface((TILE_SIZE, TILE_SIZE)))
tiles[-1].fill(BLACK)

# Ponemos las piezas en el orden predefinido
tiles = [tiles[i] for i in predefined_order]

# Funcion para comprabar si el puzzle esta resuelto
def is_solved():
    return predefined_order == final_order 

# Funcion para obtener el indice de la pieza en "libre"  
def get_blank_tile_index():
    return predefined_order.index(8)  

# Funcion para intercambiar dos piezas, tambien cambia sus posicion en la lista predefined_order
def swap_tiles(index1, index2):
    tiles[index1], tiles[index2] = tiles[index2], tiles[index1]
    predefined_order[index1], predefined_order[index2] = predefined_order[index2], predefined_order[index1]

# Funcion para manejar el movimiento de las piezas
def handle_tile_movement(pos):
    blank_index = get_blank_tile_index()
    blank_x = (blank_index % GRID_SIZE) * TILE_SIZE
    blank_y = (blank_index // GRID_SIZE) * TILE_SIZE

    for i, tile in enumerate(tiles):
        x = (i % GRID_SIZE) * TILE_SIZE
        y = (i // GRID_SIZE) * TILE_SIZE
        rect = pygame.Rect(x, y, TILE_SIZE, TILE_SIZE)
        if rect.collidepoint(pos):
            if (abs(blank_x - x) == TILE_SIZE and blank_y == y) or (abs(blank_y - y) == TILE_SIZE and blank_x == x):
                swap_tiles(i, blank_index)
                break

# Creamos la ventana
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Govern of IronRidge')


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            handle_tile_movement(event.pos)

    screen.fill(BLACK)

    # Dibujamos las piezas
    for i, tile in enumerate(tiles):
        x = (i % GRID_SIZE) * TILE_SIZE
        y = (i // GRID_SIZE) * TILE_SIZE
        screen.blit(tile, (x, y))

    # Actualizamos
    pygame.display.flip()

    # Miramos si esta resuelto
    if is_solved():
        print("¡Puzzle resuelto!")
        pygame.time.wait(3000)  # Espera 3 segundos
        running = False

pygame.quit()
sys.exit()
