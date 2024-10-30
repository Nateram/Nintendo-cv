# Manual de Usuario: Emulador Nintendo 3DS

## Índice

1. Introducción
2. Materiales
3. Manual de uso

## 1. Introducción

El emulador de Nintendo 3DS es una aplicación de software que simula la experiencia de la consola Nintendo 3DS en tu computadora. Este emulador reproduce fielmente la interfaz física de la consola, incluyendo sus dos pantallas características, controles táctiles y botones físicos, permitiendo ejecutar juegos desarrollados específicamente para esta plataforma.

### Características principales:
- Interfaz gráfica que emula el diseño físico de la Nintendo 3DS
- Soporte para dos pantallas (superior e inferior)
- Sistema de menú con navegación de juegos
- Controles mediante teclado
- Capacidad de cargar y ejecutar juegos personalizados

## 2. Materiales

### Requisitos del Sistema

#### Software necesario:
- Python 3.x instalado en el sistema
- Bibliotecas requeridas:
  - OpenCV (cv2)
  - NumPy
  - os (incluido en Python)
  - importlib

#### Instalación de dependencias:
```bash
pip install opencv-python numpy
```

### Estructura de archivos:
```
emulador_3ds/
├── main.py
└── juegos/
    ├── juego1.py
    ├── juego1.jpg
    ├── juego2.py
    ├── juego2.jpg
    └── imagenes/
        ├── juego1.jpg
        └── juego2.jpg
```

## 3. Manual de uso

### 3.1 Inicio del emulador

1. Abrir una terminal o línea de comandos
2. Navegar hasta el directorio del emulador
3. Ejecutar el comando:
   ```bash
   python main.py
   ```

### 3.2 Controles básicos

#### Navegación en el menú:
- `A`: Seleccionar juego anterior
- `D`→`: Seleccionar juego siguiente
- `Enter`: Iniciar juego seleccionado
- `Pulsar boton apagado`: Salir del emulador

#### Durante el juego:
- `Q`: Volver al menú principal
- Otros controles específicos dependerán de cada juego

### 3.3 Interfaz del emulador

La interfaz del emulador está dividida en varias secciones:

1. **Pantalla superior:**
   - Muestra la imagen principal del juego
   - Incluye LEDs indicadores decorativos

2. **Pantalla inferior:**
   - En el menú: Muestra la selección de juegos disponibles
   - Durante el juego: Muestra controles o interfaz secundaria

3. **Controles físicos:**
   - Circle Pad (simulado)
   - Botones direccionales (D-Pad)
   - Botones de acción (A, B, X, Y)
   - Botones START y SELECT
   - Botón de encendido

### 3.4 Gestión de juegos

Para añadir nuevos juegos al emulador:

1. Crear un archivo Python (.py) en la carpeta "juegos/"
2. El juego debe implementar:
   - Función `get_frame()` para juegos de una pantalla
   - Función `get_frames()` para juegos de dos pantallas
   - Función `handle_key(key)` para manejar controles

### 3.5 Solución de problemas comunes

1. **El emulador no inicia:**
   - Verificar que Python está instalado correctamente
   - Comprobar que todas las dependencias están instaladas
   - Verificar permisos de ejecución del archivo

2. **Los juegos no se cargan:**
   - Comprobar que los archivos están en la carpeta correcta
   - Verificar que el formato del archivo del juego es correcto
   - Revisar la implementación de las funciones requeridas

3. **Problemas de rendimiento:**
   - Cerrar aplicaciones en segundo plano
   - Verificar que el sistema cumple con los requisitos mínimos
   - Comprobar la resolución de pantalla configurada

### 3.6 Recomendaciones de uso

- Mantener actualizado Python y las bibliotecas requeridas
- Hacer copias de seguridad de los juegos desarrollados
- Documentar adecuadamente el código de los juegos nuevos
- Mantener una estructura organizada de archivos
- Probar los juegos antes de integrarlos al sistema

Para soporte adicional o consultas técnicas, consultar la documentación de las bibliotecas utilizadas o contactar con el equipo de desarrollo.



#
#
#


# Manual del Programador: Emulador Nintendo 3DS

## Índice

1. Arquitectura del Sistema
2. Clase Principal Nintendo3DSEmulator
3. Sistema de Renderizado
4. Sistema de Control
5. Gestión de Juegos
6. Guía de Implementación

## 1. Arquitectura del Sistema

### 1.1 Estructura del Proyecto
```
emulador_3ds/
├── main.py                 # Archivo principal del emulador
├── constants.py           # Constantes y configuraciones
└── juegos/               # Directorio de juegos
    ├── __init__.py
    ├── juego1.py
    └── juego2.py
