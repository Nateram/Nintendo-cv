import cv2
import numpy as np
import threading
from dataclasses import dataclass
from typing import Tuple, List, Optional
from enum import Enum

class Mode(Enum):
    STANDBY = 0
    CAMERA = 1
    PAINT = 2

@dataclass
class Color:
    BGR: Tuple[int, int, int]
    name: str

@dataclass
class Button:
    x1: int
    y1: int
    x2: int
    y2: int
    color: Color
    text: str

class Nintendo3DSSimulator:
    # Colores predefinidos
    COLORS = {
        'BLUE': Color((240, 130, 30), "Azul"),
        'BLACK': Color((0, 0, 0), "Negro"),
        'DARK_GRAY': Color((20, 20, 20), "Gris Oscuro"),
        'LIGHT_BLUE': Color((173, 216, 230), "Azul Claro"),
        'DARK_TEXT': Color((40, 40, 40), "Texto Oscuro"),
        'LIGHT_GRAY': Color((211, 211, 211), "Gris Claro"),
        'WHITE': Color((255, 255, 255), "Blanco"),
        'RED': Color((0, 0, 255), "Rojo"),
        'GREEN': Color((0, 255, 0), "Verde"),
        'YELLOW': Color((0, 255, 255), "Amarillo"),
        'PURPLE': Color((255, 0, 255), "Morado"),
        'ORANGE': Color((0, 165, 255), "Naranja")
    }

    def __init__(self, width: int = 800, height: int = 700):
        self.width = width
        self.height = height
        self.scale_x = width / 400
        self.scale_y = height / 400
        
        # Estado del simulador
        self.mode = Mode.STANDBY
        self.current_color = self.COLORS['BLACK']
        self.brush_size = 2
        self.is_drawing = False
        self.last_pos = None
        
        # Inicialización de componentes
        self.image = np.zeros((height, width, 3), dtype=np.uint8)
        self.drawing_canvas = self._create_drawing_canvas()
        self.camera = None
        self.camera_thread = None
        
        # Configuración de la ventana
        cv2.namedWindow('Nintendo 3DS')
        cv2.setMouseCallback('Nintendo 3DS', self._handle_mouse_events)
        
        # Inicializar la interfaz
        self._init_interface()

    def _create_drawing_canvas(self) -> np.ndarray:
        canvas = np.zeros((int(100 * self.scale_y), int(260 * self.scale_x), 3), dtype=np.uint8)
        canvas.fill(255)
        return canvas

    def _init_interface(self):
        """Inicializa todos los elementos de la interfaz"""
        self._draw_case()
        self._draw_screens()
        self._draw_buttons()
        self._draw_controls()

    def _draw_case(self):
        """Dibuja la carcasa principal"""
        # Superior
        cv2.rectangle(self.image, 
                     self._scale_point(50, 20), 
                     self._scale_point(350, 200), 
                     self.COLORS['BLUE'].BGR, -1)
        # Inferior
        cv2.rectangle(self.image, 
                     self._scale_point(50, 205), 
                     self._scale_point(350, 385), 
                     self.COLORS['BLUE'].BGR, -1)

    def _draw_screens(self):
        """Dibuja las pantallas superior e inferior"""
        # Pantalla superior
        self._draw_screen(40, 180, True)
        # Pantalla inferior
        self._draw_screen(220, 350, False)

    def _draw_screen(self, y_start: int, y_end: int, is_upper: bool):
        """Dibuja una pantalla individual"""
        margin = 10
        if is_upper:
            # Marco exterior
            cv2.rectangle(self.image,
                         self._scale_point(60, y_start - margin),
                         self._scale_point(340, y_end + margin),
                         self.COLORS['BLACK'].BGR, -1)
            # Pantalla
            cv2.rectangle(self.image,
                         self._scale_point(70, y_start),
                         self._scale_point(330, y_end),
                         self.COLORS['DARK_GRAY'].BGR, -1)
        else:
            cv2.rectangle(self.image,
                         self._scale_point(125, y_start),
                         self._scale_point(275, y_end),
                         self.COLORS['WHITE'].BGR, -1)

    def _scale_point(self, x: int, y: int) -> Tuple[int, int]:
        """Escala un punto según las dimensiones actuales"""
        return (int(x * self.scale_x), int(y * self.scale_y))

    def _handle_mouse_events(self, event, x: int, y: int, flags, param):
        """Maneja todos los eventos del mouse"""
        if event == cv2.EVENT_LBUTTONDOWN:
            self._handle_click(x, y)
        elif event == cv2.EVENT_MOUSEMOVE:
            self._handle_mouse_move(x, y)
        elif event == cv2.EVENT_LBUTTONUP:
            self._handle_mouse_release()

    def _handle_click(self, x: int, y: int):
        """Maneja los clicks del mouse"""
        if self.mode == Mode.PAINT:
            self._handle_paint_click(x, y)
        self._check_control_buttons(x, y)

    def run(self):
        """Ejecuta el bucle principal del simulador"""
        while True:
            if self.mode == Mode.PAINT:
                self._update_paint_screen()
            
            cv2.imshow('Nintendo 3DS', self.image)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        
        self._cleanup()

    def _cleanup(self):
        """Limpia los recursos antes de cerrar"""
        if self.camera is not None:
            self.camera.release()
        cv2.destroyAllWindows()

    def _update_paint_screen(self):
        """Actualiza la pantalla del modo pintura"""
        self._draw_color_palette()
        self.image[int(80 * self.scale_y):int(180 * self.scale_y),
                  int(70 * self.scale_x):int(330 * self.scale_x)] = self.drawing_canvas

    def _start_camera(self):
        """Inicia la cámara en un hilo separado"""
        if self.mode != Mode.CAMERA:
            self.mode = Mode.CAMERA
            self.camera = cv2.VideoCapture(0)
            self.camera_thread = threading.Thread(target=self._camera_loop)
            self.camera_thread.start()

    def _camera_loop(self):
        """Bucle principal de la cámara"""
        while self.mode == Mode.CAMERA and self.camera is not None:
            ret, frame = self.camera.read()
            if ret:
                frame_resized = cv2.resize(frame, 
                                         (int(260 * self.scale_x), 
                                          int(140 * self.scale_y)))
                self.image[int(40 * self.scale_y):int(180 * self.scale_y),
                          int(70 * self.scale_x):int(330 * self.scale_x)] = frame_resized
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        
        self._stop_camera()

    def _stop_camera(self):
        """Detiene la cámara y limpia los recursos"""
        self.mode = Mode.STANDBY
        if self.camera is not None:
            self.camera.release()
            self.camera = None
        if self.camera_thread is not None:
            self.camera_thread.join()
            self.camera_thread = None

if __name__ == "__main__":
    simulator = Nintendo3DSSimulator()
    simulator.run()