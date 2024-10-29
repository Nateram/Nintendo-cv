import cv2
import numpy as np
from time import time

class JuegoPelota:
    def __init__(self):
        self.width = 260
        self.height = 140
        self.x = self.width // 2
        self.y = self.height // 2
        self.dx = 5
        self.dy = 4
        self.radio = 10
        self.color = (0, 255, 255)  # Color amarillo
        
    def actualizar(self):
        # Actualizar posición
        self.x += self.dx
        self.y += self.dy
        
        # Rebotar en los bordes
        if self.x - self.radio <= 0 or self.x + self.radio >= self.width:
            self.dx *= -1
        if self.y - self.radio <= 0 or self.y + self.radio >= self.height:
            self.dy *= -1
    
    def dibujar(self, frame):
        # Crear fondo negro
        frame.fill(20)  # Usar el mismo dark_gray que la consola
        
        # Dibujar la pelota
        cv2.circle(frame, (self.x, self.y), self.radio, self.color, -1)
        
        return frame

def get_frame():
    if not hasattr(get_frame, "juego"):
        get_frame.juego = JuegoPelota()
        get_frame.frame = np.zeros((140, 260, 3), dtype=np.uint8)
    
    get_frame.juego.actualizar()
    return get_frame.juego.dibujar(get_frame.frame)

if __name__ == "__main__":
    # Código para prueba independiente
    while True:
        frame = get_frame()
        cv2.imshow('Juego', frame)
        if cv2.waitKey(30) & 0xFF == 27:
            break
    
    cv2.destroyAllWindows()