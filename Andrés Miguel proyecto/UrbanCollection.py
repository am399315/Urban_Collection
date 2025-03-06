# Andrés Miguel Escolastico Lara 23-EISN-2-056
import pygame
import random

# Configuración básica
ANCHO, ALTO = 800, 600
TAM_CELDA = 40
FILAS, COLUMNAS = ALTO // TAM_CELDA, ANCHO // TAM_CELDA  # Ajuste para que el laberinto ocupe toda la pantalla

# Andrés Miguel Escolastico Lara 23-EISN-2-056

# Definir colores
NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)
GRIS = (155, 155, 155)
AMARILLO = (255, 255, 0)
ROJO = (255, 0, 0)
VERDE = (0, 255, 0)
NARANJA = (255, 140, 0)

# Variables del jugador
jugador_ancho = TAM_CELDA // 2
jugador_alto = TAM_CELDA // 2

# Andrés Miguel Escolastico Lara 23-EISN-2-056

# Variable de ronda
ronda = 1

# Variables los de enemigos
enemigos = []
enemigos_muertos = 0
enemigo_ancho = jugador_ancho
enemigo_alto = jugador_alto

# Andrés Miguel Escolastico Lara 23-EISN-2-056

# Crear el laberinto
laberinto = [[1] * COLUMNAS for _ in range(FILAS)] 

# Direcciones posibles para moverse (arriba, abajo, izquierda, derecha)
DIRECCIONES = [(-2, 0), (2, 0), (0, -2), (0, 2)]

# Andrés Miguel Escolastico Lara 23-EISN-2-056

# Función para generar al jugador
def generar_jugador():
    fila, columna = random.randint(1, FILAS - 1), random.randint(1, COLUMNAS - 1)
    while laberinto[fila][columna] == 1:  # Buscar una posición libre
        fila, columna = random.randint(1, FILAS - 1), random.randint(1, COLUMNAS - 1)
    return columna * TAM_CELDA + (TAM_CELDA - jugador_ancho) // 2, fila * TAM_CELDA + (TAM_CELDA - jugador_alto) // 2

