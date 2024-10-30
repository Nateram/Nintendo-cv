# Manual de Usuario - Juego de Batalla Pokémon

## 1. Introducción
Este juego es un simulador de batallas Pokémon por turnos donde dos Pokémon se enfrentan en combate. El juego presenta una interfaz gráfica que muestra a los Pokémon, sus barras de vida y un menú de movimientos. Los Pokémon disponibles son:
- Ceruledge
- Zeraora
- Gengar
- MissingNo
- Agumon
- Shadow
- Gallade
- Eelektross
- Zoroark
- Luxray
- Froslass
- Sceptile
- Gardevoir
- Haxorus
- Chandelure
- Volcarona
- Metagross
- Noivern
- Aegislash
- Mimikyu

### 1.1 Características principales
- Sistema de batalla por turnos
- Animaciones de ataques y efectos visuales
- Sistema de tipos de movimientos
- Interfaz gráfica intuitiva
- Mecánicas de curación y daño

## 2. Materiales

### 2.1 Requerimientos de hardware
- Procesador: 1.6 GHz o superior
- Memoria RAM: 2GB mínimo
- Espacio en disco: 100MB libre
- Tarjeta gráfica: Compatible con OpenGL 2.0

### 2.2 Requerimientos de software
- Sistema operativo: Windows 7/10/11, macOS 10.12+, o Linux
- Python 3.7 o superior
- Bibliotecas Python requeridas:
  - OpenCV (cv2) versión 4.0+
  - NumPy versión 1.19+
  - Random (incluido en Python)
  - Time (incluido en Python)
  - Math (incluido en Python)

### 2.3 Archivos necesarios
- Script principal del juego
- Carpeta "Juegos/Imagenes/" con imágenes de todos los Pokémon disponibles
  - Nota: Las imágenes deben tener fondo verde (RGB: 0, 255, 0) para permitir la transparencia
  - El sistema utiliza una función específica que elimina este tono de verde para crear transparencia en los sprites

### 2.4 Sistema de Tipos
El juego incluye los siguientes tipos de movimientos:
- PHYSICAL: Movimientos físicos básicos
- FIRE: Movimientos de tipo fuego
- WATER: Movimientos de tipo agua
- ELECTRIC: Movimientos eléctricos
- GROUND: Movimientos de tipo tierra
- STEEL: Movimientos de tipo acero
- DARK: Movimientos siniestros
- POISON: Movimientos venenosos
- PSYCHIC: Movimientos psíquicos
- HEAL: Movimientos curativos
- ICE: Movimientos de hielo
- DRAGON: Movimientos tipo dragón
- FAIRY: Movimientos de tipo hada
- GRASS: Movimientos de tipo planta

## 3. Manual de uso

### 3.1 Instalación
1. Instalar Python desde python.org
2. Instalar las bibliotecas requeridas usando pip:
   ```
   pip install opencv-python numpy
   ```
3. Colocar las imágenes en la carpeta correcta
4. Ejecutar el script principal

### 3.2 Controles básicos
- **W** o **↑**: Mover selección hacia arriba
- **S** o **↓**: Mover selección hacia abajo
- **A** o **←**: Mover selección hacia la izquierda
- **D** o **→**: Mover selección hacia la derecha
- **Espacio** o **Enter**: Confirmar selección
- **R**: Reiniciar batalla
- **Esc**: Salir del juego

### 3.3 Interfaz del juego
1. **Ventana principal**:
   - Área superior: Campo de batalla
   - Área inferior: Mensajes de batalla
   - Lateral: Barras de vida

2. **Ventana de menú**:
   - Cuadrícula 2x2 de movimientos
   - Códigos de color por tipo de movimiento
   - Información de daño/curación

### 3.4 Mecánicas del juego
1. **Inicio de batalla**:
   - Al comenzar, se seleccionan automáticamente dos Pokémon aleatorios
   - Cada Pokémon comienza con 100 HP

2. **Sistema de turnos**:
   - El jugador siempre realiza el primer movimiento
   - Después del turno del jugador, el enemigo realiza su movimiento automáticamente

3. **Movimientos**:
   - Cada Pokémon tiene 4 movimientos diferentes
   - Los movimientos pueden ser:
     - Ataques (causan daño)
     - Curaciones (restauran HP)
   - Los movimientos están codificados por colores según su tipo

4. **Elementos visuales**:
   - Barra de vida:
     - Verde: HP > 50%
     - Amarillo: 20% < HP ≤ 50%
     - Rojo: HP ≤ 20%
   - Efectos visuales:
     - Flash rojo al recibir daño
     - Animaciones de movimientos
     - Mensajes de batalla

