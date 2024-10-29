import cv2
import numpy as np
import random
from collections import deque
from time import time

class Snake:
    def __init__(self): 
        # Dimensiones del juego
        self.width = 300
        self.height = 150
        
        # Tamaño de cada celda del snake
        self.cell_size = 10
        
        # Colores
        self.bg_color = (20, 20, 20)       # Fondo negro
        self.snake_color = (0, 255, 0)      # Snake verde
        self.food_color = (0, 0, 255)       # Comida roja
        self.score_color = (255, 255, 255)  # Texto blanco
        
        # Control de velocidad
        self.last_update = time()
        self.update_interval = 0.2  # Actualizar cada 200ms (más lento)
        
        # Inicializar el juego
        self.reset_game()
        
    def reset_game(self):
        # Inicializar snake en el centro
        center_x = (self.width // self.cell_size) // 2
        center_y = (self.height // self.cell_size) // 2
        
        self.snake = deque([(center_x, center_y)])
        self.direction = 'RIGHT'
        self.next_direction = 'RIGHT'
        self.food = None
        self.score = 0
        self.game_over = False
        self.spawn_food()
    
    def spawn_food(self):
        while True:
            x = random.randint(0, (self.width // self.cell_size) - 1)
            y = random.randint(0, (self.height // self.cell_size) - 1)
            if (x, y) not in self.snake:
                self.food = (x, y)
                break
    
    def handle_input(self, key):
        if self.game_over and key == ord('r'):
            self.reset_game()
            return
        
        # Mapear teclas a direcciones (incluyendo flechas del teclado)
        if (key == ord('w') or key == 82 or key == 0) and self.direction != 'DOWN':  # W o flecha arriba
            self.next_direction = 'UP'
        elif (key == ord('s') or key == 84 or key == 1) and self.direction != 'UP':  # S o flecha abajo
            self.next_direction = 'DOWN'
        elif (key == ord('a') or key == 81 or key == 2) and self.direction != 'RIGHT':  # A o flecha izquierda
            self.next_direction = 'LEFT'
        elif (key == ord('d') or key == 83 or key == 3) and self.direction != 'LEFT':  # D o flecha derecha
            self.next_direction = 'RIGHT'
    
    def should_update(self):
        current_time = time()
        if current_time - self.last_update >= self.update_interval:
            self.last_update = current_time
            return True
        return False
    
    def update(self):
        if self.game_over:
            return
            
        # Solo actualizar si ha pasado suficiente tiempo
        if not self.should_update():
            return
            
        # Actualizar dirección
        self.direction = self.next_direction
        
        # Obtener la cabeza actual
        head_x, head_y = self.snake[0]
        
        # Calcular nueva posición de la cabeza
        if self.direction == 'UP':
            head_y -= 1
        elif self.direction == 'DOWN':
            head_y += 1
        elif self.direction == 'LEFT':
            head_x -= 1
        elif self.direction == 'RIGHT':
            head_x += 1
        
        # Verificar colisiones con los bordes
        if (head_x < 0 or head_x >= self.width // self.cell_size or
            head_y < 0 or head_y >= self.height // self.cell_size):
            self.game_over = True
            return
        
        # Verificar colisión con el propio snake
        if (head_x, head_y) in self.snake:
            self.game_over = True
            return
        
        # Mover el snake
        self.snake.appendleft((head_x, head_y))
        
        # Verificar si comió la comida
        if (head_x, head_y) == self.food:
            self.score += 1
            self.spawn_food()
            # Aumentar velocidad gradualmente con cada comida
            self.update_interval = max(0.1, self.update_interval - 0.01)
        else:
            self.snake.pop()
    
    def draw(self, frame):
        # Limpiar el frame
        frame.fill(self.bg_color[0])
        
        # Dibujar el snake
        for i, (x, y) in enumerate(self.snake):
            # Hacer que la cabeza sea de un verde más brillante
            color = (0, 255, 0) if i == 0 else (0, 200, 0)
            cv2.rectangle(frame,
                        (x * self.cell_size, y * self.cell_size),
                        ((x + 1) * self.cell_size - 1, (y + 1) * self.cell_size - 1),
                        color,
                        -1)
        
        # Dibujar la comida
        if self.food:
            x, y = self.food
            cv2.rectangle(frame,
                        (x * self.cell_size, y * self.cell_size),
                        ((x + 1) * self.cell_size - 1, (y + 1) * self.cell_size - 1),
                        self.food_color,
                        -1)
        
        # Dibujar el puntaje
        score_text = f'Score: {self.score}'
        cv2.putText(frame, score_text, (5, 15),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                   self.score_color, 1, cv2.LINE_AA)
        
        # Si es game over, mostrar mensaje
        if self.game_over:
            game_over_text = 'Game Over! Press R to restart'
            text_size = cv2.getTextSize(game_over_text, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)[0]
            text_x = (self.width - text_size[0]) // 2
            text_y = self.height // 2
            cv2.putText(frame, game_over_text,
                       (text_x, text_y),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                       self.score_color, 1, cv2.LINE_AA)
        
        return frame

# Variables globales para el estado del juego
_snake_game = None

def handle_key(key):
    global _snake_game
    if _snake_game:
        _snake_game.handle_input(key)

def get_frame():
    global _snake_game
    
    # Inicializar el juego si es la primera vez
    if _snake_game is None:
        _snake_game = Snake()
    
    # Actualizar el estado del juego
    _snake_game.update()
    
    # Crear y retornar el frame
    frame = np.zeros((_snake_game.height, _snake_game.width, 3), dtype=np.uint8)
    return _snake_game.draw(frame)

# Código para prueba independiente
if __name__ == "__main__":
    cv2.namedWindow('Snake')
    
    while True:
        frame = get_frame()
        cv2.imshow('Snake', frame)
        
        key = cv2.waitKey(1) & 0xFF
        if key == 27:  # Esc
            break
        handle_key(key)
    
    cv2.destroyAllWindows()