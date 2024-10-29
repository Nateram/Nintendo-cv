import cv2
import numpy as np
import os
import importlib.util

# Constantes y configuración
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 700
SCALE_X = WINDOW_WIDTH / 400
SCALE_Y = WINDOW_HEIGHT / 400
MAX_VISIBLE_ITEMS = 5

# Colores
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

class Nintendo3DSEmulator:
    def __init__(self):
        self.image = np.zeros((WINDOW_HEIGHT, WINDOW_WIDTH, 3), dtype=np.uint8)
        self.current_game_module = None
        self.game_running = False
        self.selected_game = 0
        self.scroll_offset = 0
        self.running = True
        self.games = self.get_game_files()
        self.is_dual_screen = False  # Flag para identificar si el juego usa dos pantallas


    def draw_rounded_rectangle(self, x1, y1, x2, y2, radius, color, thickness=-1):
        """Dibuja un rectángulo con esquinas redondeadas"""
        # Dibuja los bordes rectos
        cv2.rectangle(self.image, (x1 + radius, y1), (x2 - radius, y2), color, thickness)
        cv2.rectangle(self.image, (x1, y1 + radius), (x2, y2 - radius), color, thickness)
        
        # Dibuja las esquinas redondeadas
        cv2.ellipse(self.image, (x1 + radius, y1 + radius), (radius, radius), 180, 0, 90, color, thickness)
        cv2.ellipse(self.image, (x2 - radius, y1 + radius), (radius, radius), 270, 0, 90, color, thickness)
        cv2.ellipse(self.image, (x1 + radius, y2 - radius), (radius, radius), 90, 0, 90, color, thickness)
        cv2.ellipse(self.image, (x2 - radius, y2 - radius), (radius, radius), 0, 0, 90, color, thickness)


    def draw_hinge(self):
        """Dibuja la bisagra que conecta las dos pantallas con mejor acabado y bordes circulares"""
        hinge_height = int(10 * SCALE_Y)  # Reducido de 12 a 10
        hinge_y = int(200 * SCALE_Y)
        hinge_width = int(270 * SCALE_X)  # Reducido de 300 a 250
        hinge_x = int(65 * SCALE_X)  # Aumentado de 50 a 75 para centrarlo
        radius = int(5 * SCALE_Y)  # Reducido de 6 a 5
        
        # Dibuja el rectángulo principal de la bisagra
        cv2.rectangle(self.image, 
                    (hinge_x + radius, hinge_y),
                    (hinge_x + hinge_width - radius, hinge_y + hinge_height),
                    COLORS['blue'], -1)  # Cambiado a blue para coincidir con el cuerpo
        
        # Dibuja los bordes circulares
        cv2.circle(self.image, 
                (hinge_x + radius, hinge_y + radius), 
                radius, 
                COLORS['blue'], -1)
        cv2.circle(self.image, 
                (hinge_x + hinge_width - radius, hinge_y + radius), 
                radius, 
                COLORS['blue'], -1)
        
        # Línea brillante superior
        cv2.line(self.image,
                (hinge_x + radius, hinge_y + 1),
                (hinge_x + hinge_width - radius, hinge_y + 1),
                (255, 80, 100), 1)
        
        # Línea brillante inferior
        cv2.line(self.image,
                (hinge_x + radius, hinge_y + hinge_height - 1),
                (hinge_x + hinge_width - radius, hinge_y + hinge_height - 1),
                (255, 80, 50), 1)


    def get_game_files(self):
        """Obtiene la lista de archivos de juegos disponibles."""
        if not os.path.exists('juegos'):
            os.makedirs('juegos')
        return [f for f in os.listdir('juegos') if f.endswith('.py')]

    def import_game(self, game_path):
        """Importa un juego desde su archivo."""
        try:
            module_name = os.path.splitext(os.path.basename(game_path))[0]
            spec = importlib.util.spec_from_file_location(module_name, game_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            return module
        except Exception as e:
            print(f"Error al cargar el juego: {e}")
            return None

    def draw_upper_screen(self):
        """Dibuja la pantalla superior con bordes redondeados"""
        # Carcasa superior con bordes redondeados
        self.draw_rounded_rectangle(
            int(50 * SCALE_X), int(20 * SCALE_Y),
            int(350 * SCALE_X), int(200 * SCALE_Y),
            int(20 * SCALE_X), COLORS['blue'], -1
        )
        
        # Marco negro de la pantalla
        self.draw_rounded_rectangle(
            int(60 * SCALE_X), int(30 * SCALE_Y),
            int(340 * SCALE_X), int(190 * SCALE_Y),
            int(15 * SCALE_X), COLORS['black'], -1
        )
        
        # Área de visualización
        self.draw_rounded_rectangle(
            int(70 * SCALE_X), int(40 * SCALE_Y),
            int(330 * SCALE_X), int(180 * SCALE_Y),
            int(10 * SCALE_X), COLORS['dark_gray'], -1
        )

        if self.game_running and self.current_game_module:
            try:
                upper_frame, _ = self.get_game_frames()
                if upper_frame is not None:
                    game_frame_resized = cv2.resize(upper_frame, (int(250 * SCALE_X), int(130 * SCALE_Y)))
                    # Centrar el frame en la pantalla
                    x_offset = int(75 * SCALE_X)
                    y_offset = int(45 * SCALE_Y)
                    self.image[y_offset:y_offset + int(130 * SCALE_Y), 
                            x_offset:x_offset + int(250 * SCALE_X)] = game_frame_resized
            except Exception as e:
                print(f"Error al actualizar el frame superior: {e}")

    def draw_decorative_elements(self):
        """Dibuja elementos decorativos de la consola."""
        # LEDs superiores
        for i, x in enumerate([80, 90, 100]):
            cv2.circle(self.image, (int(x * SCALE_X), int(35 * SCALE_Y)), 
                    int(2 * SCALE_X), COLORS['light_blue'], -1)
        cv2.circle(self.image, (int(320 * SCALE_X), int(35 * SCALE_Y)), 
                int(3 * SCALE_X), COLORS['light_blue'], -1)
        
        # Borde curvo
        cv2.ellipse(self.image, (int(200 * SCALE_X), int(202 * SCALE_Y)), 
                    (int(130 * SCALE_X), int(5 * SCALE_Y)), 0, 0, 180, 
                    COLORS['light_blue'], -1)

    def draw_lower_screen(self):
        """Dibuja la pantalla inferior con bordes redondeados"""
        # Carcasa inferior
        self.draw_rounded_rectangle(
            int(50 * SCALE_X), int(205 * SCALE_Y),
            int(350 * SCALE_X), int(385 * SCALE_Y),
            int(20 * SCALE_X), COLORS['blue'], -1
        )
        
        # Marco de la pantalla
        cv2.rectangle(self.image, 
                    (int(118 * SCALE_X), int(218 * SCALE_Y)),
                    (int(282 * SCALE_X), int(352 * SCALE_Y)),
                    COLORS['black'], -1)

        if self.game_running:
            self.draw_game_screen()
        else:
            self.draw_menu_screen()

    def draw_menu_screen(self):
        """Dibuja la pantalla del menú de juegos estilo Nintendo DS con scroll horizontal."""
        MAX_VISIBLE_ITEMS = 3  # Número de juegos visibles en la pantalla
        ICON_SIZE = int(32 * SCALE_X)  # Tamaño reducido del logo
        
        # Asegurar que el elemento seleccionado esté visible
        if self.selected_game >= self.scroll_offset + MAX_VISIBLE_ITEMS:
            self.scroll_offset = self.selected_game - MAX_VISIBLE_ITEMS + 1
        elif self.selected_game < self.scroll_offset:
            self.scroll_offset = self.selected_game

        # Área disponible para dibujar (2 píxeles menos por cada lado)
        MENU_LEFT = int(120 * SCALE_X)  
        MENU_TOP = int(220 * SCALE_Y)   
        MENU_RIGHT = int(280 * SCALE_X)  
        MENU_BOTTOM = int(350 * SCALE_Y) 
        
        # Fondo blanco del área del menú
        self.draw_rounded_rectangle(
            MENU_LEFT, MENU_TOP,
            MENU_RIGHT, MENU_BOTTOM,
            int(5 * SCALE_X), COLORS['white'], -1
        )
        
        # Dibujar el recuadro y nombre del juego seleccionado en la parte superior
        if 0 <= self.selected_game < len(self.games):
            selected_game_name = os.path.splitext(self.games[self.selected_game])[0]
            text_size = cv2.getTextSize(selected_game_name, cv2.FONT_HERSHEY_SIMPLEX, 
                                    0.5 * SCALE_X, 1)[0]
            
            # Calcular dimensiones del recuadro del título
            title_padding = int(10 * SCALE_X)
            title_height = int(30 * SCALE_Y)
            title_top = MENU_TOP + int(5 * SCALE_Y)
            
            # Dibujar recuadro para el título
            self.draw_rounded_rectangle(
                MENU_LEFT + title_padding,
                title_top,
                MENU_RIGHT - title_padding,
                title_top + title_height,
                int(3 * SCALE_X),
                (240, 240, 240),  # Color gris muy claro
                -1
            )
            
            # Dibujar el texto del título centrado en el recuadro
            text_x = MENU_LEFT + (MENU_RIGHT - MENU_LEFT - text_size[0]) // 2
            text_y = title_top + (title_height + text_size[1]) // 2
            cv2.putText(self.image, selected_game_name,
                    (text_x, text_y),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5 * SCALE_X,
                    COLORS['dark_text'], 1, cv2.LINE_AA)
        
        # Calcular el espacio disponible y el espaciado entre elementos
        available_width = MENU_RIGHT - MENU_LEFT - int(20 * SCALE_X)
        item_spacing = available_width // MAX_VISIBLE_ITEMS
        start_x = MENU_LEFT + int(15 * SCALE_X)
        center_y = MENU_TOP + (MENU_BOTTOM - MENU_TOP) // 2 + int(20 * SCALE_Y)
        
        for i in range(min(MAX_VISIBLE_ITEMS, len(self.games))):
            game_index = i + self.scroll_offset
            if game_index < len(self.games):
                current_x = start_x + i * item_spacing
                game_name = os.path.splitext(self.games[game_index])[0]
                
                # Cargar y mostrar el logo del juego
                logo_path = os.path.join('Juegos', f"{game_name}.jpg")
                if os.path.exists(logo_path):
                    try:
                        logo = cv2.imread(logo_path)
                        if logo is not None:
                            # Redimensionar logo
                            logo = cv2.resize(logo, (ICON_SIZE, ICON_SIZE))
                            
                            # Coordenadas para el logo
                            logo_x = current_x
                            logo_y = center_y - int(ICON_SIZE/2)
                            
                            # Si es el juego seleccionado, dibujar fondo resaltado
                            if game_index == self.selected_game:
                                padding = int(3 * SCALE_X)
                                self.draw_rounded_rectangle(
                                    logo_x - padding, 
                                    logo_y - padding,
                                    logo_x + ICON_SIZE + padding,
                                    logo_y + ICON_SIZE + padding,
                                    int(3 * SCALE_X),
                                    (214, 232, 248),
                                    -1
                                )
                                
                                # Borde de selección
                                self.draw_rounded_rectangle(
                                    logo_x - padding,
                                    logo_y - padding,
                                    logo_x + ICON_SIZE + padding,
                                    logo_y + ICON_SIZE + padding,
                                    int(3 * SCALE_X),
                                    (173, 216, 230),
                                    1
                                )
                            
                            # Insertar logo en la imagen
                            self.image[logo_y:logo_y+ICON_SIZE, 
                                    logo_x:logo_x+ICON_SIZE] = logo
                            
                    except Exception as e:
                        print(f"Error al cargar el logo de {game_name}: {e}")
                        self._draw_fallback_item(game_name, current_x, center_y, game_index, ICON_SIZE)
                else:
                    self._draw_fallback_item(game_name, current_x, center_y, game_index, ICON_SIZE)

        # Indicadores de scroll (flechas izquierda/derecha)
        if self.scroll_offset > 0:
            # Flecha izquierda (ajustada para quedar dentro del menú)
            triangle_pts = np.array([
                [MENU_LEFT + int(3 * SCALE_X), center_y],  # Punta
                [MENU_LEFT + int(8 * SCALE_X), center_y - int(5 * SCALE_Y)],  # Superior
                [MENU_LEFT + int(8 * SCALE_X), center_y + int(5 * SCALE_Y)]   # Inferior
            ], np.int32)
            cv2.fillPoly(self.image, [triangle_pts], COLORS['dark_text'])

        if self.scroll_offset + MAX_VISIBLE_ITEMS < len(self.games):
            # Flecha derecha
            triangle_pts = np.array([
                [MENU_RIGHT - int(5 * SCALE_X), center_y],  # Punta
                [MENU_RIGHT - int(10 * SCALE_X), center_y - int(5 * SCALE_Y)],  # Superior
                [MENU_RIGHT - int(10 * SCALE_X), center_y + int(5 * SCALE_Y)]   # Inferior
            ], np.int32)
            cv2.fillPoly(self.image, [triangle_pts], COLORS['dark_text'])






    def _draw_fallback_item(self, game_name, current_x, center_y, game_index, ICON_SIZE):
        """Dibuja un elemento de menú sin logo como fallback."""
        if game_index == self.selected_game:
            self.draw_rounded_rectangle(
                current_x - int(3 * SCALE_X),
                center_y - int(ICON_SIZE/2) - int(3 * SCALE_Y),
                current_x + ICON_SIZE + int(3 * SCALE_X),
                center_y + int(ICON_SIZE/2) + int(3 * SCALE_Y),
                int(3 * SCALE_X),
                (214, 232, 248),
                -1
            )
            self.draw_rounded_rectangle(
                current_x - int(3 * SCALE_X),
                center_y - int(ICON_SIZE/2) - int(3 * SCALE_Y),
                current_x + ICON_SIZE + int(3 * SCALE_X),
                center_y + int(ICON_SIZE/2) + int(3 * SCALE_Y),
                int(3 * SCALE_X),
                (173, 216, 230),
                1
            )
        
        cv2.putText(self.image, game_name,
                    (current_x, center_y),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.35 * SCALE_X,
                    COLORS['dark_text'], 1, cv2.LINE_AA)


 

    def draw_controls(self):
        """Dibuja los controles de la consola."""
        # Circle Pad
        cv2.circle(self.image, (int(81 * SCALE_X), int(260 * SCALE_Y)), 
                int(18 * SCALE_X), COLORS['light_blue'], -1)

        # D-Pad
        dpad_points = np.array([
            [65, 307], [75, 307], [75, 297], [85, 297], [85, 307],
            [95, 307], [95, 317], [85, 317], [85, 327], [75, 327],
            [75, 317], [65, 317]
        ], np.int32)
        dpad_points = np.array([[int(x * SCALE_X), int(y * SCALE_Y)] for x, y in dpad_points])
        cv2.fillPoly(self.image, [dpad_points], COLORS['light_blue'])

        # Botones A B X Y
        self.draw_action_buttons()
        
        # Botones Select y Start
        self.draw_system_buttons()

    def draw_action_buttons(self):
        """Dibuja los botones de acción (A,B,X,Y) con mejor acabado"""
        button_radius = int(8 * SCALE_X)
        offset_x = 25
        button_positions = [
            (290, 273, 'X', (200, 200, 200)),  # X button
            (270, 293, 'Y', (200, 200, 200)),  # Y button
            (310, 293, 'A', (200, 200, 200)),  # A button
            (290, 313, 'B', (200, 200, 200))   # B button
        ]
        
        for x, y, letter, color in button_positions:
            # Sombra del botón
            cv2.circle(self.image, 
                    (int((x + offset_x) * SCALE_X), int(y * SCALE_Y)),
                    button_radius + 1,
                    (30, 30, 30), -1)
            
            # Botón principal
            cv2.circle(self.image, 
                    (int((x + offset_x) * SCALE_X), int(y * SCALE_Y)),
                    button_radius,
                    color, -1)
            
            # Brillo superior
            cv2.ellipse(self.image,
                    (int((x + offset_x) * SCALE_X), int(y * SCALE_Y)),
                    (button_radius-2, button_radius//2),
                    0, 180, 360,
                    (255, 255, 255), 1)
            
            # Letra del botón
            cv2.putText(self.image, letter,
                    (int((x + offset_x - 4) * SCALE_X), int((y + 4) * SCALE_Y)),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.4 * SCALE_X,
                    (50, 50, 50), 1, cv2.LINE_AA)

    def draw_circle_pad(self):
        """Dibuja el Circle Pad con efecto 3D más realista"""
        center_x = int(81 * SCALE_X)
        center_y = int(260 * SCALE_Y)
        radius = int(18 * SCALE_X)
        
        # Base oscura del Circle Pad
        cv2.circle(self.image, (center_x, center_y), 
                radius + int(2 * SCALE_X),
                COLORS['darker_blue'], -1)
        
        # Círculo principal con gradiente
        cv2.circle(self.image, (center_x, center_y), radius,
                COLORS['light_gray'], -1)
        
        # Efecto de profundidad
        cv2.circle(self.image, (center_x, center_y),
                int(radius * 0.85),
                (200, 200, 200), -1)
        
        # Efecto de brillo superior
        cv2.ellipse(self.image,
                (center_x - int(2 * SCALE_X), center_y - int(2 * SCALE_Y)),
                (int(radius * 0.6), int(radius * 0.2)),
                -30, 0, 180,
                (255, 255, 255), 1)

    def draw_system_buttons(self):
        """Dibuja los botones SELECT y START con mejor acabado y texto centrado"""
        button_height = int(12 * SCALE_Y)  # Aumentado de 10 a 12
        
        # SELECT y START
        for i, (text, x) in enumerate([('SELECT', 150), ('START', 210)]):
            button_width = int(45 * SCALE_X)  # Aumentado de 30 a 35
            button_x = int(x * SCALE_X)
            button_y = int(360 * SCALE_Y)
            
            # Sombra del botón
            self.draw_rounded_rectangle(
                button_x, button_y,
                button_x + button_width, button_y + button_height,
                int(3 * SCALE_X), (30, 30, 30), -1
            )
            
            # Botón principal
            self.draw_rounded_rectangle(
                button_x, button_y,
                button_x + button_width, button_y + (button_height - 1),
                int(3 * SCALE_X), (180, 180, 180), -1
            )
            
            # Calcular dimensiones del texto
            font_scale = 0.35 * SCALE_X  # Reducido ligeramente de 0.4 a 0.35
            (text_width, text_height), baseline = cv2.getTextSize(
                text, cv2.FONT_HERSHEY_SIMPLEX, font_scale, 1
            )
            
            # Calcular posición centrada del texto
            text_x = button_x + (button_width - text_width) // 2
            text_y = button_y + (button_height + text_height) // 2
            
            # Dibujar texto centrado
            cv2.putText(self.image, text,
                    (text_x, text_y),
                    cv2.FONT_HERSHEY_SIMPLEX, font_scale,
                    (50, 50, 50), 1, cv2.LINE_AA)

        # Botón de encendido (sin cambios)
        power_button_x = int(290 * SCALE_X)
        power_button_y = int(360 * SCALE_Y)
        
        # Sombra del botón de encendido
        cv2.circle(self.image,
                (power_button_x, power_button_y),
                int(9 * SCALE_X),
                (30, 30, 30), -1)
        
        # Botón principal
        cv2.circle(self.image,
                (power_button_x, power_button_y),
                int(8 * SCALE_X),
                (180, 180, 180), -1)
        
        # Brillo superior
        cv2.ellipse(self.image,
                (power_button_x, power_button_y),
                (int(6 * SCALE_X), int(3 * SCALE_X)),
                0, 180, 360,
                (255, 255, 255), 1)

    def handle_mouse_click(self, event, x, y, flags, param):
        """Maneja los clics del mouse."""
        if event == cv2.EVENT_LBUTTONDOWN:
            # Obtener el centro del botón de apagado
            power_button_x = int(290 * SCALE_X)
            power_button_y = int(360 * SCALE_Y)
            
            # Radio del botón de apagado
            power_button_radius = int(9 * SCALE_X)
            
            # Calcular la distancia entre el clic y el centro del botón
            distance = ((x - power_button_x) ** 2 + (y - power_button_y) ** 2) ** 0.5
            
            # Si el clic está dentro del radio del botón
            if distance <= power_button_radius:
                self.running = False

    def handle_key(self, key):
        """Maneja las entradas de teclado."""
        if self.game_running:
            if key == ord('q'):
                self.game_running = False
                self.current_game_module = None
            else:
                try:
                    self.current_game_module.handle_key(key)
                except Exception as e:
                    print(f"Error al manejar la tecla en el juego: {e}")
        else:
            if key == 27:  # Esc
                self.running = False
            elif key in [ord('a'), 82]:  # Arriba
                self.selected_game = max(0, self.selected_game - 1)
                self.scroll_offset = min(self.scroll_offset, self.selected_game)
            elif key in [ord('d'), 84]:  # Abajo
                self.selected_game = min(len(self.games) - 1, self.selected_game + 1)
                if self.selected_game >= self.scroll_offset + MAX_VISIBLE_ITEMS:
                    self.scroll_offset = self.selected_game - MAX_VISIBLE_ITEMS + 1
            elif key == 13:  # Enter
                if self.games:
                    game_path = os.path.join('juegos', self.games[self.selected_game])
                    self.current_game_module = self.import_game(game_path)
                    if self.current_game_module:
                        self.game_running = True

    def draw_console(self):
        """Dibuja la consola completa."""
        self.image = np.zeros((WINDOW_HEIGHT, WINDOW_WIDTH, 3), dtype=np.uint8)
        self.draw_upper_screen()
        self.draw_decorative_elements()
        self.draw_lower_screen()
        self.draw_controls()
        self.draw_hinge()

    def get_game_frames(self):
        """Obtiene los frames del juego actual, maneja tanto uno como dos frames."""
        try:
            if hasattr(self.current_game_module, 'get_frames'):
                # Juego con dos pantallas
                self.is_dual_screen = True
                return self.current_game_module.get_frames()
            elif hasattr(self.current_game_module, 'get_frame'):
                # Juego con una pantalla
                self.is_dual_screen = False
                frame = self.current_game_module.get_frame()
                return frame, None
            else:
                raise AttributeError("El juego debe implementar get_frame() o get_frames()")
        except Exception as e:
            print(f"Error al obtener frames del juego: {e}")
            return None, None
    

    def draw_upper_screen(self):
        """Dibuja la pantalla superior con bordes redondeados"""
        # Carcasa superior con bordes redondeados
        self.draw_rounded_rectangle(
            int(50 * SCALE_X), int(20 * SCALE_Y),
            int(350 * SCALE_X), int(200 * SCALE_Y),
            int(20 * SCALE_X), COLORS['blue'], -1
        )
        
        # Marco negro de la pantalla con bordes redondeados más pequeños
        self.draw_rounded_rectangle(
            int(60 * SCALE_X), int(30 * SCALE_Y),
            int(340 * SCALE_X), int(190 * SCALE_Y),
            int(15 * SCALE_X), COLORS['black'], -1
        )
        
        # Área de visualización con bordes redondeados sutiles
        self.draw_rounded_rectangle(
            int(70 * SCALE_X), int(40 * SCALE_Y),
            int(330 * SCALE_X), int(180 * SCALE_Y),
            int(10 * SCALE_X), COLORS['dark_gray'], -1
        )

        if self.game_running and self.current_game_module:
            try:
                upper_frame, _ = self.get_game_frames()
                if upper_frame is not None:
                    game_frame_resized = cv2.resize(upper_frame, (int(250 * SCALE_X), int(130 * SCALE_Y)))
                    # Centrar el frame en la pantalla
                    x_offset = int(75 * SCALE_X)
                    y_offset = int(45 * SCALE_Y)
                    self.image[y_offset:y_offset + int(130 * SCALE_Y), 
                            x_offset:x_offset + int(250 * SCALE_X)] = game_frame_resized
            except Exception as e:
                print(f"Error al actualizar el frame superior: {e}")
    

    def draw_game_screen(self):
        """Dibuja la pantalla cuando un juego está en ejecución."""
        cv2.rectangle(self.image, (int(125 * SCALE_X), int(225 * SCALE_Y)), 
                    (int(275 * SCALE_X), int(345 * SCALE_Y)), COLORS['black'], -1)
        
        if self.game_running and self.current_game_module:
            if self.is_dual_screen:
                try:
                    _, lower_frame = self.get_game_frames()
                    if lower_frame is not None:
                        game_frame_resized = cv2.resize(lower_frame, 
                                                    (int(150 * SCALE_X), int(120 * SCALE_Y)))
                        # Calculamos la posición para centrar el frame
                        frame_x = int(125 * SCALE_X)
                        frame_y = int(225 * SCALE_Y)
                        self.image[frame_y:frame_y + int(120 * SCALE_Y), 
                                frame_x:frame_x + int(150 * SCALE_X)] = game_frame_resized
                except Exception as e:
                    print(f"Error al actualizar el frame inferior: {e}")
            else:
                # Solo mostramos el botón de salir si el juego usa una pantalla
                button_width = int(80 * SCALE_X)
                button_height = int(25 * SCALE_Y)
                button_x = int(200 * SCALE_X - button_width // 2)
                button_y = int(285 * SCALE_Y - button_height // 2)
                
                cv2.rectangle(self.image, (button_x, button_y), 
                            (button_x + button_width, button_y + button_height), 
                            COLORS['red'], 1)
                
                cv2.putText(self.image, 'Q = SALIR', 
                        (button_x + int(10 * SCALE_X), button_y + int(17 * SCALE_Y)), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.4 * SCALE_X, COLORS['red'], 1, 
                        cv2.LINE_AA)

    def run(self):
        cv2.namedWindow('Nintendo 3DS')
        cv2.setMouseCallback('Nintendo 3DS', lambda event, x, y, flags, param: 
                        self.handle_mouse_click(event, x, y, flags, param))

        while self.running:
            self.draw_console()
            cv2.imshow('Nintendo 3DS', self.image)
            self.handle_key(cv2.waitKey(1) & 0xFF)

        cv2.destroyAllWindows()

def main():
    emulator = Nintendo3DSEmulator()
    emulator.run()

if __name__ == "__main__":
    main()