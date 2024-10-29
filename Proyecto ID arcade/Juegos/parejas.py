import cv2
import numpy as np
import random
import os
from time import time

class MemoryGame:
    def __init__(self):
        # Dimensiones del tablero y las cartas
        self.ROWS, self.COLS = 3, 6  # Cambiado de 4x4 a 3x6
        self.CARD_WIDTH, self.CARD_HEIGHT = 80, 80
        self.CARD_SPACING = 5

        # Definición de colores
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.GREEN = (0, 255, 0)
        self.BLUE = (255, 0, 0)
        self.RED = (0, 0, 255)
        self.YELLOW = (0, 255, 255)

        # Calcular dimensiones del tablero
        board_width = self.COLS * (self.CARD_WIDTH + self.CARD_SPACING) - self.CARD_SPACING
        board_height = self.ROWS * (self.CARD_HEIGHT + self.CARD_SPACING) - self.CARD_SPACING

        # Tamaño de la ventana ajustado para acomodar las cartas más grandes
        self.width = board_width + 20   # 20 píxeles de margen a cada lado
        self.height = board_height + 20  # 20 píxeles de margen arriba y abajo

        # Variables de estado del juego
        self.first_card = None
        self.second_card = None
        self.pairs_found = 0
        self.game_over = False
        self.selectable = True

        # Variables para animación
        self.animation_start = 0
        self.animation_duration = 0.5  # segundos
        self.is_animating = False
        self.animation_cards = []
        self.animation_type = None  # 'flip' o 'hide'
        self.waiting_to_hide = False
        self.hide_start_time = 0
        self.hide_delay = 1.0  # 1 segundo de espera

        # Posición del cursor
        self.cursor_row, self.cursor_col = 0, 0

        # Cargar imágenes
        self.image_folder = 'cartas'
        self.images = self.load_images(self.image_folder)
        self.back_image = cv2.imread('CartaAtras.png')
        self.back_image = cv2.resize(self.back_image, (self.CARD_WIDTH, self.CARD_HEIGHT))

        # Inicializar el tablero
        self.board, self.flipped, self.images = self.initialize_game(self.images)

    def load_images(self, image_folder):
        images = []
        for filename in os.listdir(image_folder):
            img_path = os.path.join(image_folder, filename)
            img = cv2.imread(img_path)
            if img is not None:
                img = cv2.resize(img, (self.CARD_WIDTH, self.CARD_HEIGHT))
                images.append(img)
        return images

    def center_board(self):
        margin_x = (self.width - self.COLS * (self.CARD_WIDTH + self.CARD_SPACING)) // 2
        margin_y = (self.height - self.ROWS * (self.CARD_HEIGHT + self.CARD_SPACING)) // 2
        return margin_x, margin_y

    def create_board(self, rows, cols, images):
        num_pairs = (rows * cols) // 2
        if len(images) < num_pairs:
            print(f"Error: Necesitas al menos {num_pairs} imágenes diferentes.")
            exit()

        selected_images = random.sample(images, num_pairs)
        card_indices = list(range(num_pairs)) * 2
        random.shuffle(card_indices)

        return np.array(card_indices).reshape((rows, cols)), selected_images

    def initialize_game(self, images):
        board, selected_images = self.create_board(self.ROWS, self.COLS, images)
        return board, np.zeros((self.ROWS, self.COLS), dtype=bool), selected_images

    def start_animation(self, animation_type, cards):
        self.animation_start = time()
        self.is_animating = True
        self.animation_type = animation_type
        self.animation_cards = cards
        self.selectable = False

    def update_animation(self):
        current_time = time()
        
        # Si estamos esperando para ocultar las cartas
        if self.waiting_to_hide and current_time - self.hide_start_time >= self.hide_delay:
            self.waiting_to_hide = False
            self.start_animation('hide', [self.first_card, self.second_card])
            
        # Actualizar animación en curso
        if self.is_animating:
            progress = (current_time - self.animation_start) / self.animation_duration

            if progress >= 1:
                self.is_animating = False
                self.selectable = True
                
                if self.animation_type == 'hide':
                    for row, col in self.animation_cards:
                        self.flipped[row, col] = False
                    self.first_card = None
                    self.second_card = None

    def update(self):
        if self.game_over:
            return

        self.update_animation()

        if self.pairs_found == (self.ROWS * self.COLS) // 2:
            self.game_over = True

    def select_card(self):
        if not self.flipped[self.cursor_row, self.cursor_col] and self.selectable and not self.is_animating:
            # Iniciar animación de volteo
            self.start_animation('flip', [(self.cursor_row, self.cursor_col)])
            self.flipped[self.cursor_row, self.cursor_col] = True

            if self.first_card is None:
                self.first_card = (self.cursor_row, self.cursor_col)
            else:
                self.second_card = (self.cursor_row, self.cursor_col)
                card1 = self.board[self.first_card[0], self.first_card[1]]
                card2 = self.board[self.second_card[0], self.second_card[1]]

                if card1 == card2:
                    self.pairs_found += 1
                    self.first_card, self.second_card = None, None
                else:
                    # Iniciar el temporizador de espera
                    self.waiting_to_hide = True
                    self.hide_start_time = time()
                    self.selectable = False

    def draw_card(self, frame, card_pos, card_image, show_back=True):
        row, col = card_pos
        margin_x, margin_y = self.center_board()
        x = margin_x + col * (self.CARD_WIDTH + self.CARD_SPACING)
        y = margin_y + row * (self.CARD_HEIGHT + self.CARD_SPACING)

        if self.is_animating and (row, col) in self.animation_cards:
            progress = (time() - self.animation_start) / self.animation_duration
            if self.animation_type == 'flip':
                if progress < 0.5:
                    # Primera mitad de la animación: mostrar carta volteándose
                    scale = 1 - progress * 2
                    if scale > 0:
                        scaled_width = max(1, int(self.CARD_WIDTH * scale))
                        scaled_image = cv2.resize(self.back_image, (scaled_width, self.CARD_HEIGHT))
                        offset_x = x + (self.CARD_WIDTH - scaled_width) // 2
                        frame[y:y + self.CARD_HEIGHT, offset_x:offset_x + scaled_width] = scaled_image
                else:
                    # Segunda mitad: mostrar carta nueva
                    scale = (progress - 0.5) * 2
                    if scale > 0:
                        scaled_width = max(1, int(self.CARD_WIDTH * scale))
                        scaled_image = cv2.resize(card_image, (scaled_width, self.CARD_HEIGHT))
                        offset_x = x + (self.CARD_WIDTH - scaled_width) // 2
                        frame[y:y + self.CARD_HEIGHT, offset_x:offset_x + scaled_width] = scaled_image
            elif self.animation_type == 'hide':
                if progress < 0.5:
                    scale = 1 - progress * 2
                else:
                    scale = (progress - 0.5) * 2
                    show_back = True
                if scale > 0:
                    scaled_width = max(1, int(self.CARD_WIDTH * scale))
                    scaled_image = cv2.resize(self.back_image if show_back else card_image, 
                                           (scaled_width, self.CARD_HEIGHT))
                    offset_x = x + (self.CARD_WIDTH - scaled_width) // 2
                    frame[y:y + self.CARD_HEIGHT, offset_x:offset_x + scaled_width] = scaled_image
        else:
            frame[y:y + self.CARD_HEIGHT, x:x + self.CARD_WIDTH] = (
                self.back_image if show_back else card_image
            )

        return frame

    def draw(self, frame):
        frame.fill(0)
        margin_x, margin_y = self.center_board()
        
        # Dibujar todas las cartas
        for i in range(self.ROWS):
            for j in range(self.COLS):
                card_image = self.images[self.board[i, j]]
                show_back = not self.flipped[i, j]
                frame = self.draw_card(frame, (i, j), card_image, show_back)

                # Dibujar cursor
                if i == self.cursor_row and j == self.cursor_col:
                    x = margin_x + j * (self.CARD_WIDTH + self.CARD_SPACING)
                    y = margin_y + i * (self.CARD_HEIGHT + self.CARD_SPACING)
                    cv2.rectangle(frame, (x, y), 
                                (x + self.CARD_WIDTH, y + self.CARD_HEIGHT), 
                                self.YELLOW, 2)

        if self.game_over:
            cv2.putText(frame, '¡Has ganado!', (50, self.height // 2), 
                       cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 3)

        return frame

# Variables globales para el estado del juego
_memory_game = None

def handle_key(key):
    global _memory_game
    if _memory_game and not _memory_game.is_animating and not _memory_game.waiting_to_hide:
        if key in [ord('a'), 81, 2]:  # A o flecha izquierda
            if _memory_game.cursor_col > 0:
                _memory_game.cursor_col -= 1
        elif key in [ord('d'), 83, 3]:  # D o flecha derecha
            if _memory_game.cursor_col < _memory_game.COLS - 1:
                _memory_game.cursor_col += 1
        elif key in [ord('w'), 82, 0]:  # W o flecha arriba
            if _memory_game.cursor_row > 0:
                _memory_game.cursor_row -= 1
        elif key in [ord('s'), 84, 1]:  # S o flecha abajo
            if _memory_game.cursor_row < _memory_game.ROWS - 1:
                _memory_game.cursor_row += 1
        elif key == 13:  # Enter
            _memory_game.select_card()
        elif key == ord('r') and _memory_game.game_over:  # R para reiniciar
            _memory_game = MemoryGame()

def get_frame():
    global _memory_game
    
    if _memory_game is None:
        _memory_game = MemoryGame()
    
    _memory_game.update()
    
    frame = np.zeros((_memory_game.height, _memory_game.width, 3), dtype=np.uint8)
    return _memory_game.draw(frame)

# Código para prueba independiente
if __name__ == "__main__":
    cv2.namedWindow('Memory Game')
    
    while True:
        frame = get_frame()
        cv2.imshow('Memory Game', frame)
        
        key = cv2.waitKey(1) & 0xFF
        if key == 27:  # Esc
            break
        handle_key(key)
    
    cv2.destroyAllWindows()