# Colección urbana 🎮

# Descripción 📝

Urban Collection es un juego de laberinto en 2D desarrollado con Pygame donde el jugador debe recolectar monedas mientras evita enemigos inteligentes.

El juego presenta mecánicas únicas como un sistema de humo defensivo, regeneración de energía y múltiples rondas con dificultad progresiva.


# Desarrollado por 👨‍💻
Andrés Miguel Escolastico Lara (23-EISN-2-056).

# Características principales ✨

# Jugabilidad 🕹️

# Sistema de rondas : 
5 rondas con dificultad progresiva.📈

# Recolección de recursos : 
Monedas amarillas 🟡 para avanzar y monedas rojas 🔴 para recargar combustible.

# Mecánica defensiva : 
Sistema de humo 💨 que hace que los enemigos huyan temporalmente.

# Sistema de combustible : 
Recurso ⛽ que disminuye constantemente y debe gestionarse.

# Aspectos técnicos 🔧

# Generación procedural : 
Laberinto único creado usando un algoritmo DFS (Depth-First Search) modificado.🧩

# Inteligencia artificial avanzada 🧠
Implementación desde cero del algoritmo A* para búsqueda de caminos.🔍

Árboles de comportamiento completos para la toma de decisiones de los enemigos.🌳


# Efectos visuales : 
Rotación dinámica de sprites según la dirección del movimiento.🔄

# Interfaz de usuario : 
Menús interactivos para inicio, victoria y derrota.📊

# Elementos multimedia 🎨

# Sprites personalizados : 
Jugador, enemigos, monedas y efectos.🎭
# Efectos de sonido : 
Para acciones como recoger monedas y activar humo.🔊
# Música de fondo : 
Ambiente sonoro durante todo el juego.🎵

# Controles 🎮

# Flechas direccionales ⬆️⬇️⬅️➡️: 
Moverse por el laberinto.
# Barra espaciadora ⌨️: 
Activar el humo defensivo (requiere barra de carga completa).

# Objetivo del juego 🎯
El jugador debe recolectar todas las monedas amarillas en cada ronda para avanzar. 

Al completar las 5 rondas, el jugador gana el juego 🏆. 

Si el jugador choca con un enemigo 👾 o se queda sin combustible ⚠️, pierde.

# Implementación técnica destacada 💻

# Algoritmo A* 🧭
El juego implementa el algoritmo A* desde cero para que los enemigos encuentren la ruta más eficiente hacia el jugador, 
considerando las paredes del laberinto como obstáculos. 
Este algoritmo permite que los enemigos tomen decisiones inteligentes sobre cómo navegar por el laberinto.

# Árboles de arbol 🌲
Se ha implementado un sistema completo de árboles de comportamiento con:

Selectores (OR lógico).⚡

Secuencias (AND lógicas).⛓️

Acciones.🎬

Inversores.🔄

Temporizadores.⏱️

Los enemigos utilizan este sistema para decidir entre perseguir al jugador o huir del humo defensivo cuando está activo.

# Generación de laberintos 🧩
El juego utiliza un algoritmo DFS (Depth-First Search) modificado para generar laberintos únicos con las siguientes características:

Caminos aleatorios garantizando accesibilidad total.🔀

Probabilidad de ensanchamiento de pasillos para mejor jugabilidad.🛣️

Estructura orgánica con diversos caminos y callejones sin salida.🗺️

# Requisitos 📋

Python 3.12.8.🐍

Juego Py.🎲

Archivos de recursos (sprites y sonidos).📁

# Instalación 💾

# Clonar el repositorio
git clone https://github.com/am399315/Urban_collection.git

# Acceder al directorio
cd Urban_collection

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar el juego
python main.py

# Desarrollo 🚀
Este proyecto fue desarrollado  para demostrar implementaciones de inteligencia artificial en videojuegos. Todas las mecánicas, algoritmos y sistemas fueron programados desde cero, sin utilizar librerías externas más allá de Pygame para la interfaz gráfica.

# Estructura del proyecto 📁
# main.py:  
Archivo principal del juego.📄
# Sprites/: 
Directorio con imágenes del juego.🖼️
# Sonidos/: 
Directorio con efectos de sonido y música.🔉
# requirements.txt: 
Dependencias necesarias.📝
