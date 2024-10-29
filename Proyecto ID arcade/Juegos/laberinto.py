import cv2
import numpy as np

class MazeGame:
    def __init__(self):
        # Dimensiones del lienzo (pantalla)
        self.width = 300
        self.height = 150
        self.player_size = 10
        self.player_x = 10
        self.player_y = 10
        self.player_speed = 5
        
        # Laberinto representado por líneas (coordenadas de las paredes)
        self.walls = [
            ((0, 0), (0, self.height)),       # Izquierda
            ((0, 0), (self.width, 0)),       # Arriba
            ((self.width, 0), (self.width, self.height)),  # Derecha
            ((0, self.height), (self.width, self.height)),  # Abajo
            ((50, 30), (50, 120)),            # Pared vertical
            ((50, 30), (200, 30)),            # Pared horizontal
            ((200, 30), (200, 60)),            # Pared vertical
            ((50, 60), (200, 60)),            # Pared horizontal
            ((50, 120), (150, 120)),          # Pared horizontal
        ]
        
        # Meta
        self.goal_x = 260
        self.goal_y = 120
        
        # Estado del juego
        self.game_over = False
    
    def move_player(self, direction_x, direction_y):
        # Calcular nueva posición
        new_x = self.player_x + direction_x * self.player_speed
        new_y = self.player_y + direction_y * self.player_speed
        
        # Verificar colisiones
        if not self.check_collision(new_x, self.player_y):
            self.player_x = new_x
        if not self.check_collision(self.player_x, new_y):
            self.player_y = new_y

    def check_collision(self, x, y):
        # Verifica si el jugador colisiona con alguna pared
        for wall in self.walls:
            pt1, pt2 = wall
            if pt1[0] <= x <= pt2[0] and pt1[1] <= y <= pt2[1]:
                return True
            if pt1[0] <= x + self.player_size <= pt2[0] and pt1[1] <= y <= pt2[1]:
                return True
            if pt1[0] <= x <= pt2[0] and pt1[1] <= y + self.player_size <= pt2[1]:
                return True
            if pt1[0] <= x + self.player_size <= pt2[0] and pt1[1] <= y + self.player_size <= pt2[1]:
                return True
        return False
    
    def check_goal(self):
        # Verifica si el jugador ha alcanzado la meta
        if (self.goal_x < self.player_x < self.goal_x + self.player_size or 
            self.goal_x < self.player_x + self.player_size < self.goal_x + self.player_size) and \
           (self.goal_y < self.player_y < self.goal_y + self.player_size or 
            self.goal_y < self.player_y + self.player_size < self.goal_y + self.player_size):
            self.game_over = True
    
    def draw(self, frame):
        # Limpiar el frame (llenarlo con el color de fondo)
        frame[:] = (0, 0, 0)  # Color de fondo negro
        
        # Dibujar las paredes del laberinto
        for wall in self.walls:
            pt1, pt2 = wall
            cv2.line(frame, pt1, pt2, (255, 255, 255), 2)
        
        # Dibujar al jugador
        cv2.rectangle(frame,
                      (int(self.player_x), int(self.player_y)),
                      (int(self.player_x + self.player_size), int(self.player_y + self.player_size)),
                      (0, 255, 0), -1)  # Verde
        
        # Dibujar la meta
        cv2.rectangle(frame,
                      (self.goal_x, self.goal_y),
                      (self.goal_x + self.player_size, self.goal_y + self.player_size),
                      (255, 0, 0), -1)  # Rojo
        
        # Mensaje de fin del juego
        if self.game_over:
            cv2.putText(frame, "¡Has ganado!", (80, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        
        return frame

# Variables globales para el estado del juego
_game = None

def handle_key(key):
    global _game
    
    if _game.game_over:
        return
    
    if key == ord('a') or key == 81:  # A o flecha izquierda
        _game.move_player(-1 * _game.player_speed, 0)
    elif key == ord('d') or key == 83:  # D o flecha derecha
        _game.move_player(1 * _game.player_speed, 0)
    elif key == ord('w') or key == 82:  # W o flecha arriba
        _game.move_player(0, -1 * _game.player_speed)
    elif key == ord('s') or key == 84:  # S o flecha abajo
        _game.move_player(0, 1 * _game.player_speed)

def get_frame():
    global _game
    
    if _game is None:
        _game = MazeGame()
    
    # Crea el frame en blanco
    frame = np.zeros((150, 300, 3), dtype=np.uint8)
    _game.check_goal()  # Verifica si se ha alcanzado la meta
    return _game.draw(frame)

# Para pruebas independientes
if __name__ == "__main__":
    cv2.namedWindow('Maze Game')
    _game = MazeGame()
    
    while True:
        frame = get_frame()
        cv2.imshow('Maze Game', frame)
        
        key = cv2.waitKey(1) & 0xFF
        if key == 27:  # Esc para salir
            break
        handle_key(key)
    
    cv2.destroyAllWindows()