### 3.5 Movimientos por Pokémon

#### Ceruledge
- Terremoto (28 DMG) - GROUND
- Espada Santa (25 DMG) - STEEL
- Pulso Umbrio (22 DMG) - DARK
- Nitrocarga (20 DMG) - FIRE

#### Zeraora
- Ataque Arena (20 DMG) - GROUND
- Plasma Feroz (24 DMG) - ELECTRIC
- Velocidad Extrema (18 DMG) - PHYSICAL
- Hiperpocion (-25 HP, cura) - HEAL

#### Gengar
- Bola Sombra (23 DMG) - DARK
- Bomba Lodo (25 DMG) - POISON
- Psiquico (25 DMG) - PSYCHIC
- Maldicion (-22 HP, cura) - HEAL

#### MissingNo
- Error Fatal (30 DMG) - PSYCHIC
- Corrupcion (25 DMG) - DARK
- Terremoto (28 DMG) - GROUND
- Bug (-30 HP, cura) - HEAL

#### Agumon
- Llama Bebe (18 DMG) - FIRE
- Golpe Veneno (22 DMG) - POISON
- Aliento Dragon (22 DMG) - DRAGON
- Evolucion (-28 HP, cura) - HEAL

#### Shadow
- Pulso Oscuro (28 DMG) - DARK
- Rayo Hielo (25 DMG) - ICE
- Bomba Lodo (24 DMG) - POISON
- Aura Oscura (-24 HP, cura) - HEAL

#### Gallade
- Psico-corte (24 DMG) - PSYCHIC
- Cabeza Metal (20 DMG) - STEEL
- Terremoto (28 DMG) - GROUND
- Recuperacion (-25 HP, cura) - HEAL

#### Eelektross
- Trueno (25 DMG) - ELECTRIC
- Cola Ferrea (20 DMG) - STEEL
- Ataque Arena (18 DMG) - GROUND
- Descanso (-25 HP, cura) - HEAL

#### Zoroark
- Pulso Umbrio (24 DMG) - DARK
- Lanzamugre (20 DMG) - POISON
- Psiquico (21 DMG) - PSYCHIC
- Ilusion (-22 HP, cura) - HEAL

#### Luxray
- Colmillo Rayo (22 DMG) - ELECTRIC
- Golpe Veneno (20 DMG) - POISON
- Brillo Magico (24 DMG) - FAIRY
- Descanso (-23 HP, cura) - HEAL

#### Froslass
- Ventisca (25 DMG) - ICE
- Beso Drenaje (22 DMG) - FAIRY
- Cola Dragon (20 DMG) - DRAGON
- Nieve Curativa (-24 HP, cura) - HEAL

#### Sceptile
- Tormenta Floral (26 DMG) - GRASS
- Garra Metal (24 DMG) - STEEL
- Meteoro Dragon (28 DMG) - DRAGON
- Sintesis (-25 HP, cura) - HEAL

#### Gardevoir
- Psiquico (28 DMG) - PSYCHIC
- Luz Lunar (22 DMG) - FAIRY
- Voz Cautivadora (24 DMG) - FAIRY
- Paz Mental (-26 HP, cura) - HEAL

#### Haxorus
- Garra Dragon (27 DMG) - DRAGON
- Guillotina (30 DMG) - STEEL
- Pulso Dragon (25 DMG) - DRAGON
- Danza Dragon (-23 HP, cura) - HEAL

#### Chandelure
- Fuego Fatuo (24 DMG) - FIRE
- Fuerza Lunar (23 DMG) - FAIRY
- Llamarada (28 DMG) - FIRE
- Absorber (-22 HP, cura) - HEAL

#### Volcarona
- Danza Llama (26 DMG) - FIRE
- Garra Metal (22 DMG) - STEEL
- Vendaval (24 DMG) - DRAGON
- Escudo Polen (-25 HP, cura) - HEAL

#### Metagross
- Puño Meteoro (28 DMG) - STEEL
- Cabeza Hierro (25 DMG) - STEEL
- Garra Dragon (24 DMG) - DRAGON
- Agilidad (-24 HP, cura) - HEAL

#### Noivern
- Estruendo (25 DMG) - DRAGON
- Pulso Dragon (26 DMG) - DRAGON
- Bomba Magica (22 DMG) - FAIRY
- Supersonica (-23 HP, cura) - HEAL

#### Aegislash
- Espada Santa (27 DMG) - STEEL
- Filo Real (23 DMG) - STEEL
- Golpe Real (25 DMG) - STEEL
- Escudo Real (-24 HP, cura) - HEAL