```

### 1.2 Dependencias Principales
```python
import cv2                # Manejo de gráficos y ventanas
import numpy as np        # Operaciones con matrices
import os                 # Operaciones de sistema
import importlib.util     # Carga dinámica de módulos
```

### 1.3 Constantes Globales
```python
WINDOW_WIDTH = 800        # Ancho de la ventana
WINDOW_HEIGHT = 700       # Alto de la ventana
SCALE_X = WINDOW_WIDTH / 400   # Factor de escala X
SCALE_Y = WINDOW_HEIGHT / 400  # Factor de escala Y
MAX_VISIBLE_ITEMS = 5    # Máximo de items visibles en menú

# Diccionario de colores en formato BGR
COLORS = {
    "blue": (240, 130, 30),
    "dark_blue": (30, 60, 100),
    "black": (0, 0, 0),
    "dark_gray": (20, 20, 20),
    "light_blue": (173, 216, 230),
    "dark_text": (40, 40, 40),
    "light_gray": (211, 211, 211),
    "white": (255, 255, 255),
    "red": (0, 0, 255),
    "green": (0, 255, 0)
}
```

## 2. Clase Principal Nintendo3DSEmulator

### 2.1 Constructor
```python
def __init__(self):
    """
    Inicializa el emulador con los siguientes atributos:
    - image: Matriz NumPy para el frame actual
    - current_game_module: Módulo del juego actual
    - game_running: Estado de ejecución del juego
    - selected_game: Índice del juego seleccionado
    - scroll_offset: Desplazamiento del menú
    - running: Estado general del emulador
    - games: Lista de juegos disponibles
    - is_dual_screen: Modo de pantalla del juego
    """
```

### 2.2 Funciones de Renderizado Principal

#### draw_console()
```python
def draw_console(self):
    """
    Función principal de renderizado. Coordina el dibujado de:
    1. Limpia el frame actual
    2. Dibuja pantalla superior
    3. Dibuja elementos decorativos
    4. Dibuja pantalla inferior
    5. Dibuja controles
    6. Dibuja bisagra
    """
```

#### draw_rounded_rectangle()
```python
def draw_rounded_rectangle(self, x1, y1, x2, y2, radius, color, thickness=-1):
    """
    Dibuja un rectángulo con esquinas redondeadas.
    
    Parámetros:
    - x1, y1: Coordenadas de la esquina superior izquierda
    - x2, y2: Coordenadas de la esquina inferior derecha
    - radius: Radio de las esquinas
    - color: Color en formato BGR
    - thickness: Grosor del borde (-1 para relleno)
    """
```

### 2.3 Funciones de Pantallas

#### draw_upper_screen()
```python
def draw_upper_screen(self):
    """
    Dibuja la pantalla superior del emulador.
    - Dibuja carcasa con bordes redondeados
    - Dibuja marco negro interior
    - Dibuja área de visualización
    - Renderiza frame del juego si está activo
    """
```

#### draw_lower_screen()
```python
def draw_lower_screen(self):
    """
    Dibuja la pantalla inferior del emulador.
    - Dibuja carcasa con bordes redondeados
    - Dibuja área táctil
    - Muestra menú o juego según estado
    """
```

### 2.4 Funciones de Control

#### handle_key()
```python
def handle_key(self, key):
    """
    Maneja eventos de teclado.
    
    Modos:
    1. Modo Juego:
        - 'q': Salir al menú
        - Otras teclas: Enviadas al juego actual
    
    2. Modo Menú:
        - ESC: Salir del emulador
        - a/←: Juego anterior
        - d/→: Juego siguiente
        - Enter: Iniciar juego
    """
