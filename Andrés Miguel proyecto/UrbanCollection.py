# Andrés Miguel Escolastico Lara 23-EISN-2-056
import pygame
import random
import heapq
import time

# Configuración básica
ANCHO, ALTO = 800, 600
TAM_CELDA = 40
FILAS, COLUMNAS = ALTO // TAM_CELDA, ANCHO // TAM_CELDA

# Andrés Miguel Escolastico Lara 23-EISN-2-056

# Definir colores
NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)
GRIS = (155, 155, 155)
GRIS_OSCURO = (35, 35, 35)
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
MAX_RONDAS = 5  # Límite de rondas

# Variables de enemigos
enemigos = []
enemigos_muertos = 0
enemigo_ancho = jugador_ancho
enemigo_alto = jugador_alto
ultimo_movimiento_enemigos = time.time()
intervalo_movimiento = 0.75  # Los enemigos se moverán cada 0.75 segundos

# Andrés Miguel Escolastico Lara 23-EISN-2-056

# Variables para el humo
humo_activo = False
humo_x, humo_y = -100, -100  # Posición inicial fuera de la pantalla
humo_duracion = 5000  # Duración del humo en milisegundos
humo_tiempo_inicio = 0
RANGO_HUMO = 100

# Variables para la barra de carga
carga_maxima = 100  # Carga máxima
carga_actual = 100  # Carga actual
carga_velocidad = 0.25  # Velocidad de recarga por iteración

# Andrés Miguel Escolastico Lara 23-EISN-2-056

# Crear el laberinto
laberinto = [[1] * COLUMNAS for _ in range(FILAS)]

# Direcciones posibles para moverse (arriba, abajo, izquierda, derecha)
DIRECCIONES = [(-2, 0), (2, 0), (0, -2), (0, 2)]

# Función para generar al jugador
def generar_jugador():
    fila, columna = random.randint(1, FILAS - 1), random.randint(1, COLUMNAS - 1)
    while laberinto[fila][columna] == 1:  # Buscar una posición libre
        fila, columna = random.randint(1, FILAS - 1), random.randint(1, COLUMNAS - 1)
    return columna * TAM_CELDA + (TAM_CELDA - jugador_ancho) // 2, fila * TAM_CELDA + (TAM_CELDA - jugador_alto) // 2

# Andrés Miguel Escolastico Lara 23-EISN-2-056