#### Mimikyu
- Garra Umbria (24 DMG) - DARK
- Juego Sucio (22 DMG) - DARK
- Brillo Magico (25 DMG) - FAIRY
- Disfraz (-26 HP, cura) - HEAL


### 3.6 Sistema de Transparencia
El juego utiliza un sistema de transparencia basado en el color verde para los sprites de los Pokémon:
- Las imágenes deben tener un fondo verde específico (RGB: 0, 255, 0)
- El sistema detecta automáticamente este color verde y lo convierte en transparente
- Esto permite que los Pokémon se muestren correctamente sobre el fondo de batalla
- La transparencia se aplica en tiempo real durante el renderizado

Consideraciones para las imágenes:
- Usar exactamente el tono de verde especificado (RGB: 0, 255, 0)
- Evitar usar este tono de verde en los sprites de los Pokémon
- Mantener bordes limpios para mejor resultado
- Asegurar que la imagen tenga buena calidad para evitar artefactos

## 4. Resolución de problemas

### 4.1 Problemas comunes y soluciones
1. **El juego no inicia**:
   - Verificar que Python está instalado correctamente
   - Comprobar que todas las bibliotecas están instaladas
   - Verificar que las imágenes están en la ubicación correcta

2. **Errores de visualización**:
   - Actualizar los drivers de la tarjeta gráfica
   - Verificar la resolución mínima requerida (800x600)
   - Reiniciar el juego

3. **Problemas de rendimiento**:
   - Cerrar aplicaciones en segundo plano
   - Verificar los requisitos mínimos del sistema
   - Actualizar las bibliotecas de Python

### 4.2 Contacto y soporte
Si encuentras algún error o tienes sugerencias, puedes:
- Reportar problemas en el repositorio del proyecto
- Contactar al equipo de desarrollo
- Consultar la documentación en línea

## 5. Consejos y estrategias
1. **Gestión de HP**:
   - Utiliza movimientos de curación cuando tu HP esté por debajo del 50%
   - Considera el daño que puede hacer el enemigo en su turno

2. **Selección de movimientos**:
   - Los movimientos más fuertes suelen ser más efectivos al inicio
   - Guarda las curaciones para momentos críticos
   - Observa los patrones del enemigo

3. **Estrategia general**:
   - Mantén un balance entre ataque y defensa
   - Anticipa los movimientos del oponente
   - Utiliza las curaciones de manera estratégica


# Manual del Programador - Juego de Batalla Pokémon

## 1. Arquitectura del Sistema

### 1.1 Estructura General
El sistema está construido alrededor de la clase principal `PokemonBattle` que gestiona toda la lógica del juego. La arquitectura sigue un patrón de estado que controla el flujo de la batalla.

### 1.2 Componentes Principales
```
PokemonBattle/
├── Clases Principales
│   ├── PokemonBattle (Controlador principal)
│   ├── Pokemon (Modelo de datos)
│   └── Animation (Sistema de animaciones)
├── Estados
│   ├── BattleState.SELECTING_ACTION
│   ├── BattleState.ANIMATING
│   └── BattleState.BATTLE_ENDED
└── Sistemas
    ├── Sistema de Renderizado
    ├── Sistema de Animaciones
    └── Sistema de Entrada
```

## 2. Estructuras de Datos Principales

### 2.1 Estructura Pokémon
```python
Pokemon = {
    "name": str,         # Nombre del Pokémon
    "image": np.array,   # Imagen del Pokémon
    "hp": int,          # Puntos de vida
    "moves": List[Move]  # Lista de movimientos
}

Move = {
    "name": str,        # Nombre del movimiento
    "damage": int,      # Daño (-valor para curación)
    "type": AnimationType # Tipo de animación
}
```

### 2.2 Estados de Batalla
```python
class BattleState:
    SELECTING_ACTION  # Jugador seleccionando movimiento
    ANIMATING        # Animación en proceso
    BATTLE_ENDED     # Batalla terminada
```

### 2.3 Posiciones Globales
```python
# Posiciones predefinidas para Pokémon en batalla
player_pos = (150, 150)  # Posición del Pokémon del jugador
enemy_pos = (650, 150)   # Posición del Pokémon enemigo
```

## 3. Flujos Principales de Código

### 3.1 Loop Principal
```python
while True:
    battle_frame, menu_frame = get_frames()
    cv2.imshow('Pokemon Battle', battle_frame)
    cv2.imshow('Battle Menu', menu_frame)
    key = cv2.waitKey(1) & 0xFF
    handle_key(key)
```

### 3.2 Flujo de Batalla
1. Inicialización
2. Selección de movimiento
3. Ejecución de animación
4. Cálculo de daño
5. Turno del enemigo
6. Verificación de estado

