import cv2
import numpy as np
import random
import time

class Tetris:
    def __init__(self):
        # Ajustar dimensiones para la pantalla de la consola (260x140)
        self.width = 8  # Reducido de 10 a 8 para que quepa en la pantalla
        self.height = 12  # Reducido de 20 a 12 para que quepa en la pantalla
        self.block_size = 10  # Reducido para ajustarse al tamaño de la pantalla
        self.grid = np.zeros((self.height, self.width), dtype=int)
        
        # Colores ajustados para mejor visibilidad en pantalla pequeña
        self.colors = {
            0: (20, 20, 20),     # Fondo más oscuro
            1: (255, 50, 50),    # Rojo
            2: (50, 255, 50),    # Verde
            3: (50, 50, 255),    # Azul
            4: (255, 255, 50),   # Amarillo
            5: (255, 50, 255),   # Magenta
            6: (50, 255, 255),   # Cyan
            7: (200, 200, 200),  # Gris más claro
        }
        
        self.tetrominos = {
            'I': [(0, 0), (0, 1), (0, 2), (0, 3)],
            'O': [(0, 0), (0, 1), (1, 0), (1, 1)],
            'T': [(0, 1), (1, 0), (1, 1), (1, 2)],
            'L': [(0, 2), (1, 0), (1, 1), (1, 2)],
            'J': [(0, 0), (1, 0), (1, 1), (1, 2)],
            'S': [(0, 1), (0, 2), (1, 0), (1, 1)],
            'Z': [(0, 0), (0, 1), (1, 1), (1, 2)]
        }
        
        self.current_piece = None
        self.current_pos = None
        self.current_color = None
        self.next_piece = None
        self.next_piece_type = None
        self.next_color = None
        self.game_over = False
        self.score = 0
        self.level = 1
        self.lines_cleared_total = 0
        self.last_move_time = time.time()
        self.move_interval = 0.5
    
    def new_piece(self):
        if self.next_piece is None:
            self.generate_next_piece()
        
        self.current_piece = self.next_piece
        self.current_color = self.next_color
        pos = [0, self.width // 2 - 2]
        
        self.generate_next_piece()
        
        if self.check_collision(self.current_piece, pos):
            self.game_over = True
        else:
            self.current_pos = pos
            self.last_move_time = time.time()

    def generate_next_piece(self):
        self.next_piece_type = random.choice(list(self.tetrominos.keys()))
        self.next_piece = self.tetrominos[self.next_piece_type]
        self.next_color = random.randint(1, 7)
    
    def check_collision(self, piece, pos):
        for p in piece:
            row = pos[0] + p[0]
            col = pos[1] + p[1]
            if row >= self.height or col < 0 or col >= self.width:
                return True
            if row >= 0 and self.grid[row][col] != 0:
                return True
        return False
    
    def merge_piece(self):
        for p in self.current_piece:
            row = self.current_pos[0] + p[0]
            col = self.current_pos[1] + p[1]
            if row >= 0:
                self.grid[row][col] = self.current_color
    
    def move(self, delta_row, delta_col):
        new_pos = [self.current_pos[0] + delta_row, self.current_pos[1] + delta_col]
        if not self.check_collision(self.current_piece, new_pos):
            self.current_pos = new_pos
            return True
        return False
    
    def rotate(self):
        rotated_piece = [(p[1], -p[0]) for p in self.current_piece]
        if not self.check_collision(rotated_piece, self.current_pos):
            self.current_piece = rotated_piece
    
    def clear_lines(self):
        lines_cleared = 0
        for i in range(self.height):
            if all(self.grid[i]):
                self.grid = np.delete(self.grid, i, 0)
                self.grid = np.vstack([np.zeros(self.width), self.grid])
                lines_cleared += 1
        
        self.lines_cleared_total += lines_cleared
        self.level = self.lines_cleared_total // 5 + 1  # Cambiado a 5 líneas por nivel
        
        if lines_cleared > 0:
            self.score += 100 * lines_cleared * self.level
        
        return lines_cleared
    
    def update(self):
        if self.game_over:
            return
            
        if self.current_piece is None:
            self.new_piece()
            return
            
        current_time = time.time()
        if current_time - self.last_move_time > self.move_interval:
            if not self.move(1, 0):
                self.merge_piece()
                self.clear_lines()
                self.current_piece = None
            self.last_move_time = current_time
            self.move_interval = max(0.1, 0.5 - 0.05 * (self.level - 1))
    
    def draw(self):
        # Crear el frame con las dimensiones correctas (260x140)
        frame = np.zeros((140, 260, 3), dtype=np.uint8)
        
        # Calcular offset para centrar el juego
        offset_x = 80
        offset_y = 10
        
        # Dibujar marco del juego
        cv2.rectangle(frame,
                     (offset_x - 1, offset_y - 1),
                     (offset_x + self.width * self.block_size + 1,
                      offset_y + self.height * self.block_size + 1),
                     (128, 128, 128), 1)
        
        # Dibujar grid
        for y in range(self.height):
            for x in range(self.width):
                color = self.colors[self.grid[y][x]]
                cv2.rectangle(frame,
                            (offset_x + x * self.block_size,
                             offset_y + y * self.block_size),
                            (offset_x + (x + 1) * self.block_size - 1,
                             offset_y + (y + 1) * self.block_size - 1),
                            color, -1)
        
        # Dibujar pieza actual
        if self.current_piece:
            for p in self.current_piece:
                row = self.current_pos[0] + p[0]
                col = self.current_pos[1] + p[1]
                if row >= 0:
                    cv2.rectangle(frame,
                                (offset_x + col * self.block_size,
                                 offset_y + row * self.block_size),
                                (offset_x + (col + 1) * self.block_size - 1,
                                 offset_y + (row + 1) * self.block_size - 1),
                                self.colors[self.current_color], -1)
        
        # Dibujar información del juego
        cv2.putText(frame, f"Score: {self.score}",
                    (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1)
        cv2.putText(frame, f"Level: {self.level}",
                    (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1)
        
        # Dibujar siguiente pieza
        next_offset_x = offset_x + self.width * self.block_size + 20
        next_offset_y = offset_y
        cv2.putText(frame, "Next:",
                    (next_offset_x, next_offset_y), cv2.FONT_HERSHEY_SIMPLEX,
                    0.4, (255, 255, 255), 1)
        
        if self.next_piece:
            for p in self.next_piece:
                cv2.rectangle(frame,
                            (next_offset_x + p[1] * self.block_size,
                             next_offset_y + 10 + p[0] * self.block_size),
                            (next_offset_x + (p[1] + 1) * self.block_size - 1,
                             next_offset_y + 10 + (p[0] + 1) * self.block_size - 1),
                            self.colors[self.next_color], -1)
        
        # Dibujar mensaje de game over
        if self.game_over:
            cv2.putText(frame, "GAME OVER",
                        (offset_x + 10, 70), cv2.FONT_HERSHEY_SIMPLEX,
                        0.5, (255, 255, 255), 1)
            cv2.putText(frame, "Press R to restart",
                        (offset_x, 90), cv2.FONT_HERSHEY_SIMPLEX,
                        0.4, (255, 255, 255), 1)
        
        return frame

# Variables globales para el estado del juego
_tetris_game = None

def handle_key(key):
    global _tetris_game
    
    if _tetris_game.game_over:
        if key == ord('r'):
            _tetris_game = Tetris()
        return
    
    if key == ord('a') or key == 81:  # A o flecha izquierda
        _tetris_game.move(0, -1)
    elif key == ord('d') or key == 83:  # D o flecha derecha
        _tetris_game.move(0, 1)
    elif key == ord('w') or key == 82:  # W o flecha arriba
        _tetris_game.rotate()
    elif key == ord('s') or key == 84:  # S o flecha abajo
        _tetris_game.move(1, 0)
    elif key == 32:  # Espacio (caída rápida)
        while _tetris_game.move(1, 0):
            pass
        _tetris_game.merge_piece()
        _tetris_game.clear_lines()
        _tetris_game.current_piece = None

def get_frame():
    global _tetris_game
    
    if _tetris_game is None:
        _tetris_game = Tetris()
    
    _tetris_game.update()
    return _tetris_game.draw()

# Para pruebas independientes
if __name__ == "__main__":
    cv2.namedWindow('Tetris')
    _tetris_game = Tetris()
    
    while True:
        frame = get_frame()
        cv2.imshow('Tetris', frame)
        
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        handle_key(key)
    
    cv2.destroyAllWindows()