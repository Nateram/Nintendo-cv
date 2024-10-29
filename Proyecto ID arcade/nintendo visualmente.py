import cv2
import numpy as np

# Crear una imagen en blanco (canvas) con nuevas dimensiones
image = np.zeros((700, 800, 3), dtype=np.uint8)

# Colores
blue = (240, 130, 30)         # Azul más oscuro (Steel Blue)
dark_blue = (30, 60, 100)     # Azul oscuro (más profundo)
black = (0, 0, 0)             # Marco (sin cambios)
dark_gray = (20, 20, 20)      # Pantalla oscura (más profundo)
light_blue = (173, 216, 230)  # Azul claro (Light Blue)
dark_text = (40, 40, 40)      # Texto oscuro (más suave)
light_gray = (211, 211, 211) # Gris claro (Light Gray)
medium_gray = (169, 169, 169) # Gris medio (Dark Gray)
dark_gray_btn = (60, 60, 60)  # Botones oscuros (más sutil)
cyan = (0, 191, 255)        # Cian brillante (Deep Sky Blue)
dark_cyan = (0, 139, 139)   # Cian oscuro (Dark Cyan)
white = (255, 255, 255)     # Blanco (sin cambios)

# Redimensionar escalas
scale_x = 800 / 400
scale_y = 700 / 400

# Dibujar carcasa superior
cv2.rectangle(image, (int(50 * scale_x), int(20 * scale_y)), (int(350 * scale_x), int(200 * scale_y)), blue, -1)

# Dibujar marco de la pantalla superior
cv2.rectangle(image, (int(60 * scale_x), int(30 * scale_y)), (int(340 * scale_x), int(190 * scale_y)), black, -1)

# Dibujar pantalla superior
cv2.rectangle(image, (int(70 * scale_x), int(40 * scale_y)), (int(330 * scale_x), int(180 * scale_y)), dark_gray, -1)

# Dibujar altavoces superiores
for i, x in enumerate([80, 90, 100]):
    cv2.circle(image, (int(x * scale_x), int(35 * scale_y)), int(2 * scale_x), light_blue, -1)

# Dibujar cámara
cv2.circle(image, (int(320 * scale_x), int(35 * scale_y)), int(3 * scale_x), light_blue, -1)

# Dibujar bisagra (más grande)
cv2.ellipse(image, (int(200 * scale_x), int(202 * scale_y)), (int(130 * scale_x), int(5 * scale_y)), 0, 0, 180, light_blue, -1)

# Dibujar carcasa inferior
cv2.rectangle(image, (int(50 * scale_x), int(205 * scale_y)), (int(350 * scale_x), int(385 * scale_y)), blue, -1)

# Dibujar marco de la pantalla inferior
cv2.rectangle(image, (int(115 * scale_x), int(215 * scale_y)), (int(285 * scale_x), int(355 * scale_y)), black, -1)

# Dibujar pantalla inferior
cv2.rectangle(image, (int(125 * scale_x), int(225 * scale_y)), (int(275 * scale_x), int(345 * scale_y)), dark_gray, -1)

# Dibujar Circle Pad
cv2.circle(image, (int(81 * scale_x), int(260 * scale_y)), int(18 * scale_x), light_blue, -1)

# Dibujar D-Pad (ajustado)
points = np.array([[65, 307], [75, 307], [75, 297], [85, 297], [85, 307], [95, 307],
                   [95, 317], [85, 317], [85, 327], [75, 327], [75, 317], [65, 317]], np.int32)
points = (points * [scale_x, scale_y]).astype(np.int32)
cv2.fillPoly(image, [points], light_blue)

# Dibujar botones A B X Y
offset_x = 25
cv2.circle(image, (int((290 + offset_x) * scale_x), int(273 * scale_y)), int(8 * scale_x), light_blue, -1)  # X
cv2.circle(image, (int((270 + offset_x) * scale_x), int(293 * scale_y)), int(8 * scale_x), light_blue, -1)  # Y
cv2.circle(image, (int((310 + offset_x) * scale_x), int(293 * scale_y)), int(8 * scale_x), light_blue, -1)  # A
cv2.circle(image, (int((290 + offset_x) * scale_x), int(313 * scale_y)), int(8 * scale_x), light_blue, -1)  # B

# Dibujar texto de los botones A B X Y
cv2.putText(image, 'X', (int((285 + offset_x) * scale_x), int(277 * scale_y)), cv2.FONT_HERSHEY_SIMPLEX, 0.3 * scale_x, black, 1, cv2.LINE_AA)
cv2.putText(image, 'Y', (int((265 + offset_x) * scale_x), int(297 * scale_y)), cv2.FONT_HERSHEY_SIMPLEX, 0.3 * scale_x, black, 1, cv2.LINE_AA)
cv2.putText(image, 'A', (int((305 + offset_x) * scale_x), int(297 * scale_y)), cv2.FONT_HERSHEY_SIMPLEX, 0.3 * scale_x, black, 1, cv2.LINE_AA)
cv2.putText(image, 'B', (int((285 + offset_x) * scale_x), int(317 * scale_y)), cv2.FONT_HERSHEY_SIMPLEX, 0.3 * scale_x, black, 1, cv2.LINE_AA)

# Dibujar botones Select y Start
cv2.rectangle(image, (int(160 * scale_x), int(360 * scale_y)), (int(185 * scale_x), int(368 * scale_y)), light_blue, -1)  # Select
cv2.rectangle(image, (int(195 * scale_x), int(360 * scale_y)), (int(220 * scale_x), int(368 * scale_y)), light_blue, -1)  # Start

# Dibujar texto SELECT y START
cv2.putText(image, 'SELECT', (int(162 * scale_x), int(366 * scale_y)), cv2.FONT_HERSHEY_SIMPLEX, 0.2 * scale_x, dark_text, 1, cv2.LINE_AA)
cv2.putText(image, 'START', (int(197 * scale_x), int(366 * scale_y)), cv2.FONT_HERSHEY_SIMPLEX, 0.2 * scale_x, dark_text, 1, cv2.LINE_AA)

# Dibujar LEDs indicadores
cv2.circle(image, (int(70 * scale_x), int(350 * scale_y)), int(2 * scale_x), light_blue, -1)
cv2.circle(image, (int(70 * scale_x), int(360 * scale_y)), int(2 * scale_x), light_blue, -1)

# Dibujar botón de apagado
power_button = (int(290 * scale_x), int(360 * scale_y), int(305 * scale_x), int(375 * scale_y))
cv2.rectangle(image, (power_button[0], power_button[1]), (power_button[2], power_button[3]), dark_text, -1)
cv2.putText(image, 'o', (int(295 * scale_x), int(370 * scale_y)), cv2.FONT_HERSHEY_SIMPLEX, 0.4 * scale_x, white, 1, cv2.LINE_AA)

# Variable para controlar el cierre del programa
running = True

# Función para cerrar el programa al hacer clic en el botón de apagado
def close_program(event, x, y, flags, param):
    global running
    if event == cv2.EVENT_LBUTTONDOWN:
        if power_button[0] <= x <= power_button[2] and power_button[1] <= y <= power_button[3]:
            running = False  # Cambiar el estado para cerrar el bucle principal

# Mostrar la imagen
cv2.imshow('Nintendo 3DS', image)
cv2.setMouseCallback('Nintendo 3DS', close_program)

# Esperar hasta que se cierre la ventana
while running:
    key = cv2.waitKey(1)
    if key == 27:  # Esc para salir
        break

cv2.destroyAllWindows()