```

#### handle_mouse_click()
```python
def handle_mouse_click(self, event, x, y, flags, param):
    """
    Maneja eventos del mouse.
    - Detecta clic en botón de apagado
    - Calcula distancia al centro del botón
    - Apaga el emulador si corresponde
    """
```

## 3. Sistema de Menú

### 3.1 draw_menu_screen()
```python
def draw_menu_screen(self):
    """
    Dibuja la interfaz del menú principal.
    
    Características:
    - Scroll horizontal de juegos
    - Íconos de juegos con selección
    - Indicadores de navegación
    - Título del juego seleccionado
    
    Parámetros calculados:
    - MAX_VISIBLE_ITEMS: Juegos visibles simultáneamente
    - ICON_SIZE: Tamaño de íconos de juegos
    - Espaciado y márgenes
    """
```

### 3.2 Gestión de Juegos
```python
def get_game_files(self):
    """
    Obtiene lista de juegos disponibles.
    - Busca archivos .py en directorio 'juegos'
    - Retorna lista de nombres de archivo
    """

def import_game(self, game_path):
    """
    Importa dinámicamente un módulo de juego.
    
    Parámetros:
    - game_path: Ruta al archivo del juego
    
    Retorna:
    - Módulo del juego cargado
    - None si hay error
    """
```

## 4. Implementación de Juegos

### 4.1 Estructura Básica de un Juego
```python
class Game:
    def __init__(self):
        self.frame = np.zeros((400, 400, 3), dtype=np.uint8)
    
    def get_frame(self):
        """
        Retorna el frame actual del juego.
        Requerido para juegos de una pantalla.
        """
        return self.frame
    
    def get_frames(self):
        """
        Retorna tupla de frames (superior, inferior).
        Requerido para juegos de dos pantallas.
        """
        return self.frame_superior, self.frame_inferior
    
    def handle_key(self, key):
        """
        Procesa entrada de teclado.
        
        Parámetros:
        - key: Código ASCII de la tecla presionada
        """
        pass
```

### 4.2 Integración con el Emulador
```python
# Ejemplo de juego básico
def get_frames(self):
    """
    Si el juego usa dos pantallas, debe implementar:
    - Frame superior: 250x130 píxeles
    - Frame inferior: 150x120 píxeles
    """
    return frame_superior, frame_inferior

def get_frame(self):
    """
    Si el juego usa una pantalla, debe implementar:
    - Frame único: 250x130 píxeles
    """
    return frame
```

## 5. Consideraciones Técnicas

### 5.1 Rendimiento
- Usar `np.uint8` para frames
- Minimizar operaciones de dibujo
- Cachear elementos estáticos
- Evitar recálculos innecesarios

### 5.2 Resolución y Escalado
```python
# Factores de escala
SCALE_X = WINDOW_WIDTH / 400
SCALE_Y = WINDOW_HEIGHT / 400

# Aplicar escala a coordenadas
x_scaled = int(x * SCALE_X)
y_scaled = int(y * SCALE_Y)
```

### 5.3 Manejo de Errores
```python
try:
    # Operaciones de juego
except Exception as e:
    print(f"Error en el juego: {e}")
    # Manejo de recuperación
```

## 6. Mejores Prácticas

1. **Organización del Código**
   - Separar lógica de juego de la interfaz
   - Usar constantes para valores fijos
   - Documentar funciones y parámetros

2. **Optimización**
   - Minimizar creación de objetos
   - Reutilizar buffers de imagen
   - Limitar operaciones por frame

3. **Depuración**
   - Implementar logging detallado
   - Usar herramientas de profiling
   - Mantener consistencia en manejo de errores

4. **Extensibilidad**
   - Diseñar para facilitar nuevos juegos
   - Mantener interfaz consistente
   - Documentar API de integración

## 7. Referencias

- Documentación OpenCV: https://docs.opencv.org/
- NumPy Documentation: https://numpy.org/doc/
- Python importlib: https://docs.python.org/3/library/importlib.html