# Función para generar las monedas en cada ronda
def generar_monedas():
    global monedas
    monedas = []  # Limpiar las monedas anteriores
    for _ in range(10):
        fila = random.randint(1, FILAS - 2)
        columna = random.randint(1, COLUMNAS - 2)
        while laberinto[fila][columna] == 1:  # Asegurarse de que la moneda no esté en una pared
            fila = random.randint(1, FILAS - 2)
            columna = random.randint(1, COLUMNAS - 2)
        monedas.append((columna * TAM_CELDA + TAM_CELDA // 2, fila * TAM_CELDA + TAM_CELDA // 2))

# Función para generar las monedas rojas (en todas las rondas)
def generar_monedas_rojas():
    global monedas_rojas
    monedas_rojas.clear()  # Limpiar las monedas rojas anteriores
    for _ in range(2):  # Generar 2 monedas rojas en cada ronda
        fila, columna = random.randint(1, FILAS - 1), random.randint(1, COLUMNAS - 1)
        while laberinto[fila][columna] == 1 or (fila * TAM_CELDA, columna * TAM_CELDA) in monedas_rojas:
            fila, columna = random.randint(1, FILAS - 1), random.randint(1, COLUMNAS - 1)
        monedas_rojas.append((columna * TAM_CELDA + TAM_CELDA // 4, fila * TAM_CELDA + TAM_CELDA // 4))

# Andrés Miguel Escolastico Lara 23-EISN-2-056

# Clases para el árbol de comportamiento
class Nodo:
    def __init__(self):
        self.hijos = []

    def agregar_hijo(self, hijo):
        self.hijos.append(hijo)

    def ejecutar(self):
        pass

# Andrés Miguel Escolastico Lara 23-EISN-2-056

class Selector(Nodo):
    def ejecutar(self):
        for hijo in self.hijos:
            if hijo.ejecutar():
                return True
        return False

class Secuencia(Nodo):
    def ejecutar(self):
        for hijo in self.hijos:
            if not hijo.ejecutar():
                return False
        return True

# Andrés Miguel Escolastico Lara 23-EISN-2-056

class Accion(Nodo):
    def __init__(self, accion):
        super().__init__()
        self.accion = accion

    def ejecutar(self):
        return self.accion()

class Invertir(Nodo):
    def __init__(self, accion):
        super().__init__()
        self.agregar_hijo(accion)

    def ejecutar(self):
        return not self.hijos[0].ejecutar()

class Timer(Nodo):
    def __init__(self, tiempo):
        super().__init__()
        self.tiempo = tiempo
        self.tiempo_restante = tiempo

    def ejecutar(self):
        if self.tiempo_restante > 0:
            self.tiempo_restante -= 1
            return False
        else:
            self.tiempo_restante = self.tiempo
            self.hijos[0].ejecutar()
            return True

# Andrés Miguel Escolastico Lara 23-EISN-2-056

# Algorimto Astar
class NodoAStar:
    def __init__(self, dato, padre, costo_heuristico):
        self.dato = dato
        self.padre = padre
        self.costo_heuristico = costo_heuristico
        self.costo_total = (padre.costo_total if padre else 0) + 1 + costo_heuristico

    def __lt__(self, otro):
        return self.costo_total < otro.costo_total

# Andrés Miguel Escolastico Lara 23-EISN-2-056

def heuristica(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def generar_sucesores(estado, laberinto):
    fila, columna = estado
    sucesores = []
    for df, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:  # Arriba, abajo, izquierda, derecha
        nueva_fila, nueva_columna = fila + df, columna + dc
        if 0 <= nueva_fila < FILAS and 0 <= nueva_columna < COLUMNAS and laberinto[nueva_fila][nueva_columna] == 0:
            sucesores.append((nueva_fila, nueva_columna))
    return sucesores

# Andrés Miguel Escolastico Lara 23-EISN-2-056

def Astar(estado_inicial, estado_final, laberinto):
    if estado_inicial == estado_final:
        return [], 0, 0  # Si ya está en el objetivo

    totalnodos = 1
    nodo_inicial = NodoAStar(estado_inicial, None, heuristica(estado_inicial, estado_final))
    nodosgenerado = []
    heapq.heappush(nodosgenerado, nodo_inicial)
    nodosvisitados = set()

    inicio = time.perf_counter()

    while nodosgenerado:
        nodoactual = heapq.heappop(nodosgenerado)

        if nodoactual.dato == estado_final:
            break

        if nodoactual.dato in nodosvisitados:
            continue

        nodosvisitados.add(nodoactual.dato)

        sucesores = generar_sucesores(nodoactual.dato, laberinto)
        totalnodos += len(sucesores)

        for sucesor in sucesores:
            if sucesor not in nodosvisitados:
                nuevo_nodo = NodoAStar(sucesor, nodoactual, heuristica(sucesor, estado_final))
                heapq.heappush(nodosgenerado, nuevo_nodo)
    else:
        # No hay camino
        return [], totalnodos, time.perf_counter() - inicio

    camino = []
    while nodoactual:
        camino.append(nodoactual.dato)
        nodoactual = nodoactual.padre
    camino.reverse()
    fin = time.perf_counter()
    return camino, totalnodos, fin - inicio

# Andrés Miguel Escolastico Lara 23-EISN-2-056

# Función para generar a los enemigos
def generar_enemigo():
    fila, columna = random.randint(1, FILAS - 1), random.randint(1, COLUMNAS - 1)
    while laberinto[fila][columna] == 1 or any(abs(enemigo[0] - columna * TAM_CELDA) < TAM_CELDA and abs(enemigo[1] - fila * TAM_CELDA) < TAM_CELDA for enemigo in enemigos):
        fila, columna = random.randint(1, FILAS - 1), random.randint(1, COLUMNAS - 1)
    enemigo_x = columna * TAM_CELDA + TAM_CELDA // 4
    enemigo_y = fila * TAM_CELDA + TAM_CELDA // 4
    enemigos.append([enemigo_x, enemigo_y])  # Guardamos la posición como lista para facilitar la actualización

# Función para verificar si un enemigo está dentro del rango del humo
def esta_en_rango_humo(enemigo_x, enemigo_y, jugador_x, jugador_y, rango):
    # Calcular la distancia entre el enemigo y el jugador
    distancia = ((enemigo_x - jugador_x) ** 2 + (enemigo_y - jugador_y) ** 2) ** 0.5
    return distancia <= rango

# Andrés Miguel Escolastico Lara 23-EISN-2-056

# Función para mover los enemigos
def mover_enemigos():
    global enemigos, pos_x, pos_y, humo_activo, RANGO_HUMO, ultimo_movimiento_enemigos, intervalo_movimiento

    tiempo_actual = time.time()
    if tiempo_actual - ultimo_movimiento_enemigos < intervalo_movimiento:
        return  # No mover a los enemigos si no ha pasado el tiempo suficiente

    ultimo_movimiento_enemigos = tiempo_actual  # Reiniciar el temporizador

    for i, (enemigo_x, enemigo_y) in enumerate(enemigos[:]):
        # Convertir coordenadas a celdas del laberinto
        inicio_fila = int(enemigo_y // TAM_CELDA)
        inicio_columna = int(enemigo_x // TAM_CELDA)
        inicio = (inicio_fila, inicio_columna)

        objetivo_fila = int(pos_y // TAM_CELDA)
        objetivo_columna = int(pos_x // TAM_CELDA)
        objetivo = (objetivo_fila, objetivo_columna)

        # Árbol de comportamiento
        def perseguir_jugador(enemigo_x, enemigo_y):
            camino, _, _ = Astar(inicio, objetivo, laberinto)
            if len(camino) > 1:  # Si hay un camino válido
                siguiente_paso = camino[1]  # Toma el siguiente paso (no el actual)
                nueva_y = siguiente_paso[0] * TAM_CELDA + (TAM_CELDA - jugador_alto) // 2
                nueva_x = siguiente_paso[1] * TAM_CELDA + (TAM_CELDA - jugador_ancho) // 2

                # Mover directamente a la siguiente celda
                if puede_moverse(nueva_x, nueva_y):
                    enemigos[i] = [nueva_x, nueva_y]
                return True
            return False

        def huir_del_humo(enemigo_x, enemigo_y):
            if humo_activo and esta_en_rango_humo(enemigo_x, enemigo_y, pos_x, pos_y, RANGO_HUMO):
                # Calcular dirección de huida (alejarse del jugador)
                dx = enemigo_x - pos_x
                dy = enemigo_y - pos_y
                distancia = max(1, ((dx ** 2) + (dy ** 2))) ** 0.5

                # Calcular la nueva posición en la cuadrícula
                nueva_x = enemigo_x + (dx / distancia) * TAM_CELDA
                nueva_y = enemigo_y + (dy / distancia) * TAM_CELDA

                # Asegurarse de que la nueva posición esté en una celda válida
                nueva_fila = int(nueva_y // TAM_CELDA)
                nueva_columna = int(nueva_x // TAM_CELDA)
                if 0 <= nueva_fila < FILAS and 0 <= nueva_columna < COLUMNAS and laberinto[nueva_fila][nueva_columna] == 0:
                    enemigos[i] = [nueva_columna * TAM_CELDA + (TAM_CELDA - jugador_ancho) // 2,
                                  nueva_fila * TAM_CELDA + (TAM_CELDA - jugador_alto) // 2]
                return True
            return False

        # Árbol de comportamiento
        comportamiento = Selector()
        comportamiento.agregar_hijo(Accion(lambda: huir_del_humo(enemigo_x, enemigo_y)))
        comportamiento.agregar_hijo(Accion(lambda: perseguir_jugador(enemigo_x, enemigo_y)))
        comportamiento.ejecutar()

# Andrés Miguel Escolastico Lara 23-EISN-2-056

# Función para dibujar los enemigos
def dibujar_enemigos():
    for enemigo_x, enemigo_y in enemigos:
        pygame.draw.rect(pantalla, ROJO, (enemigo_x, enemigo_y, enemigo_ancho, enemigo_alto))

# Función para verificar si el jugador ha chocado con algún enemigo
def verificar_colision_con_enemigos():
    global pos_x, pos_y, jugador_ancho, jugador_alto
    for enemigo_x, enemigo_y in enemigos:
        if abs(enemigo_x - pos_x) < jugador_ancho and abs(enemigo_y - pos_y) < jugador_alto:
            return True  # El jugador colisionó con un enemigo
    return False

# Andrés Miguel Escolastico Lara 23-EISN-2-056

# Funciones del humo
def soltar_humo():
    global humo_activo, humo_x, humo_y, humo_tiempo_inicio, carga_actual

    if carga_actual >= 100:  # Solo soltar humo si la carga está llena
        # Determinar la dirección contraria al movimiento
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            humo_x, humo_y = pos_x, pos_y + TAM_CELDA  # Humo hacia abajo
        elif keys[pygame.K_DOWN]:
            humo_x, humo_y = pos_x, pos_y - TAM_CELDA  # Humo hacia arriba
        elif keys[pygame.K_LEFT]:
            humo_x, humo_y = pos_x + TAM_CELDA, pos_y  # Humo hacia la derecha
        elif keys[pygame.K_RIGHT]:
            humo_x, humo_y = pos_x - TAM_CELDA, pos_y  # Humo hacia la izquierda

        humo_activo = True
        humo_tiempo_inicio = pygame.time.get_ticks()  # Registrar el tiempo de inicio
        carga_actual = 0  # Reiniciar la carga

# Andrés Miguel Escolastico Lara 23-EISN-2-056

def actualizar_humo():
    global humo_activo, humo_x, humo_y

    if humo_activo:
        tiempo_actual = pygame.time.get_ticks()
        if tiempo_actual - humo_tiempo_inicio >= humo_duracion:
            humo_activo = False  # Desactivar el humo después de la duración
            humo_x, humo_y = -100, -100  # Mover el humo fuera de la pantalla

def dibujar_humo():
    if humo_activo:
        pygame.draw.circle(pantalla, GRIS_OSCURO, (int(humo_x), int(humo_y)), TAM_CELDA // 2)

# Andrés Miguel Escolastico Lara 23-EISN-2-056

def actualizar_carga():
    global carga_actual
    if carga_actual < carga_maxima:
        carga_actual += carga_velocidad  # Recargar gradualmente

# Función que determina si un enemigo está dentro del área del humo
def esta_en_humo(enemigo_x, enemigo_y, jugador_x, jugador_y, rango_humo):
    # Calcula la distancia entre el enemigo y el jugador
    distancia = ((enemigo_x - jugador_x) ** 2 + (enemigo_y - jugador_y) ** 2) ** 0.5
    return distancia < rango_humo  # Si el enemigo está dentro del área del humo

# Andrés Miguel Escolastico Lara 23-EISN-2-056

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

# Andrés Miguel Escolastico Lara 23-EISN-2-056

# Iniciar la generación del laberinto
generar_laberinto(1, 1)

# Inicializar Pygame
pygame.init()
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Urban Collection")

# Andrés Miguel Escolastico Lara 23-EISN-2-056

# Fuente personalizada para el título y botones
fuente_titulo = pygame.font.SysFont('Comic Sans MS', 50)  # Fuente más grande y diferente
# Fuente para los contadores
fuente_contadores = pygame.font.SysFont('Arial', 30)  # Fuente Arial para los contadores

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
        fila = int(ey // TAM_CELDA)
        columna = int(ex // TAM_CELDA)
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

# Andrés Miguel Escolastico Lara 23-EISN-2-056

# Función para dibujar botones
def dibujar_boton(texto, x, y, ancho, alto, color_normal, color_hover):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    # Cambiar color si el mouse está sobre el botón
    if x < mouse[0] < x + ancho and y < mouse[1] < y + alto:
        pygame.draw.rect(pantalla, color_hover, (x, y, ancho, alto))
        if click[0] == 1:
            return True
    else:
        pygame.draw.rect(pantalla, color_normal, (x, y, ancho, alto))

    # Dibujar texto en el botón
    texto_boton = fuente_titulo.render(texto, True, BLANCO)
    texto_rect = texto_boton.get_rect(center=(x + ancho // 2, y + alto // 2))
    pantalla.blit(texto_boton, texto_rect)
    return False

# Andrés Miguel Escolastico Lara 23-EISN-2-056

# Función para dibujar la pantalla de inicio
def dibujar_pantalla_inicio():
    pantalla.fill(NEGRO)
    
    # Título del juego
    titulo = fuente_titulo.render("Urban Collection", True, BLANCO)
    titulo_rect = titulo.get_rect(center=(ANCHO // 2, ALTO // 2 - 100))
    pantalla.blit(titulo, titulo_rect)

    # Botón "Iniciar"
    if dibujar_boton("Iniciar", ANCHO // 2 - 100, ALTO // 2, 200, 50, VERDE, (0, 200, 0)):
        return "jugar"
    
    # Botón "Salir"
    if dibujar_boton("Salir", ANCHO // 2 - 100, ALTO // 2 + 70, 200, 50, ROJO, (200, 0, 0)):
        return "salir"
    
    return "inicio"

# Andrés Miguel Escolastico Lara 23-EISN-2-056

# Función para dibujar la pantalla de derrota
def dibujar_pantalla_derrota():
    pantalla.fill(NEGRO)
    
    # Mensaje de derrota
    mensaje = fuente_titulo.render("¡Has perdido!", True, ROJO)
    mensaje_rect = mensaje.get_rect(center=(ANCHO // 2, ALTO // 2 - 100))
    pantalla.blit(mensaje, mensaje_rect)

    # Botón "Volver a jugar"
    if dibujar_boton("Volver a jugar", ANCHO // 2 - 150, ALTO // 2, 300, 50, VERDE, (0, 200, 0)):
        return "jugar"
    
    # Botón "Salir"
    if dibujar_boton("Salir", ANCHO // 2 - 100, ALTO // 2 + 70, 200, 50, ROJO, (200, 0, 0)):
        return "salir"
    
    return "derrota"

# Andrés Miguel Escolastico Lara 23-EISN-2-056

# Función para dibujar la pantalla de victoria
def dibujar_pantalla_victoria():
    pantalla.fill(NEGRO)
    
    # Mensaje de victoria
    mensaje = fuente_titulo.render("¡Has ganado!", True, VERDE)
    mensaje_rect = mensaje.get_rect(center=(ANCHO // 2, ALTO // 2 - 100))
    pantalla.blit(mensaje, mensaje_rect)

    # Botón "Volver a jugar"
    if dibujar_boton("Volver a jugar", ANCHO // 2 - 150, ALTO // 2, 300, 50, VERDE, (0, 200, 0)):
        return "jugar"

    # Andrés Miguel Escolastico Lara 23-EISN-2-056

    # Botón "Salir"
    if dibujar_boton("Salir", ANCHO // 2 - 100, ALTO // 2 + 70, 200, 50, ROJO, (200, 0, 0)):
        return "salir"
    
    return "victoria"

        # Andrés Miguel Escolastico Lara 23-EISN-2-056

# Bucle principal
estado = "inicio"  # Estados: inicio, jugando, derrota, victoria
jugando = True
while jugando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            jugando = False

    actualizar_carga()

        # Andrés Miguel Escolastico Lara 23-EISN-2-056

    if estado == "inicio":
        estado = dibujar_pantalla_inicio()
        if estado == "jugar":
            # Reiniciar variables del juego
            ronda = 1
            gasolina = 100
            enemigos.clear()
            monedas.clear()
            monedas_rojas.clear()
            generar_monedas()
            generar_monedas_rojas()
            generar_enemigos_en_ronda()
            pos_x, pos_y = generar_jugador()
        elif estado == "salir":
            jugando = False
    elif estado == "jugar":
        # Lógica del juego
        pantalla.fill(NEGRO)

        # Verificar si el jugador ha recolectado alguna moneda amarilla
        for moneda in monedas[:]:
            if abs(moneda[0] - pos_x) < TAM_CELDA // 2 and abs(moneda[1] - pos_y) < TAM_CELDA // 2:
                monedas.remove(moneda)

        # Andrés Miguel Escolastico Lara 23-EISN-2-056

        # Comprobar si todas las monedas han sido recolectadas
        if not monedas:
            ronda += 1  # Subir de ronda
            print(f"¡Has completado la ronda {ronda - 1}!")
            if ronda > MAX_RONDAS:
                estado = "victoria"  # Mostrar pantalla de victoria
                continue
            monedas_rojas.clear()
            gasolina = 100  # Recargar gasolina
            enemigos.clear()  # Reiniciar enemigos
            generar_monedas()  # Regenerar las monedas amarillas
            generar_monedas_rojas()  # Regenerar monedas rojas en todas las rondas
            pygame.time.delay(2000)  # Pausa entre rondas
            generar_enemigos_en_ronda()  # Generar enemigos

        # Dibujar el humo
        actualizar_humo()
        dibujar_humo()

        # Andrés Miguel Escolastico Lara 23-EISN-2-056

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

        # Mostrar medidor de carga del humo
        pygame.draw.rect(pantalla, ROJO, (300, 10, 200, 20))  # Fondo de la barra de carga
        pygame.draw.rect(pantalla, GRIS, (300, 10, 2 * carga_actual, 20))  # Barra de carga

        # Mostrar contador de monedas
        texto_monedas = fuente_contadores.render(f'Monedas restantes: {len(monedas)}', True, NEGRO)
        pantalla.blit(texto_monedas, (10, 0))

        # Andrés Miguel Escolastico Lara 23-EISN-2-056

        # Mostrar medidor de gasolina
        pygame.draw.rect(pantalla, ROJO, (ANCHO - 210, 10, 200, 20))  # Fondo del medidor de gasolina
        pygame.draw.rect(pantalla, VERDE, (ANCHO - 210, 10, 2 * gasolina, 20))  # Medidor de gasolina

        # Mostrar ronda actual
        texto_ronda = fuente_contadores.render(f'Ronda: {ronda}', True, NEGRO)
        pantalla.blit(texto_ronda, (ANCHO - 150, 0))

        # Andrés Miguel Escolastico Lara 23-EISN-2-056

        # Dibujar enemigos en pantalla
        dibujar_enemigos()

        # Mover los enemigos
        mover_enemigos()

        # Andrés Miguel Escolastico Lara 23-EISN-2-056

        # Verificar colisiones con enemigos
        if verificar_colision_con_enemigos():
            estado = "derrota"  # Mostrar pantalla de derrota

        # Movimiento del jugador
        keys = pygame.key.get_pressed()
        nueva_x, nueva_y = pos_x, pos_y

        # Andrés Miguel Escolastico Lara 23-EISN-2-056

        if keys[pygame.K_UP]:
            nueva_y -= velocidad
        if keys[pygame.K_DOWN]:
            nueva_y += velocidad
        if keys[pygame.K_LEFT]:
            nueva_x -= velocidad
        if keys[pygame.K_RIGHT]:
            nueva_x += velocidad

        # Detectar si el jugador presiona la barra espaciadora
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            soltar_humo()

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
            estado = "derrota"  # Mostrar pantalla de derrota

    elif estado == "derrota":
        estado = dibujar_pantalla_derrota()
        if estado == "jugar":
            # Reiniciar variables del juego
            ronda = 1
            gasolina = 100
            enemigos.clear()
            monedas.clear()
            monedas_rojas.clear()
            generar_monedas()
            generar_monedas_rojas()
            generar_enemigos_en_ronda()
            pos_x, pos_y = generar_jugador()
        elif estado == "salir":
            jugando = False

    # Andrés Miguel Escolastico Lara 23-EISN-2-056

    elif estado == "victoria":
        estado = dibujar_pantalla_victoria()
        if estado == "jugar":
            # Reiniciar variables del juego
            ronda = 1
            gasolina = 100
            enemigos.clear()
            monedas.clear()
            monedas_rojas.clear()
            generar_monedas()
            generar_monedas_rojas()
            generar_enemigos_en_ronda()
            pos_x, pos_y = generar_jugador()
        elif estado == "salir":
            jugando = False

    pygame.display.flip()
    pygame.time.delay(30)

pygame.quit()
# Andrés Miguel Escolastico Lara 23-EISN-2-056
