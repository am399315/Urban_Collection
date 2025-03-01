# Andrés Miguel Escolastico Lara 23-EISN-2-056
import pygame
import random

# Configuración básica
ANCHO, ALTO = 800, 600
TAM_CELDA = 40
FILAS, COLUMNAS = ALTO // TAM_CELDA, ANCHO // TAM_CELDA  # Ajuste para que el laberinto ocupe toda la pantalla

# Definir colores
NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)
GRIS = (155, 155, 155)
AMARILLO = (255, 255, 0)
ROJO = (255, 0, 0)
VERDE = (0, 255, 0)
NARANJA = (255, 140, 0)

# Andrés Miguel Escolastico Lara 23-EISN-2-056

# Crear el laberinto
laberinto = [[1] * COLUMNAS for _ in range(FILAS)]

# Direcciones posibles para moverse (arriba, abajo, izquierda, derecha)
DIRECCIONES = [(-2, 0), (2, 0), (0, -2), (0, 2)]

# Andrés Miguel Escolastico Lara 23-EISN-2-056

# Función para generar el laberinto usando DFS
def generar_laberinto(fila, columna):
    laberinto[fila][columna] = 0  # Marcar la celda como camino
    random.shuffle(DIRECCIONES)  # Mezclar direcciones
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

# Crear lista de monedas recolectables (solo en celdas accesibles dentro del área jugable)
monedas = []
for fila in range(FILAS):
    for columna in range(COLUMNAS):
        if laberinto[fila][columna] == 0 and random.random() < 0.02:  # Probabilidad de generar monedas solo en caminos libres
            monedas.append((columna * TAM_CELDA + TAM_CELDA // 4, fila * TAM_CELDA + TAM_CELDA // 4))

# Crear monedas rojas que recargan gasolina
monedas_rojas = []
for _ in range(2):
    fila, columna = random.randint(1, FILAS - 1), random.randint(1, COLUMNAS - 1)
    while laberinto[fila][columna] == 1 or (fila * TAM_CELDA, columna * TAM_CELDA) in monedas_rojas:  # Verificar que la celda sea libre
        fila, columna = random.randint(1, FILAS - 1), random.randint(1, COLUMNAS - 1)
    monedas_rojas.append((columna * TAM_CELDA + TAM_CELDA // 4, fila * TAM_CELDA + TAM_CELDA // 4))

# Andrés Miguel Escolastico Lara 23-EISN-2-056

# Medidor de gasolina
gasolina = 100  # 100% de gasolina
reducir_gasolina = 0.05  # Descontar un 0.05% por cada ciclo

# Fuente de texto para mostrar información
fuente = pygame.font.SysFont('Arial', 30)

# Andrés Miguel Escolastico Lara 23-EISN-2-056

# Bucle principal
jugando = True
while jugando:
    pantalla.fill(NEGRO)
    
    # Dibujar laberinto
    for fila in range(FILAS):
        for columna in range(COLUMNAS):
            # Dibujar bordes en verde
            if fila == 0 or columna == 0 or fila == FILAS - 1 or columna == COLUMNAS - 1:
                pygame.draw.rect(pantalla, NARANJA, (columna * TAM_CELDA, fila * TAM_CELDA, TAM_CELDA, TAM_CELDA))
            elif laberinto[fila][columna] == 1:
                pygame.draw.rect(pantalla, GRIS, (columna * TAM_CELDA, fila * TAM_CELDA, TAM_CELDA, TAM_CELDA))

    # Andrés Miguel Escolastico Lara 23-EISN-2-056

    # Dibujar monedas recolectables
    for moneda in monedas[:]:
        pygame.draw.circle(pantalla, AMARILLO, moneda, TAM_CELDA // 6)

    # Dibujar monedas rojas que recargan gasolina
    for moneda_roja in monedas_rojas[:]:
        pygame.draw.circle(pantalla, ROJO, moneda_roja, TAM_CELDA // 6)

    # Andrés Miguel Escolastico Lara 23-EISN-2-056

    # Dibujar jugador
    pygame.draw.rect(pantalla, BLANCO, (pos_x, pos_y, jugador_ancho, jugador_alto))  # Ajustar la posición del jugador
    
    # Mostrar contador de monedas
    texto_monedas = fuente.render(f'Monedas restantes: {len(monedas)}', True, NEGRO )
    pantalla.blit(texto_monedas, (10, 0))
    
    # Andrés Miguel Escolastico Lara 23-EISN-2-056

    # Mostrar medidor de gasolina en la esquina superior derecha
    pygame.draw.rect(pantalla, ROJO, (ANCHO - 210, 10, 200, 20))  # Fondo del medidor de gasolina
    pygame.draw.rect(pantalla, VERDE, (ANCHO - 210, 10, 2 * gasolina, 20))  # Medidor de gasolina
    
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

    # Verificar si el jugador ha recolectado alguna moneda
    monedas = [m for m in monedas if not (abs(m[0] - pos_x) < TAM_CELDA // 2 and abs(m[1] - pos_y) < TAM_CELDA // 2)]
    
    # Verificar si el jugador ha recolectado alguna moneda roja (que recarga gasolina)
    for moneda_roja in monedas_rojas[:]:
        if abs(moneda_roja[0] - pos_x) < TAM_CELDA // 2 and abs(moneda_roja[1] - pos_y) < TAM_CELDA // 2:
            gasolina = min(100, gasolina + 100)  # Recargar gasolina al recolectar
            monedas_rojas.remove(moneda_roja)

    # Andrés Miguel Escolastico Lara 23-EISN-2-056

    # Comprobar si todos los monedas fueron recolectados
    if not monedas:
        print("¡Has ganado!")
        jugando = False
    
    # Reducir gasolina
    gasolina -= reducir_gasolina
    if gasolina <= 0:
        print("¡Te has quedado sin gasolina! Has perdido.")
        jugando = False
    
    pygame.display.flip()
    pygame.time.delay(30)

pygame.quit()
# Andrés Miguel Escolastico Lara 23-EISN-2-056