import cv2
import numpy as np
import pygame
import random

# Inicializar pygame y el joystick
pygame.init()
pygame.joystick.init()
joystick = pygame.joystick.Joystick(0)
joystick.init()

# Configuración del juego
width, height = 800, 600
paddle_width, paddle_height = 100, 10
ball_radius = 10
brick_width, brick_height = 60, 20
brick_rows, brick_cols = 5, 10

# Colores
WHITE = (255, 255, 255)
RED = (0, 0, 255)  # OpenCV usa BGR
BLUE = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (0, 255, 255)

# Inicializar objetos del juego
paddle = [width//2 - paddle_width//2, height - 30, paddle_width, paddle_height]
ball = [float(width//2), float(height//2), 1.0, -1.0]  # x, y, dx, dy (usando flotantes)
bricks = []
for i in range(brick_rows):
    for j in range(brick_cols):
        bricks.append([j * (brick_width + 5) + 5, i * (brick_height + 5) + 5, brick_width, brick_height])

# Power-ups
POWERUP_TYPES = ["expand", "shrink", "slow", "fast"]
powerups = []

# Variable para el movimiento continuo de la paleta
paddle_speed = 0

# Función para dibujar los objetos
def draw_objects(frame):
    cv2.rectangle(frame, (int(paddle[0]), paddle[1]), (int(paddle[0] + paddle[2]), paddle[1] + paddle[3]), GREEN, -1)
    cv2.circle(frame, (int(ball[0]), int(ball[1])), ball_radius, WHITE, -1)
    for brick in bricks:
        cv2.rectangle(frame, (brick[0], brick[1]), (brick[0] + brick[2], brick[1] + brick[3]), RED, -1)
    for powerup in powerups:
        cv2.circle(frame, (int(powerup[0]), int(powerup[1])), 5, YELLOW, -1)

# Función para crear power-ups
def create_powerup(x, y):
    if random.random() < 0.2:  # 20% de probabilidad de crear un power-up
        powerup_type = random.choice(POWERUP_TYPES)
        powerups.append([float(x), float(y), powerup_type])

# Función para aplicar power-ups
def apply_powerup(powerup_type):
    global paddle, ball
    if powerup_type == "expand":
        paddle[2] = min(paddle[2] + 20, width // 2)
    elif powerup_type == "shrink":
        paddle[2] = max(paddle[2] - 20, 40)
    elif powerup_type == "slow":
        ball[2] = max(ball[2] / 2, 0.5) if ball[2] != 0 else -0.5
        ball[3] = max(ball[3] / 2, 0.5) if ball[3] != 0 else -0.5
    elif powerup_type == "fast":
        ball[2] = ball[2] * 2 if abs(ball[2]) < 2 else ball[2]
        ball[3] = ball[3] * 2 if abs(ball[3]) < 2 else ball[3]

# Contador de frames para ralentizar el juego
frame_count = 0

# Bucle principal del juego
while True:
    frame_count += 1
    if frame_count % 6 != 0:  # Procesar cada seis frames para ralentizar mucho más
        continue

    frame = np.zeros((height, width, 3), dtype=np.uint8)
    
    # Manejar eventos del joystick
    for event in pygame.event.get():
        if event.type == pygame.JOYAXISMOTION:
            if event.axis == 0:  # Eje X
                paddle_speed = event.value * 5  # Ajusta la sensibilidad aquí

    # Mover la paleta continuamente
    paddle[0] += paddle_speed
    paddle[0] = max(0, min(width - paddle[2], paddle[0]))

    # Mover la pelota (ahora con movimiento fraccionario)
    ball[0] += ball[2] / 2  # Mover la mitad de la velocidad actual
    ball[1] += ball[3] / 2
    
    # Colisiones con los bordes
    if int(ball[0]) <= ball_radius or int(ball[0]) >= width - ball_radius:
        ball[2] = -ball[2]
    if int(ball[1]) <= ball_radius:
        ball[3] = -ball[3]
    if int(ball[1]) >= height - ball_radius:
        break  # Fin del juego

    # Colisión con la paleta
    if int(ball[1]) + ball_radius >= paddle[1] and int(paddle[0]) <= int(ball[0]) <= int(paddle[0]) + paddle[2]:
        ball[3] = -abs(ball[3])

    # Colisión con los ladrillos y power-ups
    for brick in bricks[:]:
        if (brick[0] <= int(ball[0]) <= brick[0] + brick_width and
            brick[1] <= int(ball[1]) <= brick[1] + brick_height):
            ball[3] = -ball[3]
            bricks.remove(brick)
            create_powerup(brick[0] + brick_width // 2, brick[1] + brick_height)
            break

    # Mover y aplicar power-ups
    for powerup in powerups[:]:
        powerup[1] += 1  # Mover power-up hacia abajo más lentamente
        if int(powerup[1]) >= height:
            powerups.remove(powerup)
        elif (int(paddle[0]) <= int(powerup[0]) <= int(paddle[0]) + paddle[2] and
              paddle[1] <= int(powerup[1]) <= paddle[1] + paddle_height):
            apply_powerup(powerup[2])
            powerups.remove(powerup)

    # Dibujar objetos
    draw_objects(frame)

    # Mostrar el frame
    cv2.imshow('Atari Breakout', frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
pygame.quit()