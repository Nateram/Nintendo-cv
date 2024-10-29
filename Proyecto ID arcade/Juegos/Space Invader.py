import cv2
import numpy as np
import random
from time import time

class SpaceInvaders:
    def __init__(self):
        # Dimensiones de la pantalla
        self.width = 260
        self.height = 140
        self.block_size = 10
        
        # Colores
        self.colors = {
            'background': (20, 20, 20),    # Gris oscuro
            'player': (0, 255, 0),         # Verde
            'invader': (255, 0, 0),        # Rojo
            'bullet': (255, 255, 255),     # Blanco
            'text': (255, 255, 255)        # Blanco
        }
        
        # Jugador
        self.player_width = 20
        self.player_height = 10
        self.player_x = self.width // 2 - self.player_width // 2
        self.player_y = self.height - 20
        self.player_speed = 5
        
        # Invasores
        self.invader_rows = 3
        self.invaders_per_row = 6
        self.invader_width = 15
        self.invader_height = 10
        self.invader_spacing = 25
        self.invader_speed = 1
        self.invader_direction = 1
        self.invader_drop = 10
        self.initialize_invaders()
        
        # Disparos
        self.bullets = []
        self.bullet_speed = 4
        self.bullet_width = 2
        self.bullet_height = 5
        self.last_shot_time = 0
        self.shot_cooldown = 0.5
        
        # Estado del juego
        self.score = 0
        self.game_over = False
        self.last_update = time()
        self.update_interval = 0.016  # ~60 FPS
    
    def initialize_invaders(self):
        self.invaders = []
        start_x = (self.width - (self.invaders_per_row * self.invader_spacing)) // 2
        start_y = 30
        
        for row in range(self.invader_rows):
            for col in range(self.invaders_per_row):
                x = start_x + col * self.invader_spacing
                y = start_y + row * self.invader_spacing
                self.invaders.append({
                    'x': x,
                    'y': y,
                    'alive': True
                })
    
    def move_player(self, direction):
        new_x = self.player_x + direction * self.player_speed
        if 0 <= new_x <= self.width - self.player_width:
            self.player_x = new_x
    
    def shoot(self):
        current_time = time()
        if current_time - self.last_shot_time >= self.shot_cooldown:
            self.bullets.append({
                'x': self.player_x + self.player_width // 2 - self.bullet_width // 2,
                'y': self.player_y,
                'active': True
            })
            self.last_shot_time = current_time
    
    def update_bullets(self):
        for bullet in self.bullets:
            if bullet['active']:
                bullet['y'] -= self.bullet_speed
                
                # Verificar colisiones con invasores
                for invader in self.invaders:
                    if invader['alive']:
                        if (bullet['x'] < invader['x'] + self.invader_width and
                            bullet['x'] + self.bullet_width > invader['x'] and
                            bullet['y'] < invader['y'] + self.invader_height and
                            bullet['y'] + self.bullet_height > invader['y']):
                            invader['alive'] = False
                            bullet['active'] = False
                            self.score += 100
                            break
                
                # Eliminar balas fuera de pantalla
                if bullet['y'] < 0:
                    bullet['active'] = False
        
        # Limpiar balas inactivas
        self.bullets = [b for b in self.bullets if b['active']]
    
    def update_invaders(self):
        move_down = False
        min_x = min(invader['x'] for invader in self.invaders if invader['alive'])
        max_x = max(invader['x'] for invader in self.invaders if invader['alive'])
        
        # Verificar si los invasores deben cambiar de dirección
        if max_x + self.invader_width >= self.width or min_x <= 0:
            self.invader_direction *= -1
            move_down = True
        
        # Mover invasores
        for invader in self.invaders:
            if invader['alive']:
                invader['x'] += self.invader_speed * self.invader_direction
                if move_down:
                    invader['y'] += self.invader_drop
                
                # Verificar game over (invasores llegan abajo o colisionan con jugador)
                if (invader['y'] + self.invader_height >= self.player_y or
                    (invader['x'] < self.player_x + self.player_width and
                     invader['x'] + self.invader_width > self.player_x and
                     invader['y'] < self.player_y + self.player_height and
                     invader['y'] + self.invader_height > self.player_y)):
                    self.game_over = True
    
    def update(self):
        if self.game_over:
            return
            
        current_time = time()
        if current_time - self.last_update >= self.update_interval:
            self.update_bullets()
            self.update_invaders()
            self.last_update = current_time
            
            # Verificar victoria
            if not any(invader['alive'] for invader in self.invaders):
                self.initialize_invaders()
                self.invader_speed += 0.5
    
    def draw(self, frame):
        # Limpiar frame
        frame.fill(self.colors['background'][0])
        
        # Dibujar jugador
        cv2.rectangle(frame,
                     (self.player_x, self.player_y),
                     (self.player_x + self.player_width, self.player_y + self.player_height),
                     self.colors['player'], -1)
        
        # Dibujar invasores
        for invader in self.invaders:
            if invader['alive']:
                cv2.rectangle(frame,
                            (int(invader['x']), int(invader['y'])),
                            (int(invader['x'] + self.invader_width),
                             int(invader['y'] + self.invader_height)),
                            self.colors['invader'], -1)
        
        # Dibujar balas
        for bullet in self.bullets:
            cv2.rectangle(frame,
                        (bullet['x'], bullet['y']),
                        (bullet['x'] + self.bullet_width,
                         bullet['y'] + self.bullet_height),
                        self.colors['text'], -1)
        
        # Dibujar puntaje
        cv2.putText(frame, f'Score: {self.score}',
                    (5, 15), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                    self.colors['text'], 1, cv2.LINE_AA)
        
        # Dibujar mensaje de game over
        if self.game_over:
            text = 'GAME OVER - Press R to restart'
            text_size = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)[0]
            text_x = (self.width - text_size[0]) // 2
            text_y = self.height // 2
            cv2.putText(frame, text,
                       (text_x, text_y),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                       self.colors['text'], 1, cv2.LINE_AA)
        
        return frame

# Variables globales para el estado del juego
_game = None

def handle_key(key):
    global _game
    
    if _game.game_over:
        if key == ord('r'):
            _game = SpaceInvaders()
        return
    
    if key == ord('a') or key == 81:  # A o flecha izquierda
        _game.move_player(-1)
    elif key == ord('d') or key == 83:  # D o flecha derecha
        _game.move_player(1)
    elif key == ord(' '):  # Espacio para disparar
        _game.shoot()

def get_frame():
    global _game
    
    if _game is None:
        _game = SpaceInvaders()
    
    frame = np.zeros((_game.height, _game.width, 3), dtype=np.uint8)
    _game.update()
    return _game.draw(frame)

# Para pruebas independientes
if __name__ == "__main__":
    cv2.namedWindow('Space Invaders')
    _game = SpaceInvaders()
    
    while True:
        frame = get_frame()
        cv2.imshow('Space Invaders', frame)
        
        key = cv2.waitKey(1) & 0xFF
        if key == 27:  # Esc para salir
            break
        handle_key(key)
    
    cv2.destroyAllWindows()