import cv2
import numpy as np
import os
import importlib.util

# Crear imagen (canvas) y definir colores
image = np.zeros((700, 800, 3), dtype=np.uint8)
colors = {
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

# Escala
scale_x, scale_y = 800 / 400, 700 / 400

# Variables globales
current_game_module = None
game_running = False
camera_active = False
camera = None

# Función para obtener archivos .py de juegos
def get_game_files():
    if not os.path.exists('juegos'):
        os.makedirs('juegos')
    return [f for f in os.listdir('juegos') if f.endswith('.py')]

games = get_game_files()
selected_game, scroll_offset, max_visible_items = 0, 0, 5

# Importar juego
def import_game(game_path):
    try:
        module_name = os.path.splitext(os.path.basename(game_path))[0]
        spec = importlib.util.spec_from_file_location(module_name, game_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module
    except Exception as e:
        print(f"Error al cargar el juego: {e}")
        return None

# Función para manejar clics del mouse
def handle_mouse_click(event, x, y, flags, param):
    global running, camera_active, camera
    if event == cv2.EVENT_LBUTTONDOWN:
        # Coordenadas del botón de apagado
        power_button_x1 = int(290 * scale_x)
        power_button_y1 = int(360 * scale_y)
        power_button_x2 = int(305 * scale_x)
        power_button_y2 = int(375 * scale_y)
        
        # Coordenadas del botón de cámara
        camera_button_x1 = int(185 * scale_x)
        camera_button_y1 = int(360 * scale_y)
        camera_button_x2 = int(195 * scale_x)
        camera_button_y2 = int(368 * scale_y)
        
        # Verificar si el clic está dentro del botón de apagado
        if (power_button_x1 <= x <= power_button_x2 and 
            power_button_y1 <= y <= power_button_y2):
            running = False
            
        # Verificar si el clic está dentro del botón de cámara y no hay juego en ejecución
        elif (camera_button_x1 <= x <= camera_button_x2 and 
              camera_button_y1 <= y <= camera_button_y2 and 
              not game_running):
            if not camera_active:
                camera = cv2.VideoCapture(0)
                if camera.isOpened():
                    camera_active = True
            else:
                camera_active = False
                if camera is not None:
                    camera.release()
                    camera = None

# Dibujar consola
def draw_console():
    global image
    image = np.zeros((700, 800, 3), dtype=np.uint8)
    
    # Carcasa superior
    cv2.rectangle(image, (int(50 * scale_x), int(20 * scale_y)), (int(350 * scale_x), int(200 * scale_y)), colors['blue'], -1)
    cv2.rectangle(image, (int(60 * scale_x), int(30 * scale_y)), (int(340 * scale_x), int(190 * scale_y)), colors['black'], -1)
    cv2.rectangle(image, (int(70 * scale_x), int(40 * scale_y)), (int(330 * scale_x), int(180 * scale_y)), colors['dark_gray'], -1)

    if camera_active and camera is not None and not game_running:
        ret, frame = camera.read()
        if ret:
            frame = cv2.flip(frame, 1)  # Voltear horizontalmente para efecto espejo
            frame_resized = cv2.resize(frame, (int(260 * scale_x), int(140 * scale_y)))
            image[int(40 * scale_y):int(180 * scale_y), int(70 * scale_x):int(330 * scale_x)] = frame_resized
    elif game_running and current_game_module:
        try:
            game_frame = current_game_module.get_frame()
            game_frame_resized = cv2.resize(game_frame, (int(260 * scale_x), int(140 * scale_y)))
            image[int(40 * scale_y):int(180 * scale_y), int(70 * scale_x):int(330 * scale_x)] = game_frame_resized
        except Exception as e:
            print(f"Error al actualizar el frame del juego: {e}")

    # Elementos visuales
    for i, x in enumerate([80, 90, 100]):
        cv2.circle(image, (int(x * scale_x), int(35 * scale_y)), int(2 * scale_x), colors['light_blue'], -1)
    cv2.circle(image, (int(320 * scale_x), int(35 * scale_y)), int(3 * scale_x), colors['light_blue'], -1)
    cv2.ellipse(image, (int(200 * scale_x), int(202 * scale_y)), (int(130 * scale_x), int(5 * scale_y)), 0, 0, 180, colors['light_blue'], -1)
    
    # Carcasa inferior
    cv2.rectangle(image, (int(50 * scale_x), int(205 * scale_y)), (int(350 * scale_x), int(385 * scale_y)), colors['blue'], -1)
    cv2.rectangle(image, (int(118 * scale_x), int(218 * scale_y)), (int(282 * scale_x), int(352 * scale_y)), colors['black'], -1)

    if game_running:
        # Pantalla negra cuando se está ejecutando un juego
        cv2.rectangle(image, (int(125 * scale_x), int(225 * scale_y)), (int(275 * scale_x), int(345 * scale_y)), colors['black'], -1)
        
        # Añadir botón de salir estilizado
        button_width = int(80 * scale_x)
        button_height = int(25 * scale_y)
        button_x = int(200 * scale_x - button_width // 2)
        button_y = int(285 * scale_y - button_height // 2)
        
        # Dibujar el botón con borde
        cv2.rectangle(image, 
                     (button_x, button_y), 
                     (button_x + button_width, button_y + button_height), 
                     colors['red'], 1)
        
        # Texto del botón
        cv2.putText(image, 
                    'Q = SALIR', 
                    (button_x + int(10 * scale_x), button_y + int(17 * scale_y)), 
                    cv2.FONT_HERSHEY_SIMPLEX, 
                    0.4 * scale_x, 
                    colors['red'], 
                    1, 
                    cv2.LINE_AA)
    else:
        # Pantalla de menú normal
        cv2.rectangle(image, (int(125 * scale_x), int(225 * scale_y)), (int(275 * scale_x), int(345 * scale_y)), colors['white'], -1)
        start_y = int(245 * scale_y)
        for i in range(min(max_visible_items, len(games))):
            game_index = i + scroll_offset
            if game_index < len(games):
                if game_index == selected_game:
                    cv2.rectangle(image, (int(130 * scale_x), start_y + i * 20), (int(270 * scale_x), start_y + (i + 1) * 20), colors['dark_blue'], -1)
                cv2.putText(image, games[game_index], (int(135 * scale_x), start_y + i * 20 + 15), cv2.FONT_HERSHEY_SIMPLEX, 0.4 * scale_x, colors['black'] if game_index == selected_game else colors['light_blue'], 1, cv2.LINE_AA)

        if scroll_offset > 0:
            cv2.putText(image, '▲', (int(200 * scale_x), int(230 * scale_y)), cv2.FONT_HERSHEY_SIMPLEX, 0.4 * scale_x, colors['light_blue'], 1, cv2.LINE_AA)
        if scroll_offset + max_visible_items < len(games):
            cv2.putText(image, '▼', (int(200 * scale_x), int(340 * scale_y)), cv2.FONT_HERSHEY_SIMPLEX, 0.4 * scale_x, colors['light_blue'], 1, cv2.LINE_AA)

    # Circle Pad y D-Pad
    cv2.circle(image, (int(81 * scale_x), int(260 * scale_y)), int(18 * scale_x), colors['light_blue'], -1)

    # Definir puntos del D-Pad
    dpad_points = np.array([[65, 307], [75, 307], [75, 297], [85, 297], [85, 307], 
                            [95, 307], [95, 317], [85, 317], [85, 327], [75, 327], 
                            [75, 317], [65, 317]], np.int32)

    # Escalar y convertir a enteros
    dpad_points = np.array([[int(x * scale_x), int(y * scale_y)] for x, y in dpad_points])

    # Dibujar D-Pad
    cv2.fillPoly(image, [dpad_points], colors['light_blue'])

    # Botones A B X Y
    offset_x = 25
    for (x, y, letter) in [(290, 273, 'X'), (270, 293, 'Y'), (310, 293, 'A'), (290, 313, 'B')]:
        cv2.circle(image, (int((x + offset_x) * scale_x), int(y * scale_y)), int(8 * scale_x), colors['light_blue'], -1)
        cv2.putText(image, letter, (int((x + offset_x - 5) * scale_x), int((y + 4) * scale_y)), cv2.FONT_HERSHEY_SIMPLEX, 0.3 * scale_x, colors['black'], 1, cv2.LINE_AA)

    # Botones Select, Cámara y Start (reposicionados)
    cv2.rectangle(image, (int(160 * scale_x), int(360 * scale_y)), (int(180 * scale_x), int(368 * scale_y)), colors['light_blue'], -1)
    # Botón de cámara (entre Select y Start)
    button_color = colors['green'] if camera_active and not game_running else colors['dark_text']
    cv2.rectangle(image, (int(185 * scale_x), int(360 * scale_y)), (int(195 * scale_x), int(368 * scale_y)), button_color, -1)
    cv2.rectangle(image, (int(200 * scale_x), int(360 * scale_y)), (int(220 * scale_x), int(368 * scale_y)), colors['light_blue'], -1)
    
    cv2.putText(image, 'SELECT', (int(162 * scale_x), int(366 * scale_y)), cv2.FONT_HERSHEY_SIMPLEX, 0.2 * scale_x, colors['dark_text'], 1, cv2.LINE_AA)
    cv2.putText(image, 'C', (int(187 * scale_x), int(366 * scale_y)), cv2.FONT_HERSHEY_SIMPLEX, 0.2 * scale_x, colors['white'], 1, cv2.LINE_AA)
    cv2.putText(image, 'START', (int(202 * scale_x), int(366 * scale_y)), cv2.FONT_HERSHEY_SIMPLEX, 0.2 * scale_x, colors['dark_text'], 1, cv2.LINE_AA)

    # LED y menú
    cv2.circle(image, (int(70 * scale_x), int(350 * scale_y)), int(2 * scale_x), colors['light_blue'], -1)
    cv2.circle(image, (int(70 * scale_x), int(360 * scale_y)), int(2 * scale_x), colors['light_blue'], -1)

    # Botón de apagado
    cv2.rectangle(image, (int(290 * scale_x), int(360 * scale_y)), (int(305 * scale_x), int(375 * scale_y)), colors['dark_text'], -1)
    cv2.putText(image, 'o', (int(292 * scale_x), int(370 * scale_y)), cv2.FONT_HERSHEY_SIMPLEX, 0.3 * scale_x, colors['white'], 1, cv2.LINE_AA)

# Manejo de teclas
def handle_key(key):
    global selected_game, scroll_offset, running, game_running, current_game_module, camera_active, camera
    if game_running:
        if key == ord('q'):
            game_running = False
            current_game_module = None
            # Desactivar la cámara si estaba activa antes del juego
            if camera_active:
                camera_active = False
                if camera is not None:
                    camera.release()
                    camera = None
        else:
            try:
                current_game_module.handle_key(key)
            except Exception as e:
                print(f"Error al manejar la tecla en el juego: {e}")
    else:
        if key == 27:  # Esc
            running = False
        elif key in [ord('w'), 82]:  # Arriba
            selected_game = max(0, selected_game - 1)
            scroll_offset = min(scroll_offset, selected_game)
        elif key in [ord('s'), 84]:  # Abajo
            selected_game = min(len(games) - 1, selected_game + 1)
            if selected_game >= scroll_offset + max_visible_items:
                scroll_offset = selected_game - max_visible_items + 1
        elif key == 13:  # Enter
            if games:
                # Si la cámara está activa, la desactivamos antes de iniciar el juego
                if camera_active:
                    camera_active = False
                    if camera is not None:
                        camera.release()
                        camera = None
                
                game_path = os.path.join('juegos', games[selected_game])
                current_game_module = import_game(game_path)
                if current_game_module:
                    game_running = True

# Bucle principal
running = True
cv2.namedWindow('Nintendo 3DS')
cv2.setMouseCallback('Nintendo 3DS', handle_mouse_click)

while running:
    draw_console()
    cv2.imshow('Nintendo 3DS', image)
    handle_key(cv2.waitKey(1) & 0xFF)

# Asegurarse de liberar la cámara al cerrar
if camera is not None:
    camera.release()
cv2.destroyAllWindows()