# Función para generar las monedas en cada ronda
def generar_monedas():
    global monedas
    monedas = []  # Limpiar las monedas anteriores

    # Generar nuevas monedas en lugares aleatorios del laberinto
    for _ in range(10):
        fila = random.randint(1, FILAS - 2)
        columna = random.randint(1, COLUMNAS - 2)
        while laberinto[fila][columna] == 1:  # Asegurarse de que la moneda no esté en una pared
            fila = random.randint(1, FILAS - 2)
            columna = random.randint(1, COLUMNAS - 2)
        monedas.append((columna * TAM_CELDA + TAM_CELDA // 2, fila * TAM_CELDA + TAM_CELDA // 2))

# Andrés Miguel Escolastico Lara 23-EISN-2-056

# Función para generar las monedas rojas (en todas las rondas)
def generar_monedas_rojas():
    global monedas_rojas
    monedas_rojas.clear()  # Limpiar las monedas rojas anteriores
    for _ in range(2):  # Generar 2 monedas rojas en cada ronda
        fila, columna = random.randint(1, FILAS - 1), random.randint(1, COLUMNAS - 1)
        while laberinto[fila][columna] == 1 or (fila * TAM_CELDA, columna * TAM_CELDA) in monedas_rojas:
            fila, columna = random.randint(1, FILAS - 1), random.randint(1, COLUMNAS - 1)
        monedas_rojas.append((columna * TAM_CELDA + TAM_CELDA // 4, fila * TAM_CELDA + TAM_CELDA // 4))

# Función para generar a los enemigos
def generar_enemigo():
    fila, columna = random.randint(1, FILAS - 1), random.randint(1, COLUMNAS - 1)
    while laberinto[fila][columna] == 1 or any(abs(enemigo[0] - columna * TAM_CELDA) < TAM_CELDA and abs(enemigo[1] - fila * TAM_CELDA) < TAM_CELDA for enemigo in enemigos):
        fila, columna = random.randint(1, FILAS - 1), random.randint(1, COLUMNAS - 1)
    enemigo_x = columna * TAM_CELDA + TAM_CELDA // 4
    enemigo_y = fila * TAM_CELDA + TAM_CELDA // 4
    enemigos.append([enemigo_x, enemigo_y])  # Guardamos la posición como lista para facilitar la actualización

# Andrés Miguel Escolastico Lara 23-EISN-2-056

# Función para mover los enemigos
def mover_enemigos():
    for i, (enemigo_x, enemigo_y) in enumerate(enemigos[:]):
        # Movimiento más fluido (pequeños pasos)
        direccion = random.choice([(-1, 0), (1, 0), (0, -1), (0, 1)])  # Movimiento en 4 direcciones
        nuevo_x = enemigo_x + direccion[0]
        nuevo_y = enemigo_y + direccion[1]

        if puede_moverse(nuevo_x, nuevo_y):  # Verificar si el movimiento es válido
            enemigos[i] = [nuevo_x, nuevo_y]

# Función para dibujar los enemigos
def dibujar_enemigos():
    for enemigo_x, enemigo_y in enemigos:
        pygame.draw.rect(pantalla, ROJO, (enemigo_x, enemigo_y, enemigo_ancho, enemigo_alto))

# Andrés Miguel Escolastico Lara 23-EISN-2-056

# Función para verificar si el jugador ha chocado con algún enemigo
def verificar_colision_con_enemigos():
    global pos_x, pos_y, jugador_ancho, jugador_alto
    for enemigo_x, enemigo_y in enemigos:
        if abs(enemigo_x - pos_x) < jugador_ancho and abs(enemigo_y - pos_y) < jugador_alto:
            return True  # El jugador colisionó con un enemigo
    return False

# Función para generar los enemigos en posiciones aleatorias fuera de las paredes
def generar_enemigos_en_ronda():
    enemigos.clear()  # Limpiar lista de enemigos al iniciar una nueva ronda
    for _ in range(ronda):  # Aumentar la cantidad de enemigos por ronda
        generar_enemigo()

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

# Crear lista de monedas recolectables
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

# Iniciar el juego con los enemigos en la primera ronda
generar_enemigos_en_ronda()

# Fuente de texto para mostrar información
fuente = pygame.font.SysFont('Arial', 30)

# Andrés Miguel Escolastico Lara 23-EISN-2-056

# Bucle principal
jugando = True
while jugando:
    pantalla.fill(NEGRO)

    # Verificar si el jugador ha recolectado alguna moneda amarilla
    for moneda in monedas[:]:
        if abs(moneda[0] - pos_x) < TAM_CELDA // 2 and abs(moneda[1] - pos_y) < TAM_CELDA // 2:
            monedas.remove(moneda)

    # Comprobar si todas las monedas han sido recolectadas
    if not monedas:
        ronda += 1  # Subir de ronda
        print(f"¡Has completado la ronda {ronda - 1}!")
        monedas_rojas.clear()
        gasolina = 100  # Recargar gasolina
        enemigos.clear()  # Reiniciar enemigos
        generar_monedas()  # Regenerar las monedas amarillas
        generar_monedas_rojas()  # Regenerar monedas rojas en todas las rondas
        pygame.time.delay(2000)  # Pausa entre rondas
        generar_enemigos_en_ronda()  # Generar enemigos

    # Andrés Miguel Escolastico Lara 23-EISN-2-056

    # Resto del código (dibujar laberinto, jugador, enemigos, etc.)
    # Dibujar laberinto
    for fila in range(FILAS):
        for columna in range(COLUMNAS):
            if fila == 0 or columna == 0 or fila == FILAS - 1 or columna == COLUMNAS - 1:
                pygame.draw.rect(pantalla, NARANJA, (columna * TAM_CELDA, fila * TAM_CELDA, TAM_CELDA, TAM_CELDA))
            elif laberinto[fila][columna] == 1:
                pygame.draw.rect(pantalla, GRIS, (columna * TAM_CELDA, fila * TAM_CELDA, TAM_CELDA, TAM_CELDA))

    # Dibujar monedas amarillas
    for moneda in monedas[:]:
        pygame.draw.circle(pantalla, AMARILLO, moneda, TAM_CELDA // 6)

    # Andrés Miguel Escolastico Lara 23-EISN-2-056

    # Dibujar monedas rojas
    for moneda_roja in monedas_rojas[:]:
        pygame.draw.circle(pantalla, ROJO, moneda_roja, TAM_CELDA // 6)

    # Dibujar jugador
    pygame.draw.rect(pantalla, BLANCO, (pos_x, pos_y, jugador_ancho, jugador_alto))

    # Andrés Miguel Escolastico Lara 23-EISN-2-056

    # Mostrar contador de monedas
    texto_monedas = fuente.render(f'Monedas restantes: {len(monedas)}', True, NEGRO)
    pantalla.blit(texto_monedas, (10, 0))

    # Mostrar medidor de gasolina
    pygame.draw.rect(pantalla, ROJO, (ANCHO - 210, 10, 200, 20))  # Fondo del medidor de gasolina
    pygame.draw.rect(pantalla, VERDE, (ANCHO - 210, 10, 2 * gasolina, 20))  # Medidor de gasolina

    # Mostrar ronda actual
    texto_ronda = fuente.render(f'Ronda: {ronda}', True, NEGRO)
    pantalla.blit(texto_ronda, (ANCHO - 150, 0))

    # Andrés Miguel Escolastico Lara 23-EISN-2-056

    # Dibujar enemigos en pantalla
    dibujar_enemigos()

    # Mover los enemigos
    mover_enemigos()

    # Verificar colisiones con enemigos
    if verificar_colision_con_enemigos():
        print("¡Te has chocado con un enemigo! Has perdido.")
        jugando = False

    # Andrés Miguel Escolastico Lara 23-EISN-2-056

    # Manejo de eventos
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            jugando = False

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

    # Andrés Miguel Escolastico Lara 23-EISN-2-056

    # Verificar si el movimiento es válido
    if puede_moverse(nueva_x, nueva_y):
        pos_x, pos_y = nueva_x, nueva_y

    # Verificar si el jugador ha recolectado alguna moneda roja
    for moneda_roja in monedas_rojas[:]:
        if abs(moneda_roja[0] - pos_x) < TAM_CELDA // 2 and abs(moneda_roja[1] - pos_y) < TAM_CELDA // 2:
            gasolina = min(100, gasolina + 100)  # Recargar gasolina al recolectar
            monedas_rojas.remove(moneda_roja)

    # Andrés Miguel Escolastico Lara 23-EISN-2-056

    # Reducir gasolina
    gasolina -= reducir_gasolina
    if gasolina <= 0:
        print("¡Te has quedado sin gasolina! Has perdido.")
        jugando = False

    pygame.display.flip()
    pygame.time.delay(30)

pygame.quit()
# Andrés Miguel Escolastico Lara 23-EISN-2-056
