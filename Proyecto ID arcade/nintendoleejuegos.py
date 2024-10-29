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
        """Dibuja la pantalla superior de la consola."""
        # Carcasa superior
        cv2.rectangle(self.image, (int(50 * SCALE_X), int(20 * SCALE_Y)), 
                     (int(350 * SCALE_X), int(200 * SCALE_Y)), COLORS['blue'], -1)
        cv2.rectangle(self.image, (int(60 * SCALE_X), int(30 * SCALE_Y)), 
                     (int(340 * SCALE_X), int(190 * SCALE_Y)), COLORS['black'], -1)
        cv2.rectangle(self.image, (int(70 * SCALE_X), int(40 * SCALE_Y)), 
                     (int(330 * SCALE_X), int(180 * SCALE_Y)), COLORS['dark_gray'], -1)

        # Dibujar frame del juego si está en ejecución
        if self.game_running and self.current_game_module:
            try:
                game_frame = self.current_game_module.get_frame()
                game_frame_resized = cv2.resize(game_frame, (int(260 * SCALE_X), int(140 * SCALE_Y)))
                self.image[int(40 * SCALE_Y):int(180 * SCALE_Y), 
                          int(70 * SCALE_X):int(330 * SCALE_X)] = game_frame_resized
            except Exception as e:
                print(f"Error al actualizar el frame del juego: {e}")

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
        """Dibuja la pantalla inferior y su contenido."""
        # Carcasa inferior
        cv2.rectangle(self.image, (int(50 * SCALE_X), int(205 * SCALE_Y)), 
                     (int(350 * SCALE_X), int(385 * SCALE_Y)), COLORS['blue'], -1)
        cv2.rectangle(self.image, (int(118 * SCALE_X), int(218 * SCALE_Y)), 
                     (int(282 * SCALE_X), int(352 * SCALE_Y)), COLORS['black'], -1)

        if self.game_running:
            self.draw_game_screen()
        else:
            self.draw_menu_screen()

    def draw_game_screen(self):
        """Dibuja la pantalla cuando un juego está en ejecución."""
        cv2.rectangle(self.image, (int(125 * SCALE_X), int(225 * SCALE_Y)), 
                     (int(275 * SCALE_X), int(345 * SCALE_Y)), COLORS['black'], -1)
        
        # Botón de salir
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

    def draw_menu_screen(self):
        """Dibuja la pantalla del menú de juegos."""
        cv2.rectangle(self.image, (int(125 * SCALE_X), int(225 * SCALE_Y)), 
                     (int(275 * SCALE_X), int(345 * SCALE_Y)), COLORS['white'], -1)
        
        start_y = int(245 * SCALE_Y)
        for i in range(min(MAX_VISIBLE_ITEMS, len(self.games))):
            game_index = i + self.scroll_offset
            if game_index < len(self.games):
                if game_index == self.selected_game:
                    cv2.rectangle(self.image, (int(130 * SCALE_X), start_y + i * 20), 
                                (int(270 * SCALE_X), start_y + (i + 1) * 20), 
                                COLORS['dark_blue'], -1)
                cv2.putText(self.image, self.games[game_index], 
                           (int(135 * SCALE_X), start_y + i * 20 + 15), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.4 * SCALE_X, 
                           COLORS['black'] if game_index == self.selected_game else COLORS['light_blue'], 
                           1, cv2.LINE_AA)

        # Flechas de scroll
        if self.scroll_offset > 0:
            cv2.putText(self.image, '▲', (int(200 * SCALE_X), int(230 * SCALE_Y)), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.4 * SCALE_X, COLORS['light_blue'], 
                       1, cv2.LINE_AA)
        if self.scroll_offset + MAX_VISIBLE_ITEMS < len(self.games):
            cv2.putText(self.image, '▼', (int(200 * SCALE_X), int(340 * SCALE_Y)), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.4 * SCALE_X, COLORS['light_blue'], 
                       1, cv2.LINE_AA)

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
        """Dibuja los botones de acción (A, B, X, Y)."""
        offset_x = 25
        for (x, y, letter) in [(290, 273, 'X'), (270, 293, 'Y'), 
                              (310, 293, 'A'), (290, 313, 'B')]:
            cv2.circle(self.image, (int((x + offset_x) * SCALE_X), int(y * SCALE_Y)), 
                      int(8 * SCALE_X), COLORS['light_blue'], -1)
            cv2.putText(self.image, letter, 
                       (int((x + offset_x - 5) * SCALE_X), int((y + 4) * SCALE_Y)), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.3 * SCALE_X, COLORS['black'], 
                       1, cv2.LINE_AA)

    def draw_system_buttons(self):
        """Dibuja los botones del sistema (Select, Start, Power)."""
        # Select
        cv2.rectangle(self.image, (int(160 * SCALE_X), int(360 * SCALE_Y)), 
                     (int(180 * SCALE_X), int(368 * SCALE_Y)), COLORS['light_blue'], -1)
        cv2.putText(self.image, 'SELECT', (int(162 * SCALE_X), int(366 * SCALE_Y)), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.2 * SCALE_X, COLORS['dark_text'], 
                    1, cv2.LINE_AA)

        # Start
        cv2.rectangle(self.image, (int(200 * SCALE_X), int(360 * SCALE_Y)), 
                     (int(220 * SCALE_X), int(368 * SCALE_Y)), COLORS['light_blue'], -1)
        cv2.putText(self.image, 'START', (int(202 * SCALE_X), int(366 * SCALE_Y)), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.2 * SCALE_X, COLORS['dark_text'], 
                    1, cv2.LINE_AA)

        # Power
        cv2.rectangle(self.image, (int(290 * SCALE_X), int(360 * SCALE_Y)), 
                     (int(305 * SCALE_X), int(375 * SCALE_Y)), COLORS['dark_text'], -1)
        cv2.putText(self.image, 'o', (int(292 * SCALE_X), int(370 * SCALE_Y)), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.3 * SCALE_X, COLORS['white'], 
                    1, cv2.LINE_AA)

    def handle_mouse_click(self, event, x, y, flags, param):
        """Maneja los clics del mouse."""
        if event == cv2.EVENT_LBUTTONDOWN:
            # Verificar clic en botón de apagado
            power_button_x1 = int(290 * SCALE_X)
            power_button_y1 = int(360 * SCALE_Y)
            power_button_x2 = int(305 * SCALE_X)
            power_button_y2 = int(375 * SCALE_Y)
            
            if (power_button_x1 <= x <= power_button_x2 and 
                power_button_y1 <= y <= power_button_y2):
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
            elif key in [ord('w'), 82]:  # Arriba
                self.selected_game = max(0, self.selected_game - 1)
                self.scroll_offset = min(self.scroll_offset, self.selected_game)
            elif key in [ord('s'), 84]:  # Abajo
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
        """Dibuja la pantalla superior de la consola."""
        # Carcasa superior
        cv2.rectangle(self.image, (int(50 * SCALE_X), int(20 * SCALE_Y)), 
                     (int(350 * SCALE_X), int(200 * SCALE_Y)), COLORS['blue'], -1)
        cv2.rectangle(self.image, (int(60 * SCALE_X), int(30 * SCALE_Y)), 
                     (int(340 * SCALE_X), int(190 * SCALE_Y)), COLORS['black'], -1)
        cv2.rectangle(self.image, (int(70 * SCALE_X), int(40 * SCALE_Y)), 
                     (int(330 * SCALE_X), int(180 * SCALE_Y)), COLORS['dark_gray'], -1)

        # Dibujar frame del juego si está en ejecución
        if self.game_running and self.current_game_module:
            try:
                upper_frame, _ = self.get_game_frames()
                if upper_frame is not None:
                    game_frame_resized = cv2.resize(upper_frame, (int(260 * SCALE_X), int(140 * SCALE_Y)))
                    self.image[int(40 * SCALE_Y):int(180 * SCALE_Y), 
                             int(70 * SCALE_X):int(330 * SCALE_X)] = game_frame_resized
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
        """Ejecuta el bucle principal del emulador."""
        cv2.namedWindow('Nintendo 3DS')
        cv2.setMouseCallback('Nintendo 3DS', lambda event, x, y, flags, param: 
                           self.handle_mouse_click(event, x, y, flags, param))

        while self.running:
            self.draw_console()
            cv2.imshow('Nintendo 3DS', self.image)
            self.handle_key(cv2.waitKey(1) & 0xFF)

        cv2.destroyAllWindows()
    

def main():
    """Función principal que inicia el emulador."""
    emulator = Nintendo3DSEmulator()
    emulator.run()

if __name__ == "__main__":
    main()