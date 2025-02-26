# Andrés Miguel Escolastico Lara 23-EISN-2-056
import pygame
import random

# Configuración básica
ANCHO, ALTO = 1200, 900
TAM_CELDA = 40
FILAS, COLUMNAS = ALTO // TAM_CELDA, ANCHO // TAM_CELDA

# Andrés Miguel Escolastico Lara 23-EISN-2-056

# Definir colores
NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)
AZUL = (0, 0, 255)
AMARILLO = (255, 255, 0)

# Crear un laberinto lleno de paredes
laberinto = [[1] * COLUMNAS for _ in range(FILAS)]

# Andrés Miguel Escolastico Lara 23-EISN-2-056

# Direcciones posibles para moverse (arriba, abajo, izquierda, derecha)
DIRECCIONES = [(-2, 0), (2, 0), (0, -2), (0, 2)]

# Función para generar el laberinto usando DFS
def generar_laberinto(fila, columna):
    laberinto[fila][columna] = 0  # Marcar la celda como camino
    random.shuffle(DIRECCIONES)  # Mezclar direcciones

# Andrés Miguel Escolastico Lara 23-EISN-2-056

    for df, dc in DIRECCIONES:
        nueva_fila, nueva_columna = fila + df, columna + dc
        if 1 <= nueva_fila < FILAS - 1 and 1 <= nueva_columna < COLUMNAS - 1 and laberinto[nueva_fila][nueva_columna] == 1:
            laberinto[fila + df // 2][columna + dc // 2] = 0  # Abrir paso
            laberinto[nueva_fila][nueva_columna] = 0  # Hacer la nueva celda un camino
            if random.random() < 0.4:  # Probabilidad de ensanchar el camino
                if df == 0:  # Horizontal
                    if 1 <= fila - 1 < FILAS - 1:
                        laberinto[fila - 1][columna] = 0
                    if 1 <= fila + 1 < FILAS - 1:
                        laberinto[fila + 1][columna] = 0
                else:  # Vertical
                    if 1 <= columna - 1 < COLUMNAS - 1:
                        laberinto[fila][columna - 1] = 0
                    if 1 <= columna + 1 < COLUMNAS - 1:
                        laberinto[fila][columna + 1] = 0
            generar_laberinto(nueva_fila, nueva_columna)

# Iniciar la generación del laberinto
generar_laberinto(1, 1)

# Andrés Miguel Escolastico Lara 23-EISN-2-056

# Inicializar Pygame
pygame.init()
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Urban Collection")

# Posicionar al jugador en el centro o en la celda libre más cercana
centro_fila, centro_columna = FILAS // 2, COLUMNAS // 2
while laberinto[centro_fila][centro_columna] == 1:
    centro_fila -= 1  # Buscar celda libre

# Andrés Miguel Escolastico Lara 23-EISN-2-056

# Tamaño del jugador ajustado
jugador_ancho = TAM_CELDA // 2
jugador_alto = TAM_CELDA // 2
pos_x = centro_columna * TAM_CELDA + (TAM_CELDA - jugador_ancho) // 2
pos_y = centro_fila * TAM_CELDA + (TAM_CELDA - jugador_alto) // 2
velocidad = 5

# Función para verificar colisiones con paredes correctamente
def puede_moverse(x, y):
    esquinas = [
        (x, y),
        (x + jugador_ancho - 1, y),
        (x, y + jugador_alto - 1),
        (x + jugador_ancho - 1, y + jugador_alto - 1)
    ]
    for ex, ey in esquinas:
        fila, columna = ey // TAM_CELDA, ex // TAM_CELDA
        if not (0 <= fila < FILAS and 0 <= columna < COLUMNAS) or laberinto[fila][columna] == 1:
            return False
    return True

# Andrés Miguel Escolastico Lara 23-EISN-2-056

# Crear lista de puntos recolectables
puntos = []
for fila in range(FILAS):
    for columna in range(COLUMNAS):
        if laberinto[fila][columna] == 0 and random.random() < 0.02:  # Probabilidad de generar puntos
            puntos.append((columna * TAM_CELDA + TAM_CELDA // 4, fila * TAM_CELDA + TAM_CELDA // 4))

# Bucle principal
jugando = True
while jugando:
    pantalla.fill(NEGRO)
    
    # Dibujar laberinto
    for fila in range(FILAS):
        for columna in range(COLUMNAS):
            if laberinto[fila][columna] == 1:
                pygame.draw.rect(pantalla, AZUL, (columna * TAM_CELDA, fila * TAM_CELDA, TAM_CELDA, TAM_CELDA))
    
    # Andrés Miguel Escolastico Lara 23-EISN-2-056
    
    # Dibujar puntos recolectables
    for punto in puntos[:]:
        pygame.draw.circle(pantalla, AMARILLO, punto, TAM_CELDA // 6)
    
    # Dibujar jugador
    pygame.draw.rect(pantalla, BLANCO, (pos_x, pos_y, jugador_ancho, jugador_alto))
    
    # Manejo de eventos
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            jugando = False

# Andrés Miguel Escolastico Lara 23-EISN-2-056

    # Movimiento del jugador
    keys = pygame.key.get_pressed()
    nueva_x, nueva_y = pos_x, pos_y
    
    if keys[pygame.K_UP]:
        nueva_y -= velocidad
    if keys[pygame.K_DOWN]:
        nueva_y += velocidad
    if keys[pygame.K_LEFT]:
        nueva_x -= velocidad
    if keys[pygame.K_RIGHT]:
        nueva_x += velocidad
    
    # Verificar si el movimiento es válido
    if puede_moverse(nueva_x, nueva_y):
        pos_x, pos_y = nueva_x, nueva_y
    
    # Andrés Miguel Escolastico Lara 23-EISN-2-056
    
    # Verificar si el jugador ha recolectado algún punto
    puntos = [p for p in puntos if not (abs(p[0] - pos_x) < TAM_CELDA // 2 and abs(p[1] - pos_y) < TAM_CELDA // 2)]
    
    # Comprobar si todos los puntos fueron recolectados
    if not puntos:
        print("¡Has ganado!")
        jugando = False
    
    pygame.display.flip()
    pygame.time.delay(30)

pygame.quit()
# Andrés Miguel Escolastico Lara 23-EISN-2-056