## 4. APIs y Métodos Principales

### 4.1 PokemonBattle
```python
class PokemonBattle:
    def reset_battle(self)
    def execute_move(self)
    def update_battle_state(self)
    def draw(self)
    def handle_input(self, key)
```

### 4.2 Métodos de Renderizado
```python
def draw_background(self, frame)
def draw_menu(self)
def draw_health_bar(self, frame, x, y, width, current_hp, max_hp)
```

### 4.3 Métodos de Animación
```python
def create_animation(self, move, attacker_pos, target_pos)
def start_damage_animation(self, is_player)
def start_health_animation(self, pokemon, new_hp)
def update_health_animation(self)
```

### 4.4 Métodos de Procesamiento de Imagen
```python
def remove_green_background(image):
    """
    Elimina el fondo verde de las imágenes de Pokémon.
    Parámetros:
        image: Imagen PIL con fondo verde
    Retorna:
        Imagen PIL con fondo transparente
    """
```

## 5. Sistema de Animaciones

### 5.1 Tipos de Animación
```python
class AnimationType(Enum):
    NONE = 0
    FIRE = 1       # Efectos de fuego y calor
    ELECTRIC = 2   # Rayos y electricidad
    HEAL = 3       # Efectos curativos
    PHYSICAL = 4   # Ataques físicos
    WATER = 5      # Efectos de agua
    GRASS = 6      # Efectos naturales
    PSYCHIC = 7    # Efectos psíquicos
    ICE = 8        # Efectos de hielo
    DARK = 9       # Efectos oscuros
    STEEL = 10     # Efectos metálicos
    FAIRY = 11     # Efectos de hada
    DRAGON = 12    # Efectos dracónicos
    POISON = 13    # Efectos venenosos
    GROUND = 14    # Efectos terrestres
```

### 5.2 Sistema de Partículas

El sistema de animaciones está basado en partículas, donde cada tipo de ataque tiene sus propias características y comportamientos. Las partículas se generan, mueven y desvanecen según patrones específicos para cada tipo de ataque.

#### 5.2.1 Configuración de Partículas
Cada tipo de animación tiene su propia configuración que define:
- Cantidad de partículas
- Rango de tamaños
- Comportamiento de movimiento
- Paleta de colores
- Efectos especiales (estelas, brillos, etc.)

#### 5.2.2 Estructura de Partícula
Cada partícula en el sistema contiene:
```python
particle = {
    'pos': list,              # Posición actual [x, y]
    'velocity': list,         # Vector de velocidad [vx, vy]
    'size': int,             # Tamaño de la partícula
    'lifetime': float,        # Duración de vida
    'angle': float,          # Ángulo de rotación
    'alpha': int,            # Transparencia
    'color_offset': float,   # Desplazamiento de color
    'oscillation_offset': float, # Desplazamiento de oscilación
    'trail': list           # Lista para efectos de estela
}
```

### 5.3 Control de Animaciones

#### 5.3.1 Inicialización
El sistema inicializa las partículas según el tipo de animación, configurando:
- Cantidad y tamaño según el tipo
- Propiedades específicas del tipo de ataque
- Velocidades y posiciones iniciales
- Efectos especiales requeridos

#### 5.3.2 Cálculo de Velocidad
Las velocidades se calculan considerando:
- Dirección hacia el objetivo
- Dispersión aleatoria controlada
- Velocidad base del tipo de ataque
- Factores de aceleración/desaceleración

### 5.4 Parámetros de Animación

#### 5.4.1 Temporización
- Duración base: 1.5 segundos
- Progress: 0.0 a 1.0 (controla la evolución de la animación)
- Lifetime de partículas: 0.7 a 1.2 segundos (variable)

#### 5.4.2 Espaciales
- Dispersión: Variable según tipo de ataque
- Tamaños: Configurados por tipo
- Velocidades: 12.0 a 15.0 unidades base
- Área de efecto: Determinada por el tipo de ataque

## 6. Gestión de Recursos

### 6.1 Imágenes
- Formato: JPG
- Ubicación: "Juegos/Imagenes/"
- Nomenclatura: pokemon1.jpg, pokemon2.jpg, etc.
- Fondo verde para transparencia

### 6.2 Memoria
- Uso de NumPy para procesamiento de imágenes
- Gestión de frames en memoria
- Limpieza de recursos no utilizados

### 6.3 Dependencias Externas
- PIL (Python Imaging Library)
  - Usado para: Procesamiento de imágenes
  - Clases principales: Image, ImageDraw, ImageFont
- OpenCV (cv2)
  - Usado para: Renderizado y visualización
  - Funciones principales: imshow, waitKey
- NumPy
  - Usado para: Procesamiento de arrays de imágenes
- Enum
  - Usado para: Estados de batalla y tipos de animación

## 7. Guía de Modificación

### 7.1 Añadir Nuevo Pokémon
1. Agregar imagen en formato correcto
2. Definir movimientos en `reset_battle()`
3. Actualizar lista de `available_pokemon`

```python
moves_nuevo_pokemon = [
    {"name": "Movimiento1", "damage": 20, "type": AnimationType.PHYSICAL},
    {"name": "Movimiento2", "damage": 25, "type": AnimationType.FIRE},
    {"name": "Movimiento3", "damage": 22, "type": AnimationType.WATER},
    {"name": "Movimiento4", "damage": -20, "type": AnimationType.HEAL}
]

available_pokemon.append({
    "name": "NuevoPokemon",
    "image": "Juegos/Imagenes/pokemon5.jpg",
    "hp": 100,
    "moves": moves_nuevo_pokemon
})
```

### 7.2 Añadir Nuevo Tipo de Animación
1. Definir nuevo tipo en `AnimationType`
2. Implementar lógica de renderizado
3. Actualizar `create_animation()`

### 7.3 Gestión de Estado Global
```python
# Variable global del juego
_pokemon_battle = None  # Instancia única de PokemonBattle

def get_battle_instance():
    """
    Patrón Singleton para acceder a la instancia de batalla
    Returns:
        PokemonBattle: Instancia única del juego
    """
    global _pokemon_battle
    if _pokemon_battle is None:
        _pokemon_battle = PokemonBattle()
    return _pokemon_battle
```

## 8. Debugging

### 8.1 Puntos de Control Principales
```python
def debug_state(self):
    print(f"Battle State: {self.battle_state}")
    print(f"Pokemon 1 HP: {self.pokemon1.current_hp}")
    print(f"Pokemon 2 HP: {self.pokemon2.current_hp}")
    print(f"Current Animation: {self.current_animation}")
```

### 8.2 Errores Comunes
1. Problemas de carga de imágenes
   - Verificar rutas
   - Comprobar formato
2. Errores de animación
   - Revisar temporizadores
   - Verificar posiciones
3. Problemas de rendimiento
   - Profiling de operaciones costosas
   - Optimización de renderizado

### 8.3 Logging y Monitoreo
```python
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('pokemon_battle')

def log_battle_state(self):
    """
    Registra el estado actual de la batalla
    """
    logger.debug(f"Battle State: {self.battle_state}")
    logger.debug(f"Animations running: {len(self.active_animations)}")
    logger.debug(f"Current move: {self.current_move}")
```

## 9. Futuras Mejoras

### 9.1 Mejoras Propuestas
1. Sistema de tipos de Pokémon
2. Efectividad de movimientos
3. Efectos de estado
4. Multiplayer local
5. Sistema de guardado

### 9.2 Refactorizaciones Sugeridas
1. Separación de lógica de renderizado
2. Sistema de eventos
3. Gestor de recursos centralizado
4. Sistema de configuración externo

### 9.3 Integración con Sistemas Externos
1. Sistema de guardado en base de datos
2. Modo multijugador en red
3. Sistema de repeticiones
4. Integración con API de estadísticas
5. Sistema de logros

## 10. Control de Entrada

### 10.1 Sistema de Manejo de Teclas
```python
def handle_input(self, key):
    """
    Procesa la entrada del usuario
    Parámetros:
        key: Código de tecla OpenCV
    """
    # Mapeo de teclas
    KEY_UP = 0xFF
    KEY_DOWN = 0xFF
    KEY_ENTER = 13
    KEY_ESC = 27
```

### 10.2 Estados de Input
- MENU_NAVIGATION: Navegación por menú
- MOVE_SELECTION: Selección de movimiento
- BATTLE_ANIMATION: Input bloqueado durante animaciones

## 11. Gestión de Ventanas

### 11.1 Configuración de Ventanas OpenCV
```python
def setup_windows():
    """
    Configura las ventanas de OpenCV
    """
    cv2.namedWindow('Pokemon Battle', cv2.WINDOW_NORMAL)
    cv2.namedWindow('Battle Menu', cv2.WINDOW_NORMAL)
    cv2.resizeWindow('Pokemon Battle', 800, 600)
    cv2.resizeWindow('Battle Menu', 400, 200)
```

### 11.2 Limpieza de Recursos
```python
def cleanup():
    """
    Limpia recursos y cierra ventanas
    """
    cv2.destroyAllWindows()
    # Limpieza de caché y recursos
```