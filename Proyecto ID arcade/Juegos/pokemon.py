import cv2
import numpy as np
from enum import Enum
import random
import math
import time
from PIL import Image, ImageDraw, ImageFont


player_pos = (150, 150)
enemy_pos = (650, 150)


def remove_green_background(image):
    """
    Remove the green background from the image
    BGR color to remove: (34, 139, 34)
    """
    # Convert to float32 for better precision
    image = image.astype(np.float32)
    
    # Create a mask for the green background
    # Allow for some variation in the green color
    green_mask = (
        (image[:, :, 0] >= 29) & (image[:, :, 0] <= 39) &  # Blue channel
        (image[:, :, 1] >= 134) & (image[:, :, 1] <= 144) &  # Green channel
        (image[:, :, 2] >= 29) & (image[:, :, 2] <= 39)  # Red channel
    )
    
    # Create an alpha channel (255 for non-background, 0 for background)
    alpha = np.where(green_mask, 0, 255).astype(np.uint8)
    
    # Convert back to uint8
    image = image.astype(np.uint8)
    
    # Return the image with transparency
    return image, alpha

class BattleState(Enum):
    SELECTING_ACTION = 1
    EXECUTING_ACTION = 2
    BATTLE_ENDED = 3
    ANIMATING = 4  # Nuevo estado para las animaciones

class AnimationType(Enum):
    NONE = 0
    FIRE = 1
    ELECTRIC = 2
    HEAL = 3
    PHYSICAL = 4
    WATER = 5    # Nuevo
    GRASS = 6    # Nuevo
    PSYCHIC = 7  # Nuevo
    ICE = 8      # Nuevo
    DARK = 9     # Nuevo
    STEEL = 10
    FAIRY = 11 
    DRAGON = 12
    POISON = 13
    GROUND = 14




class Animation:
    def __init__(self, anim_type, start_pos, end_pos, duration=1.5):
        self.type = anim_type
        self.start_pos = start_pos
        self.end_pos = end_pos
        self.duration = duration
        self.start_time = time.time()
        self.particles = []
        self.trails = []  # Para efectos de estela
        self.secondary_particles = []  # Para efectos secundarios
        self.initialize_particles()

    def initialize_particles(self):
        particle_configs = {
            AnimationType.FIRE: {'count': 40, 'size_range': (4, 12)},
            AnimationType.ELECTRIC: {'count': 35, 'size_range': (3, 8)},
            AnimationType.WATER: {'count': 30, 'size_range': (4, 10)},
            AnimationType.GRASS: {'count': 25, 'size_range': (5, 12)},
            AnimationType.PSYCHIC: {'count': 45, 'size_range': (3, 8)},
            AnimationType.ICE: {'count': 20, 'size_range': (6, 14)},
            AnimationType.DARK: {'count': 50, 'size_range': (4, 10)}
        }

        config = particle_configs.get(self.type, {'count': 30, 'size_range': (3, 8)})
        
        for _ in range(config['count']):
            particle = {
                'pos': list(self.start_pos),
                'velocity': self._calculate_velocity_towards_target(),
                'size': random.randint(*config['size_range']),
                'lifetime': random.uniform(0.7, 1.2),
                'angle': random.uniform(0, 2 * math.pi),
                'alpha': 255,
                'color_offset': random.uniform(0, 1),
                'oscillation_offset': random.uniform(0, 2 * math.pi),
                'trail': []  # Para efectos de estela
            }
            
            if self.type == AnimationType.WATER:
                particle['wave_offset'] = random.uniform(0, 2 * math.pi)
                particle['wave_frequency'] = random.uniform(8, 12)
            
            self.particles.append(particle)

    def _calculate_velocity_towards_target(self):
        direction = [
            self.end_pos[0] - self.start_pos[0],
            self.end_pos[1] - self.start_pos[1]
        ]
        
        length = math.sqrt(direction[0]**2 + direction[1]**2)
        if length > 0:
            base_speed = random.uniform(12.0, 15.0)  # Velocidad mas variable
            spread = 3.0  # Mayor dispersion
            return [
                (direction[0] / length) * base_speed + random.uniform(-spread, spread),
                (direction[1] / length) * base_speed + random.uniform(-spread, spread)
            ]
        return [random.uniform(-6, 6), random.uniform(-6, 6)]            

    def is_finished(self):
        return time.time() - self.start_time > self.duration

    def update_and_draw(self, frame):
        progress = (time.time() - self.start_time) / self.duration
        if progress > 1:
            return

        if self.type == AnimationType.FIRE:
            self._draw_fire_animation(frame, progress)
        elif self.type == AnimationType.ELECTRIC:
            self._draw_electric_animation(frame, progress)
        elif self.type == AnimationType.HEAL:
            self._draw_heal_animation(frame, progress)
        elif self.type == AnimationType.PHYSICAL:
            self._draw_physical_animation(frame, progress)
        elif self.type == AnimationType.WATER:
            self._draw_water_animation(frame, progress)
        elif self.type == AnimationType.GRASS:
            self._draw_grass_animation(frame, progress)
        elif self.type == AnimationType.PSYCHIC:
            self._draw_psychic_animation(frame, progress)
        elif self.type == AnimationType.ICE:
            self._draw_ice_animation(frame, progress)
        elif self.type == AnimationType.DARK:
            self._draw_dark_animation(frame, progress)
        elif self.type == AnimationType.STEEL:
            self._draw_steel_animation(frame, progress)
        elif self.type == AnimationType.FAIRY:
            self._draw_fairy_animation(frame, progress)
        elif self.type == AnimationType.DRAGON:
            self._draw_dragon_animation(frame, progress)
        elif self.type == AnimationType.POISON:
            self._draw_poison_animation(frame, progress)
        elif self.type == AnimationType.GROUND:
            self._draw_ground_animation(frame, progress)

    def _draw_fire_animation(self, frame, progress):
        fire_colors = [
            (0, 0, 255),    # Rojo
            (0, 128, 255),  # Naranja
            (0, 215, 255),  # Amarillo
            (255, 255, 255)  # Blanco (centro)
        ]

        # Direccion calculada desde self.start_pos hacia self.end_pos
        direction = np.array(self.end_pos) - np.array(self.start_pos)
        direction = direction / np.linalg.norm(direction)  # Normalizar direccion

        # Parametros de velocidad y dispersion
        speed = 8 * (1 - progress)  # Mantener velocidad
        cone_angle = 0.3  # angulo del cono en radianes (ajustable segun el efecto deseado)

        # Generar nuevas particulas en cada cuadro
        num_new_particles = 10
        for _ in range(num_new_particles):
            # Generar una variacion aleatoria en el angulo dentro del cono
            angle_variation = random.uniform(-cone_angle, cone_angle)
            cos_angle = math.cos(angle_variation)
            sin_angle = math.sin(angle_variation)

            # Rotar la direccion base por el angulo de variacion
            rotated_direction = np.array([
                direction[0] * cos_angle - direction[1] * sin_angle,
                direction[0] * sin_angle + direction[1] * cos_angle
            ])

            # Crear la nueva particula con direccion en el cono
            new_particle = {
                'pos': list(self.start_pos),
                'velocity': [
                    rotated_direction[0] * speed + random.uniform(-2, 2),  # Ajuste minimo de dispersion
                    rotated_direction[1] * speed + random.uniform(-2, 2)
                ],
                'size': random.randint(5, 10)
            }
            self.particles.append(new_particle)

        # Mover y renderizar particulas
        active_particles = []
        for particle in self.particles:
            particle['pos'][0] += particle['velocity'][0]
            particle['pos'][1] += particle['velocity'][1]

            # Tamaño dinamico y efecto de parpadeo
            flicker = random.uniform(0.8, 1.2)
            size = int(particle['size'] * (1 - progress * 0.5) * flicker)

            if size > 0:
                pos = (int(particle['pos'][0]), int(particle['pos'][1]))

                # Crear efecto de gradiente de fuego
                for i, color in enumerate(fire_colors):
                    current_size = size - i * 2
                    if current_size > 0:
                        cv2.circle(frame, pos, current_size, color, -1)

                # Añadir chispas dispersas
                if random.random() < 0.2:
                    spark_pos = (
                        pos[0] + int(random.uniform(-size, size)),
                        pos[1] + int(random.uniform(-size, size))
                    )
                    cv2.circle(frame, spark_pos, 2, (255, 215, 0), -1)

                # Mantener particulas activas
                active_particles.append(particle)

        # Actualizar las particulas activas
        self.particles = active_particles

        # Añadir lineas de calor para el efecto de "llamas largas"
        for i in range(5):
            line_length = random.randint(10, 30)
            start_pos_line = (
                int(self.start_pos[0] + random.uniform(-10, 10)),
                int(self.start_pos[1] + random.uniform(-10, 10))
            )
            end_pos_line = (
                int(start_pos_line[0] + line_length * direction[0] + random.uniform(-2, 2)),
                int(start_pos_line[1] + line_length * direction[1] + random.uniform(-2, 2))
            )
            cv2.line(frame, start_pos_line, end_pos_line, (255, 140, 0), 1)




    def _draw_electric_animation(self, frame, progress):
        electric_colors = [
            (255, 255, 0),   # Amarillo brillante
            (200, 255, 255),  # Cyan claro
            (255, 255, 255)   # Blanco
        ]

        # Direccion calculada segun self.start_pos y self.end_pos
        direction = np.array(self.end_pos) - np.array(self.start_pos)
        direction = direction / np.linalg.norm(direction)
        speed = 10 * (1 - progress)  # Velocidad reducida
        spread = 10  # Dispersion mas controlada

        for particle in self.particles:
            particle['velocity'][0] = direction[0] * speed + random.uniform(-spread, spread)
            particle['velocity'][1] = direction[1] * speed + random.uniform(-spread, spread)
            particle['pos'][0] += particle['velocity'][0]
            particle['pos'][1] += particle['velocity'][1]

            start_pos = (int(particle['pos'][0]), int(particle['pos'][1]))
            points = [start_pos]
            num_segments = 4  # Menor numero de segmentos para mantener el rayo compacto

            for _ in range(num_segments):
                last_point = points[-1]
                next_point = (
                    last_point[0] + int(random.uniform(-10, 10)),  # Menor variacion para control
                    last_point[1] + int(random.uniform(-10, 10))
                )
                points.append(next_point)

            for i in range(len(points) - 1):
                for color in electric_colors:
                    thickness = 3 - electric_colors.index(color)
                    cv2.line(frame, points[i], points[i + 1], color, thickness)

            # Añadir chispas alrededor de las particulas
            if random.random() < 0.3:
                spark_pos = (
                    start_pos[0] + int(random.uniform(-5, 5)),
                    start_pos[1] + int(random.uniform(-5, 5))
                )
                cv2.circle(frame, spark_pos, 2, (255, 255, 255), -1)



    def _draw_physical_animation(self, frame, progress):
        # Posiciones inicial y final
        start = np.array(self.start_pos)
        end = np.array(self.end_pos)
        current = start + (end - start) * progress
        
        # Dibujar la linea de movimiento con un rastro mas ancho que se desvanece
        trail_thickness = max(1, int(20 * (1 - progress)))  # Asegurarse de que thickness sea al menos 1
        cv2.line(frame, 
                tuple(map(int, start)), 
                tuple(map(int, current)), 
                (200, 50, 50), trail_thickness)
        
        # Añadir "ondas de choque" en el punto final del golpe
        impact_radius = max(1, int(30 * (1 - progress)))  # Asegurarse de que el radio sea al menos 1
        if impact_radius > 0:
            for i in range(3):
                cv2.circle(
                    frame, 
                    tuple(map(int, current)), 
                    impact_radius + i * 5, 
                    (255, 255, 255), 
                    1
                )

        # Añadir "destellos" en el punto de impacto para simular un golpe fuerte
        if random.random() < 0.5:  # Aleatorio para dar un efecto de parpadeo
            for _ in range(3):  # Varios destellos en distintas direcciones
                angle = random.uniform(0, 2 * np.pi)
                length = random.randint(10, 30)
                end_pos = (
                    int(current[0] + length * np.cos(angle)),
                    int(current[1] + length * np.sin(angle))
                )
                cv2.line(frame, 
                        tuple(map(int, current)), 
                        end_pos, 
                        (255, 255, 255), 
                        2)

        # Efecto de "aura" alrededor del impacto para simular la fuerza
        aura_radius = max(1, int(50 * (1 - progress)))  # Asegurarse de que el radio sea al menos 1
        aura_color = (255, int(255 * (1 - progress)), 0)
        cv2.circle(frame, 
                tuple(map(int, current)), 
                aura_radius, 
                aura_color, 
                2)

    def _draw_heal_animation(self, frame, progress):
        center = (int(self.end_pos[0]), int(self.end_pos[1]))
        
        # Colores de curacion mejorados
        heal_colors = [
            (0, 255, 0),    # Verde brillante
            (150, 255, 150), # Verde claro
            (255, 255, 255)  # Blanco
        ]
        
        # Asegurarse de que progress este entre 0 y 1
        progress = max(0, min(1, progress))
        
        # Efecto de aureola expansiva
        for i in range(3):
            radius = max(1, int(80 * progress * (1 + i * 0.3)))  # Asegurar radio minimo de 1
            alpha = int(255 * (1 - progress))
            color = heal_colors[i]
            cv2.circle(frame, center, radius, color, 2)
        
        # Particulas curativas giratorias
        num_particles = 12
        for i in range(num_particles):
            angle = (2 * math.pi * i / num_particles) + (progress * 6 * math.pi)
            for radius_mult in [0.5, 0.75, 1.0]:
                radius = max(1, 40 * progress * radius_mult)  # Asegurar radio minimo de 1
                x = int(center[0] + radius * math.cos(angle))
                y = int(center[1] + radius * math.sin(angle))
                
                # Efecto de brillo
                size = max(1, int(5 * (1 - progress)))  # Asegurar tamaño minimo de 1
                for color in heal_colors:
                    cv2.circle(frame, (x, y), size, color, -1)
                    size = max(1, size - 1)  # Asegurar que size nunca sea menor que 1
        
        # Runas curativas
        rune_size = max(1, int(30 * (1 - progress * 0.5)))  # Asegurar tamaño minimo de 1
        for i in range(4):
            angle = (2 * math.pi * i / 4) + (progress * 2 * math.pi)
            x = int(center[0] + rune_size * 2 * math.cos(angle))
            y = int(center[1] + rune_size * 2 * math.sin(angle))
            
            # Dibujar simbolo runico
            points = np.array([
                [x - rune_size, y],
                [x, y - rune_size],
                [x + rune_size, y],
                [x, y + rune_size]
            ], np.int32)
            
            cv2.polylines(frame, [points], True, (0, 255, 0), 2)


    def _draw_steel_animation(self, frame, progress):
        # Posiciones inicial y final
        start = np.array(self.start_pos)
        end = np.array(self.end_pos)
        current = start + (end - start) * progress
        
        # Efectos metálicos reflectantes (destellos plateados)
        metallic_colors = [
            (192, 192, 192),  # Plateado claro
            (169, 169, 169),  # Plateado medio
            (211, 211, 211),  # Plateado brillante
            (220, 220, 220)   # Casi blanco
        ]
        
        # Crear múltiples "hojas" de acero
        for i in range(3):
            offset = 20 * np.array([
                np.cos(2 * np.pi * i / 3 + progress * 4),
                np.sin(2 * np.pi * i / 3 + progress * 4)
            ])
            blade_pos = current + offset
            
            # Dibujar las hojas de acero con efecto de rotación
            blade_length = 40
            angle = progress * 720  # Rotación de 720 grados
            end_blade = (
                int(blade_pos[0] + blade_length * np.cos(np.radians(angle))),
                int(blade_pos[1] + blade_length * np.sin(np.radians(angle)))
            )
            
            # Efecto de brillo metálico
            color_idx = int(progress * len(metallic_colors))
            color = metallic_colors[min(color_idx, len(metallic_colors) - 1)]
            
            cv2.line(frame,
                    tuple(map(int, blade_pos)),
                    end_blade,
                    color,
                    3)
        
        # Ondas de energía metálica
        wave_radius = int(50 * progress)
        for r in range(3):
            radius = wave_radius + r * 15
            opacity = int(255 * (1 - progress))
            cv2.circle(frame,
                    tuple(map(int, current)),
                    radius,
                    (169, 169, 169, opacity),
                    2)
        
        # Destellos metálicos aleatorios
        if random.random() < 0.7:
            for _ in range(5):
                spark_pos = (
                    int(current[0] + random.uniform(-30, 30)),
                    int(current[1] + random.uniform(-30, 30))
                )
                size = random.randint(2, 5)
                cv2.circle(frame,
                        spark_pos,
                        size,
                        (255, 255, 255),
                        -1)
        
        # Efecto de impacto metálico al final
        # Efecto de impacto metálico al final
        if progress > 0.8:
            impact_progress = (progress - 0.8) / 0.2
            impact_size = max(20, int(60 * impact_progress))  # Asegura que impact_size sea al menos 20

            # Crear patrón de grietas metálicas
            for _ in range(8):
                angle = random.uniform(0, 2 * np.pi)
                length = random.randint(20, impact_size)
                end_crack = (
                    int(current[0] + length * np.cos(angle)),
                    int(current[1] + length * np.sin(angle))
                )
                cv2.line(frame,
                        tuple(map(int, current)),
                        end_crack,
                        (192, 192, 192),
                        2)

        
        # Añadir partículas metálicas
        particle_count = 20
        for _ in range(particle_count):
            angle = random.uniform(0, 2 * np.pi)
            distance = random.uniform(0, 40 * (1 - progress))
            particle_pos = (
                int(current[0] + distance * np.cos(angle)),
                int(current[1] + distance * np.sin(angle))
            )
            size = random.randint(2, 4)
            cv2.circle(frame,
                    particle_pos,
                    size,
                    random.choice(metallic_colors),
                    -1)

    def _draw_fairy_animation(self, frame, progress):
        # Colores suaves y mágicos en BGR
        fairy_colors = [
            (255, 255, 255),  # Blanco puro para el brillo central
            (203, 192, 255),  # Rosa suave
            (147, 112, 219),  # Rosa más profundo
            (238, 130, 238)   # Violeta claro
        ]
        
        t = time.time() * 1.5  # Tiempo para animaciones
        
        # Centro del efecto
        center = np.array(self.start_pos)
        target = np.array(self.end_pos)
        direction = target - center
        current_center = center + direction * progress
        
        # Dibujar círculos concéntricos con efecto de rotación
        for i in range(6):
            radius = 40 * (1 + np.sin(t + i * 0.5) * 0.3)
            rotation = t * 0.5 + i * np.pi / 3
            for j in range(6):
                angle = rotation + j * np.pi / 3
                pos = current_center + np.array([
                    np.cos(angle) * radius,
                    np.sin(angle) * radius
                ])
                
                # Dibujar pétalos de flor
                for color_idx, color in enumerate(fairy_colors):
                    petal_size = int(15 * (1 - color_idx * 0.2))
                    cv2.circle(frame, 
                            tuple(map(int, pos)), 
                            petal_size, 
                            color, 
                            -1)
        
        # Dibujar espirales de polvo de hadas
        num_spirals = 12
        for i in range(num_spirals):
            spiral_progress = (progress + i/num_spirals) % 1
            angle = t * 2 + i * (2 * np.pi / num_spirals)
            
            for j in range(10):
                spiral_t = j / 10
                spiral_radius = 30 * (1 - spiral_t)
                
                pos = center + direction * spiral_progress
                pos += np.array([
                    np.cos(angle + spiral_t * 4) * spiral_radius,
                    np.sin(angle + spiral_t * 4) * spiral_radius
                ])
                
                size = int(4 * (1 - spiral_t))
                if size > 0:
                    cv2.circle(frame, 
                            tuple(map(int, pos)), 
                            size, 
                            fairy_colors[0], 
                            -1)
        
        # Efecto de brillo mágico en el centro
        glow_radius = int(40 * (1 + np.sin(t * 2) * 0.3))
        for i in range(3):
            cv2.circle(frame,
                    tuple(map(int, current_center)),
                    glow_radius - i * 10,
                    fairy_colors[i],
                    2)
        
        # Añadir estrellas brillantes alrededor
        for i in range(8):
            star_angle = t + i * np.pi / 4
            star_dist = 50 * (1 + np.sin(t * 2 + i) * 0.3)
            star_pos = current_center + np.array([
                np.cos(star_angle) * star_dist,
                np.sin(star_angle) * star_dist
            ])
            
            # Dibujar estrella de 5 puntas
            for j in range(5):
                angle = j * (2 * np.pi / 5) + t
                point1 = star_pos + np.array([
                    np.cos(angle) * 10,
                    np.sin(angle) * 10
                ])
                point2 = star_pos + np.array([
                    np.cos(angle + np.pi/5) * 4,
                    np.sin(angle + np.pi/5) * 4
                ])
                cv2.line(frame,
                        tuple(map(int, point1)),
                        tuple(map(int, point2)),
                        fairy_colors[0],
                        2)
        
        # Añadir destellos aleatorios
        for _ in range(20):
            if random.random() < 0.3:
                sparkle_pos = current_center + np.array([
                    random.uniform(-60, 60),
                    random.uniform(-60, 60)
                ])
                sparkle_size = random.randint(1, 3)
                cv2.circle(frame,
                        tuple(map(int, sparkle_pos)),
                        sparkle_size,
                        fairy_colors[0],
                        -1)

    def _draw_poison_animation(self, frame, progress):
        """
        Dibuja una animación de veneno localizada alrededor del Pokémon objetivo.
        Usa self.start_pos y self.end_pos para determinar la dirección
        """
        height, width = frame.shape[:2]
        
        # Colores temáticos de veneno
        poison_colors = [
            (147, 39, 143),   # Púrpura profundo
            (191, 62, 255),   # Violeta brillante
            (126, 87, 194),   # Púrpura medio
            (163, 0, 186),    # Violeta intenso
            (108, 0, 147)     # Púrpura oscuro
        ]
        
        # Calcular la posición actual del efecto
        current_pos = np.array([
            self.start_pos[0] + (self.end_pos[0] - self.start_pos[0]) * progress,
            self.start_pos[1] + (self.end_pos[1] - self.start_pos[1]) * progress
        ], dtype=np.int32)
        
        # Crear capa para el efecto
        overlay = np.zeros_like(frame, dtype=np.uint8)
        
        # Radio de efecto alrededor del Pokémon
        effect_radius = 60
        
        # Burbujas de veneno ascendentes
        num_bubbles = 15
        for i in range(num_bubbles):
            # Posición base de cada burbuja
            angle = (i / num_bubbles) * 2 * np.pi
            base_offset_x = math.cos(angle) * effect_radius * 0.5
            base_offset_y = math.sin(angle) * effect_radius * 0.5
            
            # Movimiento ascendente con wobble
            bubble_progress = (progress + i/num_bubbles) % 1.0
            wobble = math.sin(bubble_progress * 6 * np.pi) * 10
            
            # Calcular posición final de la burbuja
            x = int(current_pos[0] + base_offset_x + wobble)
            y = int(current_pos[1] + base_offset_y - bubble_progress * effect_radius)
            
            # Tamaño variable de las burbujas
            size = int(8 * (1 - bubble_progress))
            
            if size > 0 and 0 <= x < width and 0 <= y < height:
                # Dibujar burbuja principal
                color = poison_colors[i % len(poison_colors)]
                cv2.circle(overlay, (x, y), size, color, -1)
                
                # Añadir brillo a la burbuja
                highlight_pos = (x - size//3, y - size//3)
                if 0 <= highlight_pos[0] < width and 0 <= highlight_pos[1] < height:
                    cv2.circle(overlay, highlight_pos, size//3, (255, 255, 255), -1)
        
        # Efecto de charco de veneno en la base
        puddle_vertices = []
        num_vertices = 12
        for i in range(num_vertices):
            angle = 2 * np.pi * i / num_vertices
            # Radio variable para dar efecto de pulsación
            puddle_radius = effect_radius * (0.8 + 0.2 * math.sin(progress * 4 * np.pi))
            x = int(current_pos[0] + math.cos(angle) * puddle_radius)
            y = int(current_pos[1] + math.sin(angle) * puddle_radius * 0.4)
            puddle_vertices.append([x, y])
        
        puddle_vertices = np.array([puddle_vertices], dtype=np.int32)
        
        # Dibujar charco con gradiente
        for i in range(3):
            size_mult = 1 - (i * 0.2)
            center_point = np.array([[[current_pos[0], current_pos[1]]]])
            scaled_points = (puddle_vertices * size_mult + 
                            (1 - size_mult) * center_point).astype(np.int32)
            cv2.fillPoly(overlay, scaled_points, poison_colors[i])
        
        # Niebla tóxica localizada
        for i in range(20):
            angle = 2 * np.pi * (i / 20 + progress)
            radius = effect_radius * (0.5 + 0.5 * math.sin(progress * np.pi + i))
            x = int(current_pos[0] + math.cos(angle) * radius)
            y = int(current_pos[1] + math.sin(angle) * radius)
            
            if 0 <= x < width and 0 <= y < height:
                mist_size = int(15 * (1 - (radius / effect_radius)))
                cv2.circle(overlay, (x, y), mist_size, 
                        poison_colors[i % len(poison_colors)], -1)
        
        # Suavizar efectos
        overlay = cv2.GaussianBlur(overlay, (7, 7), 0)
        
        # Combinar con el frame original
        alpha = 0.7
        frame[:] = cv2.addWeighted(frame, 1 - alpha, overlay, alpha, 0)
        
        # Efecto de distorsión sutil solo en el área afectada
        if 0.2 < progress < 0.8:
            mask = np.zeros((height, width), dtype=np.uint8)
            cv2.circle(mask, (int(current_pos[0]), int(current_pos[1])), effect_radius, 255, -1)
            
            distorted = frame.copy()
            for y in range(max(0, int(current_pos[1]) - effect_radius), 
                        min(height, int(current_pos[1]) + effect_radius)):
                for x in range(max(0, int(current_pos[0]) - effect_radius), 
                            min(width, int(current_pos[0]) + effect_radius)):
                    if mask[y, x]:
                        dx = 3 * math.sin(y/10 + progress * 10)
                        dy = 3 * math.cos(x/10 + progress * 10)
                        
                        src_x = x + dx
                        src_y = y + dy
                        
                        if (0 <= src_x < width - 1 and 0 <= src_y < height - 1):
                            distorted[y, x] = frame[int(src_y), int(src_x)]
            
            frame[:] = distorted

        




    def _draw_dragon_animation(self, frame, progress):
        # Colores en BGR para que sean correctos en OpenCV
        beam_colors = [
            (255, 255, 255),  # Blanco para el centro
            (130, 0, 75),     # Morado oscuro
            (130, 20, 0),     # Azul muy oscuro
            (255, 100, 0)     # Naranja oscuro para detalles
        ]
        
        # Calcular dirección principal
        direction = np.array(self.end_pos) - np.array(self.start_pos)
        total_distance = np.linalg.norm(direction)
        direction = direction / total_distance  # Normalizar dirección
        
        # Variables para efectos
        t = time.time() * 5
        beam_width = 50 * (1 + np.sin(t) * 0.2)  # Rayo más ancho
        
        # Calcular punto actual del rayo basado en el progreso
        current_distance = total_distance * progress
        beam_end = np.array(self.start_pos) + direction * current_distance
        
        # Dibujar el rayo principal (efecto base)
        cv2.line(frame,
                tuple(map(int, self.start_pos)),
                tuple(map(int, beam_end)),
                beam_colors[0],
                15)  # Línea central más gruesa
        
        # Efecto de espiral alrededor del rayo principal
        num_spirals = 30
        for i in range(num_spirals):
            phase = t + i * (2 * np.pi / num_spirals)
            for d in np.linspace(0, current_distance, 50):
                point = np.array(self.start_pos) + direction * d
                spiral_radius = beam_width * (1 - d/total_distance * 0.5)
                offset_x = np.cos(phase + d * 0.1) * spiral_radius
                offset_y = np.sin(phase + d * 0.1) * spiral_radius
                point = point + np.array([offset_x, offset_y])
                
                if i % 3 == 0:  # Cada tercera espiral es más brillante
                    color = beam_colors[0]
                    size = 3
                else:
                    color = beam_colors[1]
                    size = 2
                    
                cv2.circle(frame, tuple(map(int, point)), size, color, -1)
        
        # Efecto de carga al inicio
        if progress < 0.3:
            charge_radius = int(80 * (progress / 0.3))
            for i in range(8):  # Más orbes de energía
                angle = t * 3 + i * (2 * np.pi / 8)
                orb_x = int(self.start_pos[0] + np.cos(angle) * charge_radius)
                orb_y = int(self.start_pos[1] + np.sin(angle) * charge_radius)
                cv2.circle(frame, (orb_x, orb_y), 15, beam_colors[1], -1)
                cv2.circle(frame, (orb_x, orb_y), 18, beam_colors[0], 2)
        
        # Efecto de impacto
        if progress > 0.7:  # Empezar el efecto antes
            impact_center = tuple(map(int, self.end_pos))
            explosion_size = int(150 * (progress - 0.7) / 0.3)  # Explosión más grande
            
            # Ondas de choque más intensas
            for i in range(4):
                cv2.circle(frame, impact_center, explosion_size + i * 25, beam_colors[i % len(beam_colors)], 4)
            
            # Destellos radiales más grandes
            for i in range(12):  # Más rayos
                angle = t + i * (2 * np.pi / 12)
                end_x = int(impact_center[0] + np.cos(angle) * explosion_size * 2)
                end_y = int(impact_center[1] + np.sin(angle) * explosion_size * 2)
                cv2.line(frame, impact_center, (end_x, end_y), beam_colors[0], 3)
        
        # Partículas de energía adicionales
        num_particles = 40  # Más partículas
        for i in range(num_particles):
            particle_progress = (progress + i/num_particles) % 1
            offset_angle = t * 2 + i * (2 * np.pi / num_particles)
            
            # Distribuir partículas a lo largo del rayo
            base_pos = np.array(self.start_pos) + direction * (current_distance * particle_progress)
            offset_dist = beam_width * 0.7 * (1 - particle_progress * 0.5)
            particle_pos = base_pos + np.array([
                np.cos(offset_angle) * offset_dist,
                np.sin(offset_angle) * offset_dist
            ])
            
            size = max(2, int(10 * (1 - particle_progress)))
            cv2.circle(frame, 
                    tuple(map(int, particle_pos)), 
                    size, 
                    beam_colors[0], 
                    -1)



    def _draw_ground_animation(self, frame, progress):
        # Paleta de colores marrones (BGR)
        ground_colors = [
            (87, 139, 189),     # Marrón base
            (47, 79, 139),      # Marrón oscuro
            (71, 99, 169),      # Marrón medio
            (108, 156, 206),    # Marrón claro
            (156, 183, 224),    # Marrón muy claro
        ]
        
        # Calcular dirección principal
        direction = np.array(self.end_pos) - np.array(self.start_pos)
        total_distance = np.linalg.norm(direction)
        
        # Generar puntos de la grieta principal con zigzag
        main_points = []
        num_segments = 20
        last_deviation = 0
        
        for i in range(num_segments + 1):
            t = i / num_segments
            if t > progress:
                break
                
            # Crear zigzag natural para la grieta principal
            max_deviation = 25 * (1 - t)  # Menos desviación cerca del objetivo
            deviation = last_deviation + random.uniform(-10, 10)
            deviation = max(min(deviation, max_deviation), -max_deviation)
            last_deviation = deviation
            
            # Vector perpendicular para el zigzag
            perp = np.array([-direction[1], direction[0]]) / total_distance
            point = (np.array(self.start_pos) + direction * t + perp * deviation).astype(int)
            main_points.append(point)
        
        # Dibujar la grieta principal
        if len(main_points) > 1:
            # Grieta principal más gruesa
            cv2.polylines(frame, [np.array(main_points)], False, ground_colors[0], 12)
            # Borde interno para dar profundidad
            cv2.polylines(frame, [np.array(main_points)], False, ground_colors[1], 6)
            
            # Grietas secundarias más pequeñas
            for i in range(len(main_points) - 1):
                if random.random() < 0.7:  # 70% de probabilidad de grieta secundaria
                    start_point = main_points[i]
                    
                    # 2-3 grietas secundarias por punto
                    for _ in range(random.randint(2, 3)):
                        # Ángulo aleatorio pero evitando que vaya hacia atrás
                        base_angle = math.atan2(direction[1], direction[0])
                        angle = base_angle + random.uniform(-math.pi/3, math.pi/3)
                        
                        # Longitud aleatoria pero siempre más corta que la principal
                        length = random.randint(10, 25)
                        end_point = start_point + np.array([
                            math.cos(angle) * length,
                            math.sin(angle) * length
                        ]).astype(int)
                        
                        # Crear puntos para el zigzag de la grieta secundaria
                        secondary_points = []
                        num_secondary_segments = 3
                        for j in range(num_secondary_segments + 1):
                            st = j / num_secondary_segments
                            small_deviation = random.uniform(-5, 5)
                            secondary_point = (start_point + (end_point - start_point) * st +
                                            np.array([-direction[1], direction[0]]) * small_deviation / total_distance).astype(int)
                            secondary_points.append(secondary_point)
                        
                        # Dibujar grieta secundaria
                        if len(secondary_points) > 1:
                            cv2.polylines(frame, [np.array(secondary_points)], False, ground_colors[1], 3)
                            cv2.polylines(frame, [np.array(secondary_points)], False, ground_colors[2], 1)
        
        if len(main_points) > 0:
            for point in main_points[::2]:  # Tomar solo puntos alternos para reducir densidad
                # Reducido a solo una roca por punto
                if random.random() < 0.3:  # Reducida la probabilidad
                    rock_pos = point + np.array([
                        random.randint(-10, 10),  # Reducido el rango
                        random.randint(-10, 10)
                    ])
                    rock_size = random.randint(2, 3)  # Reducido el tamaño
                    cv2.circle(frame, tuple(rock_pos), rock_size, ground_colors[2], -1)
                
                # Efecto de polvo simplificado
                dust_opacity = int(100 * (1 - progress))  # Reducida la opacidad
                if dust_opacity > 0:
                    # Solo 2 partículas de polvo por punto
                    for _ in range(2):
                        dust_pos = point + np.array([
                            random.randint(-15, 15),  # Reducido el rango
                            random.randint(-15, 15)
                        ])
                        dust_size = random.randint(3, 6)  # Reducido el tamaño
                        cv2.circle(frame, tuple(dust_pos), dust_size,
                                (*ground_colors[4][:3], dust_opacity), -1)
        
        # Efecto de impacto reducido
        if len(main_points) > 0:
            current_point = main_points[-1]
            cv2.circle(frame, tuple(current_point), 6, ground_colors[1], -1)  # Reducido el tamaño
            cv2.circle(frame, tuple(current_point), 3, ground_colors[2], -1)


    def _draw_water_animation(self, frame, progress):
        # Colores del agua
        water_colors = [
            (255, 178, 102),  # Azul claro
            (255, 215, 102),  # Azul mas claro
            (255, 255, 255)   # Blanco (para brillos)
        ]
        
        # Actualizar y dibujar gotas de agua
        for particle in self.particles:
            # Movimiento ondulatorio mas complejo
            wave_x = math.sin(progress * particle['wave_frequency'] + particle['wave_offset']) * 15
            wave_y = math.cos(progress * particle['wave_frequency'] + particle['wave_offset']) * 8
            
            current_pos = [
                particle['pos'][0] + wave_x,
                particle['pos'][1] + wave_y
            ]
            
            # Actualizar posicion con efecto de arrastre
            particle['pos'][0] += particle['velocity'][0] * 0.6
            particle['pos'][1] += particle['velocity'][1] * 0.6
            
            # Dibujar gota de agua con efectos
            pos = (int(current_pos[0]), int(current_pos[1]))
            size = int(particle['size'] * (1.2 - progress * 0.5))
            
            if size > 0:
                # Gota principal con gradiente
                for i, color in enumerate(water_colors):
                    current_size = size - i * 2
                    if current_size > 0:
                        cv2.circle(frame, pos, current_size, color, -1)
                
                # Efecto de brillo
                highlight_pos = (pos[0] - 1, pos[1] - 1)
                highlight_size = max(1, size // 3)
                cv2.circle(frame, highlight_pos, highlight_size, (255, 255, 255), -1)
                
                # Añadir rastro de agua
                if random.random() < 0.3:
                    splash_pos = (
                        pos[0] + int(random.uniform(-size, size)),
                        pos[1] + int(random.uniform(-size, size))
                    )
                    cv2.circle(frame, splash_pos, 1, water_colors[0], -1)

    def _draw_grass_animation(self, frame, progress):
        leaf_colors = [
            (0, 255, 0),     # Verde brillante
            (50, 255, 50),   # Verde claro
            (150, 255, 150)  # Verde muy claro
        ]
        
        for particle in self.particles:
            # Movimiento mas organico
            particle['pos'][0] += particle['velocity'][0] * 0.6
            particle['pos'][1] += particle['velocity'][1] * 0.6
            
            # Rotacion con oscilacion
            base_angle = particle['angle'] + progress * 8
            wave = math.sin(progress * 10 + particle['oscillation_offset']) * 0.5
            angle = base_angle + wave
            
            pos = (int(particle['pos'][0]), int(particle['pos'][1]))
            size = int(particle['size'] * (1.2 - progress * 0.4))
            
            if size > 0:
                # Dibujar hojas con efectos
                for i, color in enumerate(leaf_colors):
                    current_size = size - i * 2
                    if current_size > 0:
                        points = self._get_rotated_leaf_points(pos, angle, current_size)
                        cv2.fillPoly(frame, [points], color)
                
                # Añadir efectos de brillo
                if random.random() < 0.2:
                    spark_pos = (
                        pos[0] + int(random.uniform(-size, size)),
                        pos[1] + int(random.uniform(-size, size))
                    )
                    cv2.circle(frame, spark_pos, 1, (200, 255, 200), -1)
                
                # Efecto de rastro de energia
                trail_points = self._get_rotated_leaf_points(pos, angle - 0.5, size // 2)
                cv2.polylines(frame, [trail_points], True, (100, 255, 100), 1)


    def _get_rotated_leaf_points(self, pos, angle, size):
        # Crear puntos base para una hoja mas detallada
        points = np.array([
            [pos[0], pos[1] - size * 1.5],  # Punta
            [pos[0] - size, pos[1] - size],  # Izquierda superior
            [pos[0] - size * 1.2, pos[1]],   # Izquierda medio
            [pos[0] - size, pos[1] + size],  # Izquierda inferior
            [pos[0], pos[1] + size * 1.2],   # Base
            [pos[0] + size, pos[1] + size],  # Derecha inferior
            [pos[0] + size * 1.2, pos[1]],   # Derecha medio
            [pos[0] + size, pos[1] - size]   # Derecha superior
        ], np.int32)
        
        # Rotar puntos
        center = np.array([pos[0], pos[1]])
        rotated_points = []
        for point in points:
            dx = point[0] - center[0]
            dy = point[1] - center[1]
            rotated_x = dx * math.cos(angle) - dy * math.sin(angle) + center[0]
            rotated_y = dx * math.sin(angle) + dy * math.cos(angle) + center[1]
            rotated_points.append([int(rotated_x), int(rotated_y)])
        
        return np.array(rotated_points, np.int32)

    def _draw_psychic_animation(self, frame, progress):
        # Colores psionicos mejorados
        psychic_colors = [
            (255, 0, 255),    # Magenta
            (200, 0, 200),    # Magenta oscuro
            (255, 100, 255),  # Rosa claro
            (255, 255, 255)   # Blanco
        ]
        
        # Calcular centro actual con movimiento suave
        current_center = np.array([
            self.start_pos[0] + (self.end_pos[0] - self.start_pos[0]) * progress,
            self.start_pos[1] + (self.end_pos[1] - self.start_pos[1]) * progress
        ])
        
        # Anillos psionicos con efectos
        num_rings = 4
        for i in range(num_rings):
            progress_offset = progress + i * 0.25
            radius = int(50 * (1 + math.sin(progress_offset * 2 * math.pi)))
            
            # Dibujar multiples anillos con diferentes colores
            for j, color in enumerate(psychic_colors):
                current_radius = radius - j * 3
                if current_radius > 0:
                    thickness = max(1, int(3 * (1 - progress)))
                    cv2.circle(frame, 
                            (int(current_center[0]), int(current_center[1])),
                            current_radius, color, thickness)
        
        # Particulas orbitantes con efectos de energia
        for particle in self.particles:
            base_angle = particle['angle'] + progress * 15
            radius = 30 + 20 * math.sin(progress * 4 * math.pi)
            
            # Calcular posicion de la particula
            pos = (
                int(current_center[0] + radius * math.cos(base_angle)),
                int(current_center[1] + radius * math.sin(base_angle))
            )
            
            # Dibujar estela de energia psiquica
            trail_length = 8
            for i in range(trail_length):
                trail_angle = base_angle - i * 0.2
                trail_pos = (
                    int(current_center[0] + radius * math.cos(trail_angle)),
                    int(current_center[1] + radius * math.sin(trail_angle))
                )
                size = max(1, 3 - i // 2)
                alpha = int(255 * (1 - i/trail_length) * (1 - progress))
                cv2.circle(frame, trail_pos, size, psychic_colors[min(i//2, len(psychic_colors)-1)], -1)
            
            # Dibujar particula principal
            cv2.circle(frame, pos, 3, (255, 255, 255), -1)
        
        # Efecto de ondas psiquicas expansivas
        wave_count = 3
        for i in range(wave_count):
            wave_progress = (progress + i/wave_count) % 1
            wave_radius = int(100 * wave_progress)
            alpha = int(255 * (1 - wave_progress))
            cv2.circle(frame, (int(current_center[0]), int(current_center[1])),
                    wave_radius, (255, 0, 255), 1)

    def _draw_ice_animation(self, frame, progress):
        # Colores de hielo mejorados
        ice_colors = [
            (255, 255, 255),  # Blanco
            (250, 250, 255),  # Blanco azulado
            (200, 220, 255),  # Azul muy claro
            (150, 200, 255)   # Azul hielo
        ]
        
        for particle in self.particles:
            # Movimiento con efecto de cristalizacion
            particle['pos'][0] += particle['velocity'][0] * 0.8 * (1 - progress * 0.7)
            particle['pos'][1] += particle['velocity'][1] * 0.8 * (1 - progress * 0.7)
            
            center = (int(particle['pos'][0]), int(particle['pos'][1]))
            size = int(particle['size'] * (1.2 - progress * 0.3))
            base_angle = particle['angle'] + progress * 3
            
            if size > 0:
                # Dibujar copo de nieve principal
                for i in range(6):
                    angle = base_angle + i * math.pi / 3
                    
                    # Rama principal
                    end_point = (
                        int(center[0] + size * 3 * math.cos(angle)),
                        int(center[1] + size * 3 * math.sin(angle))
                    )
                    
                    # Dibujar rama principal con gradiente
                    for j, color in enumerate(ice_colors):
                        thickness = 3 - j
                        if thickness > 0:
                            cv2.line(frame, center, end_point, color, thickness)
                    
                    # Ramificaciones secundarias
                    branch_count = 3
                    for j in range(branch_count):
                        branch_start = (
                            int(center[0] + (j + 1) * size * math.cos(angle)),
                            int(center[1] + (j + 1) * size * math.sin(angle))
                        )
                        
                        # Ramas laterales
                        for direction in [-1, 1]:
                            branch_angle = angle + direction * math.pi / 3
                            branch_length = size * (1 - j/branch_count)
                            branch_end = (
                                int(branch_start[0] + branch_length * math.cos(branch_angle)),
                                int(branch_start[1] + branch_length * math.sin(branch_angle))
                            )
                            
                            # Dibujar rama secundaria con gradiente
                            for k, color in enumerate(ice_colors):
                                thickness = 2 - k
                                if thickness > 0:
                                    cv2.line(frame, branch_start, branch_end, color, thickness)
                
                # Efecto de cristalizacion
                if random.random() < 0.3:
                    crystal_pos = (
                        center[0] + int(random.uniform(-size*2, size*2)),
                        center[1] + int(random.uniform(-size*2, size*2))
                    )
                    crystal_size = random.randint(1, 3)
                    cv2.circle(frame, crystal_pos, crystal_size, ice_colors[0], -1)

    def _draw_dark_animation(self, frame, progress):
        # Colores oscuros mejorados
        dark_colors = [
            (139, 0, 139),    # Morado oscuro
            (75, 0, 130),     # indigo
            (20, 0, 40),      # Casi negro
            (160, 32, 240)    # Purpura
        ]
        
        # Calcular centro actual
        center = np.array(self.start_pos) + (np.array(self.end_pos) - np.array(self.start_pos)) * progress
        
        # Efecto de vortice oscuro
        for particle in self.particles:
            # Movimiento en espiral mas dramatico
            spiral_progress = progress * 5
            radius = 50 * (1 - progress ** 1.5)  # Contraccion no lineal
            angle = particle['angle'] + spiral_progress * (1 + progress * 2)
            
            # Calcular posicion con distorsion
            distortion = math.sin(progress * 10 + particle['oscillation_offset']) * 5
            pos = (
                int(center[0] + (radius + distortion) * math.cos(angle)),
                int(center[1] + (radius + distortion) * math.sin(angle))
            )
            
            # Tamaño variable con el progreso
            size = int(particle['size'] * (1.2 - progress))
            
            if size > 0:
                # Dibujar particula principal con efecto de gradiente
                for i, color in enumerate(dark_colors):
                    current_size = size - i
                    if current_size > 0:
                        cv2.circle(frame, pos, current_size, color, -1)
                
                # Añadir estela oscura
                trail_length = 5
                for i in range(trail_length):
                    trail_angle = angle - i * 0.2
                    trail_pos = (
                        int(center[0] + (radius * (1 + i/trail_length)) * math.cos(trail_angle)),
                        int(center[1] + (radius * (1 + i/trail_length)) * math.sin(trail_angle))
                    )
                    trail_size = max(1, size - i)
                    alpha = int(255 * (1 - i/trail_length) * (1 - progress))
                    cv2.circle(frame, trail_pos, trail_size, dark_colors[-1], -1)
        
        # Efecto de ondas de oscuridad
        wave_count = 4
        for i in range(wave_count):
            wave_progress = (progress + i/wave_count) % 1
            wave_radius = int(80 * wave_progress)
            thickness = max(1, int(3 * (1 - wave_progress)))
            cv2.circle(frame, (int(center[0]), int(center[1])),
                    wave_radius, dark_colors[i % len(dark_colors)], thickness)
        
        # Efecto de sombras convergentes
        shadow_count = 8
        for i in range(shadow_count):
            angle = (i * 2 * math.pi / shadow_count) + progress * 4
            start_radius = 100 * (1 - progress)
            end_radius = 20 * (1 - progress)
            
            start_pos = (
                int(center[0] + start_radius * math.cos(angle)),
                int(center[1] + start_radius * math.sin(angle))
            )
            end_pos = (
                int(center[0] + end_radius * math.cos(angle)),
                int(center[1] + end_radius * math.sin(angle))
            )
            
            cv2.line(frame, start_pos, end_pos, dark_colors[0], 2)


class Pokemon:
    def __init__(self, name, image_path, hp, moves):
        self.name = name
        self.max_hp = hp
        self.current_hp = hp
        self.moves = moves
        try:
            self.image = cv2.imread(image_path)
            if self.image is not None:
                self.image = cv2.resize(self.image, (200, 200))
            else:
                self.image = np.ones((200, 200, 3), dtype=np.uint8) * 255
        except:
            self.image = np.ones((200, 200, 3), dtype=np.uint8) * 255

class PokemonBattle:
    def __init__(self):
        self.width = 800
        self.height = 400  # Reduced height for main window
        self.menu_height = 200  # Height for menu window
        self.menu_width = 500
        self.frame_count = 0  # Add this line to initialize the frame counter
        self.is_waiting = False
        self.wait_start_time = 0
        # Colores mejorados
        self.bg_color = (34, 139, 34)  # Verde oscuro para el campo
        self.text_color = (255, 255, 255)  # Blanco para mejor contraste
        self.menu_color = (0, 0, 0, 180)  # Negro semi-transparente
        
        # Diccionario de colores por tipo de ataque
        self.move_type_colors = {
            AnimationType.FIRE: (51, 51, 255),       # Rojo (BGR)
            AnimationType.ELECTRIC: (0, 255, 255),    # Amarillo (BGR)
            AnimationType.PHYSICAL: (139, 69, 19),    # Marron (BGR)
            AnimationType.HEAL: (0, 255, 0),          # Verde (BGR)
            AnimationType.WATER: (255, 178, 102),     # Azul claro (BGR)
            AnimationType.GRASS: (0, 255, 0),         # Verde (BGR)
            AnimationType.PSYCHIC: (255, 0, 255),     # Magenta (BGR)
            AnimationType.ICE: (145, 145, 145),       # Gris claro (BGR)
            AnimationType.DARK: (139, 0, 139),        # Morado oscuro (BGR)
            AnimationType.STEEL: (192, 192, 128),     # Gris metálico (BGR)
            AnimationType.DRAGON: (139, 0, 0),        # Azul oscuro (BGR)
            AnimationType.FAIRY: (147, 20, 255),      # Rosa (BGR)
            AnimationType.POISON: (204, 0, 204),      # Morado/Púrpura (BGR)
            AnimationType.GROUND: (87, 139, 189),     # Marrón tierra (BGR)
        }


        self.damage_flash_start = 0
        self.damage_flash_duration = 0.5  # duracion en segundos
        self.health_animation = None
        self.is_flashing = False
        self.flash_target = None
        
        # Elementos de diseño
        self.current_animation = None
        self.last_frame_time = time.time()
        self.is_player_turn = True
        self.animation_start_time = 0
        self.enemy_move = None
        
        self.reset_battle()
        
            
    def reset_battle(self):
        # Movimientos actualizados de Ceruledge

        moves_ceruledge = [
            {"name": "Terremoto", "damage": 28, "type": AnimationType.GROUND},  # Nuevo movimiento
            {"name": "Espada Santa", "damage": 25, "type": AnimationType.STEEL},
            {"name": "Pulso Umbrio", "damage": 22, "type": AnimationType.DARK},
            {"name": "Nitrocarga", "damage": 20, "type": AnimationType.FIRE}  # Quité Recuperación
        ]

        moves_zeraora = [
            {"name": "Ataque Arena", "damage": 20, "type": AnimationType.GROUND},  # Nuevo movimiento
            {"name": "Plasma Feroz", "damage": 24, "type": AnimationType.ELECTRIC},
            {"name": "Velocidad Extrema", "damage": 18, "type": AnimationType.PHYSICAL},
            {"name": "Hiperpocion", "damage": -25, "type": AnimationType.HEAL}  # Quité Garra Metal
        ]

        moves_gengar = [
            {"name": "Bola Sombra", "damage": 23, "type": AnimationType.DARK},
            {"name": "Bomba Lodo", "damage": 25, "type": AnimationType.POISON},  # Nuevo movimiento
            {"name": "Psiquico", "damage": 25, "type": AnimationType.PSYCHIC},
            {"name": "Maldicion", "damage": -22, "type": AnimationType.HEAL}  # Quité Carantoña
        ]

        moves_missingno = [
            {"name": "Error Fatal", "damage": 30, "type": AnimationType.PSYCHIC},
            {"name": "Corrupcion", "damage": 25, "type": AnimationType.DARK},
            {"name": "Terremoto", "damage": 28, "type": AnimationType.GROUND},  # Nuevo movimiento
            {"name": "Bug", "damage": -30, "type": AnimationType.HEAL}  # Quité Filo Metal
        ]

        moves_agumon = [
            {"name": "Llama Bebe", "damage": 18, "type": AnimationType.FIRE},
            {"name": "Golpe Veneno", "damage": 22, "type": AnimationType.POISON},  # Nuevo movimiento
            {"name": "Aliento Dragon", "damage": 22, "type": AnimationType.DRAGON},
            {"name": "Evolucion", "damage": -28, "type": AnimationType.HEAL}  # Quité Hydro Pump
        ]

        moves_shadow = [
            {"name": "Pulso Oscuro", "damage": 28, "type": AnimationType.DARK},
            {"name": "Rayo Hielo", "damage": 25, "type": AnimationType.ICE},
            {"name": "Bomba Lodo", "damage": 24, "type": AnimationType.POISON},  # Nuevo movimiento
            {"name": "Aura Oscura", "damage": -24, "type": AnimationType.HEAL}  # Quité Fuerza Lunar
        ]

        moves_gallade = [
            {"name": "Psico-corte", "damage": 24, "type": AnimationType.PSYCHIC},
            {"name": "Cabeza Metal", "damage": 20, "type": AnimationType.STEEL},
            {"name": "Terremoto", "damage": 28, "type": AnimationType.GROUND},  # Nuevo movimiento
            {"name": "Recuperacion", "damage": -25, "type": AnimationType.HEAL}  # Quité Viento Feerico
        ]

        moves_eelektross = [
            {"name": "Trueno", "damage": 25, "type": AnimationType.ELECTRIC},
            {"name": "Cola Ferrea", "damage": 20, "type": AnimationType.STEEL},
            {"name": "Ataque Arena", "damage": 18, "type": AnimationType.GROUND},  # Nuevo movimiento
            {"name": "Descanso", "damage": -25, "type": AnimationType.HEAL}  # Quité Pulso Dragon
        ]

        moves_zoroark = [
            {"name": "Pulso Umbrio", "damage": 24, "type": AnimationType.DARK},
            {"name": "Lanzamugre", "damage": 20, "type": AnimationType.POISON},  # Nuevo movimiento
            {"name": "Psiquico", "damage": 21, "type": AnimationType.PSYCHIC},
            {"name": "Ilusion", "damage": -22, "type": AnimationType.HEAL}  # Quité Dragoaliento
        ]

        moves_luxray = [
            {"name": "Colmillo Rayo", "damage": 22, "type": AnimationType.ELECTRIC},
            {"name": "Golpe Veneno", "damage": 20, "type": AnimationType.POISON},  # Nuevo movimiento
            {"name": "Brillo Magico", "damage": 24, "type": AnimationType.FAIRY},
            {"name": "Descanso", "damage": -23, "type": AnimationType.HEAL}  # Quité Fauces Metal
        ]


        moves_froslass = [
            {"name": "Ventisca", "damage": 25, "type": AnimationType.ICE},
            {"name": "Beso Drenaje", "damage": 22, "type": AnimationType.FAIRY},
            {"name": "Cola Dragon", "damage": 20, "type": AnimationType.DRAGON},
            {"name": "Nieve Curativa", "damage": -24, "type": AnimationType.HEAL}
        ]

        moves_sceptile = [
            {"name": "Tormenta Floral", "damage": 26, "type": AnimationType.GRASS},
            {"name": "Garra Metal", "damage": 24, "type": AnimationType.STEEL},
            {"name": "Meteoro Dragon", "damage": 28, "type": AnimationType.DRAGON},
            {"name": "Sintesis", "damage": -25, "type": AnimationType.HEAL}
        ]

        moves_gardevoir = [
            {"name": "Psiquico", "damage": 28, "type": AnimationType.PSYCHIC},
            {"name": "Luz Lunar", "damage": 22, "type": AnimationType.FAIRY},
            {"name": "Voz Cautivadora", "damage": 24, "type": AnimationType.FAIRY},
            {"name": "Paz Mental", "damage": -26, "type": AnimationType.HEAL}
        ]

        moves_haxorus = [
            {"name": "Garra Dragon", "damage": 27, "type": AnimationType.DRAGON},
            {"name": "Guillotina", "damage": 30, "type": AnimationType.STEEL},
            {"name": "Pulso Dragon", "damage": 25, "type": AnimationType.DRAGON},
            {"name": "Danza Dragon", "damage": -23, "type": AnimationType.HEAL}
        ]

        moves_chandelure = [
            {"name": "Fuego Fatuo", "damage": 24, "type": AnimationType.FIRE},
            {"name": "Fuerza Lunar", "damage": 23, "type": AnimationType.FAIRY},
            {"name": "Llamarada", "damage": 28, "type": AnimationType.FIRE},
            {"name": "Absorber", "damage": -22, "type": AnimationType.HEAL}
        ]

        moves_volcarona = [
            {"name": "Danza Llama", "damage": 26, "type": AnimationType.FIRE},
            {"name": "Garra Metal", "damage": 22, "type": AnimationType.STEEL},
            {"name": "Vendaval", "damage": 24, "type": AnimationType.DRAGON},
            {"name": "Escudo Polen", "damage": -25, "type": AnimationType.HEAL}
        ]

        moves_metagross = [
            {"name": "Puño Meteoro", "damage": 28, "type": AnimationType.STEEL},
            {"name": "Cabeza Hierro", "damage": 25, "type": AnimationType.STEEL},
            {"name": "Garra Dragon", "damage": 24, "type": AnimationType.DRAGON},
            {"name": "Agilidad", "damage": -24, "type": AnimationType.HEAL}
        ]

        moves_noivern = [
            {"name": "Estruendo", "damage": 25, "type": AnimationType.DRAGON},
            {"name": "Pulso Dragon", "damage": 26, "type": AnimationType.DRAGON},
            {"name": "Bomba Magica", "damage": 22, "type": AnimationType.FAIRY},
            {"name": "Supersonica", "damage": -23, "type": AnimationType.HEAL}
        ]

        moves_aegislash = [
            {"name": "Espada Santa", "damage": 27, "type": AnimationType.STEEL},
            {"name": "Filo Real", "damage": 23, "type": AnimationType.STEEL},
            {"name": "Golpe Real", "damage": 25, "type": AnimationType.STEEL},
            {"name": "Escudo Real", "damage": -24, "type": AnimationType.HEAL}
        ]

        moves_mimikyu = [
            {"name": "Garra Umbria", "damage": 24, "type": AnimationType.DARK},
            {"name": "Juego Sucio", "damage": 22, "type": AnimationType.DARK},
            {"name": "Brillo Magico", "damage": 25, "type": AnimationType.FAIRY},
            {"name": "Disfraz", "damage": -26, "type": AnimationType.HEAL}
        ]
        # Lista actualizada de todos los Pokemon disponibles
        available_pokemon = [
            {"name": "Ceruledge", "image": "Juegos/Imagenes/pokemon1.jpg", "hp": 100, "moves": moves_ceruledge},
            {"name": "Zeraora", "image": "Juegos/Imagenes/pokemon2.jpg", "hp": 100, "moves": moves_zeraora},
            {"name": "Gengar", "image": "Juegos/Imagenes/pokemon3.jpg", "hp": 100, "moves": moves_gengar},
            {"name": "MissingNo", "image": "Juegos/Imagenes/pokemon4.jpg", "hp": 100, "moves": moves_missingno},
            {"name": "Agumon", "image": "Juegos/Imagenes/pokemon5.jpg", "hp": 100, "moves": moves_agumon},
            {"name": "Shadow", "image": "Juegos/Imagenes/pokemon6.jpg", "hp": 100, "moves": moves_shadow},
            {"name": "Gallade", "image": "Juegos/Imagenes/pokemon7.jpg", "hp": 100, "moves": moves_gallade},
            {"name": "Eelektross", "image": "Juegos/Imagenes/pokemon8.jpg", "hp": 100, "moves": moves_eelektross},
            {"name": "Zoroark", "image": "Juegos/Imagenes/pokemon9.jpg", "hp": 100, "moves": moves_zoroark},
            {"name": "Luxray", "image": "Juegos/Imagenes/pokemon10.jpg", "hp": 100, "moves": moves_luxray},
            {"name": "Froslass", "image": "Juegos/Imagenes/pokemon11.jpg", "hp": 100, "moves": moves_froslass},
            {"name": "Sceptile", "image": "Juegos/Imagenes/pokemon12.jpg", "hp": 100, "moves": moves_sceptile},
            {"name": "Gardevoir", "image": "Juegos/Imagenes/pokemon13.jpg", "hp": 100, "moves": moves_gardevoir},
            {"name": "Haxorus", "image": "Juegos/Imagenes/pokemon14.jpg", "hp": 100, "moves": moves_haxorus},
            {"name": "Chandelure", "image": "Juegos/Imagenes/pokemon15.jpg", "hp": 100, "moves": moves_chandelure},
            {"name": "Volcarona", "image": "Juegos/Imagenes/pokemon16.jpg", "hp": 100, "moves": moves_volcarona},
            {"name": "Metagross", "image": "Juegos/Imagenes/pokemon17.jpg", "hp": 100, "moves": moves_metagross},
            {"name": "Noivern", "image": "Juegos/Imagenes/pokemon18.jpg", "hp": 100, "moves": moves_noivern},
            {"name": "Aegislash", "image": "Juegos/Imagenes/pokemon19.jpg", "hp": 100, "moves": moves_aegislash},
            {"name": "Mimikyu", "image": "Juegos/Imagenes/pokemon20.jpg", "hp": 100, "moves": moves_mimikyu}
        ]

        # Seleccionar dos Pokemon aleatorios diferentes
        selected_pokemon = random.sample(available_pokemon, 2)
        
        # Crear los objetos Pokemon
        self.pokemon1 = Pokemon(
            selected_pokemon[0]["name"],
            selected_pokemon[0]["image"],
            selected_pokemon[0]["hp"],
            selected_pokemon[0]["moves"]
        )
        
        self.pokemon2 = Pokemon(
            selected_pokemon[1]["name"],
            selected_pokemon[1]["image"],
            selected_pokemon[1]["hp"],
            selected_pokemon[1]["moves"]
        )
        
        self.selected_option = 0
        self.battle_state = BattleState.SELECTING_ACTION
        self.current_message = "What will " + self.pokemon1.name + " do?"
        self.winner = None
        self.current_animation = None

    def create_animation(self, move, attacker_pos, target_pos):
        move_type = move.get("type", AnimationType.PHYSICAL)
        return Animation(move_type, attacker_pos, target_pos)

    def execute_move(self):
        if self.battle_state != BattleState.SELECTING_ACTION:
            return

        # Verificar si el jugador está vivo antes de ejecutar el movimiento
        if self.pokemon1.current_hp <= 0:
            self.battle_state = BattleState.BATTLE_ENDED
            self.winner = self.pokemon2.name
            return

        # Posiciones para las animaciones


        # Guardar el movimiento del enemigo para usarlo después
        self.enemy_move = random.choice(self.pokemon2.moves)
        
        # Iniciar la secuencia con el movimiento del jugador
        move = self.pokemon1.moves[self.selected_option]
        
        if move["damage"] < 0:  # Curación del jugador
            self.current_animation = Animation(AnimationType.HEAL, player_pos, player_pos)
            self.current_message = f"{self.pokemon1.name} is using {move['name']}!"
        else:  # Ataque del jugador
            self.current_animation = self.create_animation(move, player_pos, enemy_pos)
            self.current_message = f"{self.pokemon1.name} used {move['name']}!"

        self.current_move = move
        self.battle_state = BattleState.ANIMATING
        self.animation_start_time = time.time()
        self.is_player_turn = True



    def draw_background(self, frame):
        # Inicializar el sistema de partículas si no existe
        if not hasattr(self, 'particles'):
            self.particles = []
            for _ in range(50):  # Número de partículas
                self.particles.append({
                    'x': np.random.randint(0, self.width),
                    'y': np.random.randint(0, self.height),
                    'size': np.random.randint(1, 5),
                    'speed': np.random.uniform(1, 3),
                    'wind_offset': 0,
                    'wind_speed': np.random.uniform(0.5, 1.5)
                })

        # Cielo tormentoso con vórtice
        center_x, center_y = self.width // 2, self.height // 3
        for radius in range(0, max(self.width, self.height), 15):
            angle = radius / 40
            color_intensity = 255 - (radius * 255 // max(self.width, self.height))
            color = (
                min(int(color_intensity * 0.3), 255),
                min(int(color_intensity * 0.1), 255),
                min(int(color_intensity * 0.5), 255)
            )
            for theta in range(0, 360, 15):
                rad = math.radians(theta + angle)
                x1 = int(center_x + radius * math.cos(rad))
                y1 = int(center_y + radius * math.sin(rad))
                x2 = int(center_x + (radius + 5) * math.cos(rad))
                y2 = int(center_y + (radius + 5) * math.sin(rad))
                if 0 <= x1 < self.width and 0 <= y1 < self.height and 0 <= x2 < self.width and 0 <= y2 < self.height:
                    cv2.line(frame, (x1, y1), (x2, y2), color, 2)

        # Sistema de tiempo para los rayos
        current_time = time.time()
        if not hasattr(self, 'last_lightning_time'):
            self.last_lightning_time = current_time
        
        # Actualizar el tiempo de los rayos cada 2.5 segundos
        if current_time - self.last_lightning_time >= 2.5:
            self.should_draw_lightning = True
            self.last_lightning_time = current_time
            self.lightning_positions = [(np.random.randint(0, self.width), 0) for _ in range(2)]
            self.lightning_intensity = 255

        # Dibujar rayos con desvanecimiento
        if hasattr(self, 'should_draw_lightning') and self.should_draw_lightning:
            for start_pos in self.lightning_positions:
                points = [start_pos]
                for _ in range(6):
                    prev_x, prev_y = points[-1]
                    new_x = prev_x + np.random.randint(-120, 120)
                    new_y = prev_y + self.height // 6
                    points.append((new_x, new_y))
                
                points = np.array(points, np.int32)
                
                cv2.polylines(frame, [points], False, (0, 0, self.lightning_intensity), 8)
                cv2.polylines(frame, [points], False, (self.lightning_intensity, self.lightning_intensity, self.lightning_intensity), 4)
                
                for i in range(len(points) - 1):
                    if np.random.random() < 0.5:
                        branch_start = points[i]
                        branch_points = [branch_start]
                        for _ in range(3):
                            prev_x, prev_y = branch_points[-1]
                            new_x = prev_x + np.random.randint(-60, 60)
                            new_y = prev_y + self.height // 8
                            branch_points.append((new_x, new_y))
                        
                        branch_points = np.array(branch_points, np.int32)
                        cv2.polylines(frame, [branch_points], False, (0, 0, self.lightning_intensity), 4)
                        cv2.polylines(frame, [branch_points], False, (self.lightning_intensity, self.lightning_intensity, self.lightning_intensity), 2)
            
            self.lightning_intensity -= 25
            if self.lightning_intensity <= 0:
                self.should_draw_lightning = False

        # Actualizar y dibujar partículas flotantes
        wind_time = self.frame_count / 30  # Tiempo para el movimiento del viento
        for particle in self.particles:
            # Actualizar posición
            particle['wind_offset'] += particle['wind_speed']
            wind_x = math.sin(wind_time + particle['wind_offset']) * 2  # Movimiento sinusoidal del viento
            
            # Mover partícula
            particle['x'] += wind_x
            particle['y'] += particle['speed']
            
            # Reiniciar si sale de la pantalla
            if particle['y'] > self.height:
                particle['y'] = 0
                particle['x'] = np.random.randint(0, self.width)
            if particle['x'] < 0:
                particle['x'] = self.width
            if particle['x'] > self.width:
                particle['x'] = 0
                
            # Dibujar partícula con brillo sutil
            alpha = np.random.uniform(0.5, 0.8)  # Variar la opacidad
            color = (
                int(100 * alpha),  # Tono grisáceo
                int(100 * alpha),
                int(120 * alpha)
            )
            cv2.circle(frame, (int(particle['x']), int(particle['y'])), 
                    particle['size'], color, -1)

        # Plataformas flotantes
        def draw_epic_platform(center_x, center_y):
            for i in range(20, 0, -2):
                alpha = i / 20
                color = (
                    int(180 * alpha),
                    int(40 * alpha),
                    int(255 * alpha)
                )
                size = (120 + i*2, 40 + i//2)
                cv2.ellipse(frame, (center_x, center_y), size, 0, 0, 360, color, -1)
            
            cv2.ellipse(frame, (center_x, center_y), (120, 40), 0, 0, 360, (80, 80, 100), -1)
            cv2.ellipse(frame, (center_x, center_y), (110, 35), 0, 0, 360, (120, 120, 140), 2)
            cv2.ellipse(frame, (center_x, center_y-5), (90, 25), 0, 0, 180, (200, 200, 220), 2)

        draw_epic_platform(150, 250)
        draw_epic_platform(650, 250)

        self.frame_count = (self.frame_count + 1) % 360

    def draw_menu(self):
        # Create separate menu frame
        menu_frame = np.zeros((self.menu_height, self.menu_width, 3), dtype=np.uint8)
        
        # Fill with dark background
        cv2.rectangle(menu_frame, (0, 0), (self.menu_width, self.menu_height), (0, 0, 0), -1)
        
        # Dibujar movimientos en matriz 2x2 solo si estamos seleccionando accion
        if self.battle_state == BattleState.SELECTING_ACTION:
            moves_per_row = 2
            cell_width = self.menu_width // moves_per_row
            cell_height = self.menu_height // 2
            
            for i, move in enumerate(self.pokemon1.moves):
                row = i // moves_per_row
                col = i % moves_per_row
                
                x = col * cell_width
                y = row * cell_height
                
                # Obtener el color segun el tipo de movimiento
                move_type = move.get("type", AnimationType.PHYSICAL)
                move_color = self.move_type_colors.get(move_type, self.text_color)
                
                # Dibujar rectangulo de fondo
                box_width = cell_width * 0.95
                box_height = cell_height * 0.9
                box_x = int(x + (cell_width - box_width) / 2)
                box_y = int(y + (cell_height - box_height) / 2)
                
                cv2.rectangle(menu_frame,
                            (box_x, box_y),
                            (int(box_x + box_width), int(box_y + box_height)),
                            move_color, 2)
                
                # Calcular el tamaño del texto para centrarlo
                text_color = (255, 255, 255) if i == self.selected_option else move_color
                move_name = move["name"]
                
                # Calcular el espacio disponible para el nombre y el daño
                target_width = box_width * 0.8
                name_height = box_height * 0.4
                
                # Calcular escala para el nombre
                font_scale = 1.0
                text_size = cv2.getTextSize(move_name, cv2.FONT_HERSHEY_SIMPLEX, font_scale, 2)[0]
                
                width_scale = target_width / text_size[0]
                height_scale = name_height / text_size[1]
                font_scale = min(width_scale, height_scale) * 0.9
                
                # Posicionar el nombre en el tercio superior de la caja
                text_size = cv2.getTextSize(move_name, cv2.FONT_HERSHEY_SIMPLEX, font_scale, 2)[0]
                text_x = box_x + (box_width - text_size[0]) // 2
                text_y = box_y + box_height * 0.43  # Movido mas arriba
                
                # Dibujar el nombre del movimiento
                cv2.putText(menu_frame, move_name,
                        (int(text_x), int(text_y)),
                        cv2.FONT_HERSHEY_SIMPLEX, font_scale,
                        text_color, 3, cv2.LINE_AA)
                
                # Calcular y dibujar el daño en el tercio inferior
                damage_text = f"({abs(move['damage'])} {'HP' if move['damage'] < 0 else 'DMG'})"
                damage_font_scale = font_scale * 0.55  # Reducido ligeramente
                damage_size = cv2.getTextSize(damage_text, cv2.FONT_HERSHEY_SIMPLEX, damage_font_scale, 2)[0]
                damage_x = box_x + (box_width - damage_size[0]) // 2
                
                # Posicionar el daño mas abajo
                damage_y = int(box_y + box_height * 0.8)  # Movido mas abajo
                
                cv2.putText(menu_frame, damage_text,
                        (int(damage_x), damage_y),
                        cv2.FONT_HERSHEY_SIMPLEX, damage_font_scale,
                        move_color, 2, cv2.LINE_AA)
        
        return menu_frame


    def draw(self):
        # Create main battle frame
        battle_frame = np.zeros((self.height, self.width, 3), dtype=np.uint8)
        
        # Dibujar fondo
        self.draw_background(battle_frame)
        
        # Dibujar Pokemon con efecto de daño si corresponde
        pokemon1_y = 100
        pokemon2_y = 100
        
        # Crear copias de las imágenes para aplicar efectos
        pokemon1_img = self.pokemon1.image.copy()
        pokemon2_img = self.pokemon2.image.copy()
        
        # Remover fondo verde y obtener máscaras alpha
        pokemon1_img, alpha1 = remove_green_background(pokemon1_img)
        pokemon2_img, alpha2 = remove_green_background(pokemon2_img)
        
        pokemon2_img = cv2.flip(pokemon2_img, 1)
        alpha2 = cv2.flip(alpha2, 1)

        # Aplicar efecto de flash rojo si corresponde
        if self.is_flashing:
            current_time = time.time()
            flash_elapsed = current_time - self.damage_flash_start
            
            if flash_elapsed < self.damage_flash_duration:
                # Calcular intensidad del flash (oscilación)
                flash_intensity = abs(math.sin(flash_elapsed * 10)) * 0.7
                
                if self.flash_target == "player":
                    pokemon1_img = self.apply_damage_flash(pokemon1_img, flash_intensity)
                else:
                    pokemon2_img = self.apply_damage_flash(pokemon2_img, flash_intensity)
            else:
                self.is_flashing = False
        
        # Dibujar los Pokemon con alpha blending
        # Pokemon 1
        roi1 = battle_frame[pokemon1_y:pokemon1_y+200, 50:250]
        alpha1_3d = np.stack([alpha1/255.0]*3, axis=2)
        roi1[:] = (pokemon1_img * alpha1_3d + roi1 * (1 - alpha1_3d)).astype(np.uint8)
        
        # Pokemon 2
        roi2 = battle_frame[pokemon2_y:pokemon2_y+200, 550:750]
        alpha2_3d = np.stack([alpha2/255.0]*3, axis=2)
        roi2[:] = (pokemon2_img * alpha2_3d + roi2 * (1 - alpha2_3d)).astype(np.uint8)
        
        # El resto del método draw permanece igual...
        # Actualizar y dibujar las barras de vida
        self.update_health_animation()
        
        # Dibujar barras de vida
        bar_y1 = pokemon1_y - 30
        self.draw_health_bar(battle_frame, 50, bar_y1, 200, self.pokemon1.current_hp, self.pokemon1.max_hp)
        cv2.putText(battle_frame, f"{self.pokemon1.name} HP: {int(self.pokemon1.current_hp)}/{self.pokemon1.max_hp}",
                    (50, bar_y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, self.text_color, 1, cv2.LINE_AA)
        
        bar_y2 = pokemon2_y - 30
        self.draw_health_bar(battle_frame, 550, bar_y2, 200, self.pokemon2.current_hp, self.pokemon2.max_hp)
        cv2.putText(battle_frame, f"{self.pokemon2.name} HP: {int(self.pokemon2.current_hp)}/{self.pokemon2.max_hp}",
                    (550, bar_y2 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, self.text_color, 1, cv2.LINE_AA)

        # Actualizar y dibujar animación si existe
        if self.current_animation:
            self.current_animation.update_and_draw(battle_frame)
            
        # Actualizar el estado de la batalla
        self.update_battle_state()

        message_y = pokemon1_y + 220
        padding = 10
        border_thickness = 2
        box_height = 60

        # Dibujar el borde blanco exterior (fondo)
        cv2.rectangle(battle_frame,
                    (40, message_y - padding),
                    (self.width - 40, message_y + box_height),
                    (255, 255, 255), -1)

        # Dibujar el rectángulo negro interior
        cv2.rectangle(battle_frame,
                    (40 + border_thickness, message_y - padding + border_thickness),
                    (self.width - 40 - border_thickness, message_y + box_height - border_thickness),
                    (0, 0, 0), -1)

        # Agregar el triángulo pequeño de continuación en la esquina inferior derecha
        triangle_points = np.array([
            [self.width - 60, message_y + box_height - 15],
            [self.width - 50, message_y + box_height - 15],
            [self.width - 55, message_y + box_height - 10]
        ], np.int32)
        cv2.fillPoly(battle_frame, [triangle_points], (255, 255, 255))

        # Dibujar el texto con un estilo más parecido al juego
        cv2.putText(battle_frame, f"{self.current_message}!",
                    (60, message_y + 25),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7,
                    (255, 255, 255), 1, cv2.LINE_AA)

        # Mostrar mensaje de victoria en la ventana principal
        if self.battle_state == BattleState.BATTLE_ENDED:
            victory_text = f"{self.winner} wins! Press R to restart"
            text_size = cv2.getTextSize(victory_text, cv2.FONT_HERSHEY_SIMPLEX, 1, 2)[0]
            text_x = (self.width - text_size[0]) // 2
            text_y = self.height // 2
            cv2.putText(battle_frame, victory_text,
                    (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
            
        return battle_frame, self.draw_menu()

    def are_animations_finished(self):
        """Comprueba si todas las animaciones han terminado y ha pasado el delay"""
        return (not self.health_animation and 
                not self.is_flashing and 
                not self.current_animation and
                time.time() - self.last_animation_end >= 0.5)

    def update_battle_state(self):
        current_time = time.time()
        
        # Si hay una animacion en curso
        if self.current_animation:
            if self.current_animation.is_finished():
                # Aplicar el daño o curacion despues de que termine la animacion
                if self.is_player_turn:
                    if self.current_move["damage"] < 0:  # Curacion del jugador
                        heal_amount = min(-self.current_move["damage"], 
                                        self.pokemon1.max_hp - self.pokemon1.current_hp)
                        new_hp = self.pokemon1.current_hp + heal_amount
                        self.start_health_animation(self.pokemon1, new_hp)
                        self.current_message = f"{self.pokemon1.name} healed for {heal_amount} HP!"
                    else:  # Daño al enemigo
                        new_hp = max(0, self.pokemon2.current_hp - self.current_move["damage"])
                        self.start_health_animation(self.pokemon2, new_hp)
                        self.start_damage_animation(False)  # Animacion de daño al enemigo
                        self.current_message = f"{self.pokemon2.name} took {self.current_move['damage']} damage!"
                        
                        # Verificar si el enemigo fue derrotado inmediatamente
                        if new_hp <= 0:
                            self.pokemon2.current_hp = 0
                            self.battle_state = BattleState.BATTLE_ENDED
                            self.winner = self.pokemon1.name
                            self.current_message = f"{self.pokemon2.name} fainted!"
                            return
                else:
                    if self.enemy_move["damage"] < 0:  # Curacion del enemigo
                        heal_amount = min(-self.enemy_move["damage"], 
                                        self.pokemon2.max_hp - self.pokemon2.current_hp)
                        new_hp = self.pokemon2.current_hp + heal_amount
                        self.start_health_animation(self.pokemon2, new_hp)
                        self.current_message = f"{self.pokemon2.name} healed for {heal_amount} HP!"
                    else:  # Daño al jugador
                        new_hp = max(0, self.pokemon1.current_hp - self.enemy_move["damage"])
                        self.start_health_animation(self.pokemon1, new_hp)
                        self.start_damage_animation(True)  # Animacion de daño al jugador
                        self.current_message = f"{self.pokemon1.name} took {self.enemy_move['damage']} damage!"
                        
                        # Verificar si el jugador fue derrotado inmediatamente
                        if new_hp <= 0:
                            self.pokemon1.current_hp = 0
                            self.battle_state = BattleState.BATTLE_ENDED
                            self.winner = self.pokemon2.name
                            self.current_message = f"{self.pokemon1.name} fainted!"
                            return

                self.current_animation = None
                self.wait_start_time = time.time()
                self.is_waiting = True

        # Manejar el estado de espera
        if hasattr(self, 'is_waiting') and self.is_waiting:
            if time.time() - self.wait_start_time >= 1.0:
                self.is_waiting = False
                
                # Si acabamos de terminar la animacion del jugador y el enemigo sigue vivo
                if self.battle_state == BattleState.ANIMATING and self.is_player_turn:
                    if self.pokemon2.current_hp > 0:  # Solo continuar si el enemigo sigue vivo
                        self.is_player_turn = False
                        enemy_pos = (650, 150)
                        player_pos = (150, 150)
                        
                        if self.enemy_move["damage"] < 0:
                            self.current_animation = Animation(AnimationType.HEAL, enemy_pos, enemy_pos)
                            self.current_message = f"{self.pokemon2.name} is using {self.enemy_move['name']}!"
                        else:
                            self.current_animation = self.create_animation(self.enemy_move, enemy_pos, player_pos)
                            self.current_message = f"{self.pokemon2.name} used {self.enemy_move['name']}!"
                
                # Si acabamos de terminar la animacion del enemigo y nadie ha muerto
                elif self.battle_state == BattleState.ANIMATING and not self.is_player_turn:
                    if self.battle_state != BattleState.BATTLE_ENDED:
                        self.battle_state = BattleState.SELECTING_ACTION
                        self.current_message = f"What will {self.pokemon1.name} do?"

    def apply_damage_flash(self, image, intensity):
        # Crear una mascara roja con la intensidad especificada
        red_overlay = np.zeros_like(image)
        red_overlay[:, :, 2] = 255  # Canal rojo
        
        # Combinar la imagen original con el overlay rojo
        return cv2.addWeighted(image, 1.0, red_overlay, intensity, 0)


    def start_damage_animation(self, is_player):
        self.is_flashing = True
        self.flash_target = "player" if is_player else "enemy"
        self.damage_flash_start = time.time()
        
    def start_health_animation(self, pokemon, new_hp):
        start_hp = pokemon.current_hp
        self.health_animation = {
            'pokemon': pokemon,
            'start_hp': start_hp,
            'end_hp': new_hp,
            'start_time': time.time(),
            'duration': 0.5  # duracion en segundos
        }

    def update_health_animation(self):
        if not self.health_animation:
            return
            
        current_time = time.time()
        animation = self.health_animation
        elapsed = current_time - animation['start_time']
        progress = min(elapsed / animation['duration'], 1.0)
        
        if progress >= 1.0:
            animation['pokemon'].current_hp = animation['end_hp']
            self.health_animation = None
        else:
            # Interpolacion lineal entre HP inicial y final
            hp_diff = animation['end_hp'] - animation['start_hp']
            animation['pokemon'].current_hp = animation['start_hp'] + (hp_diff * progress)



    def draw_health_bar(self, frame, x, y, width, current_hp, max_hp):
        health_percentage = current_hp / max_hp
        # Determinar color basado en HP
        if health_percentage > 0.5:
            bar_color = (0, 255, 0)  # Verde
        elif health_percentage > 0.2:
            bar_color = (0, 255, 255)  # Amarillo
        else:
            bar_color = (0, 0, 255)  # Rojo
            
        # Dibujar barra base (gris)
        cv2.rectangle(frame, (x, y), (x + width, y + 20), (128, 128, 128), -1)
        
        # Dibujar borde negro
        cv2.rectangle(frame, (x, y), (x + width, y + 20), (0, 0, 0), 2)
        
        # Dibujar barra de vida actual
        bar_width = int(width * health_percentage)
        if bar_width > 0:
            cv2.rectangle(frame, (x + 2, y + 2), (x + bar_width - 2, y + 18), bar_color, -1)
            
        # Añadir efecto de brillo
        shine_width = min(5, bar_width - 4)
        if shine_width > 0:
            cv2.rectangle(frame, (x + 2, y + 2), (x + shine_width, y + 6), 
                         (255, 255, 255), -1, cv2.LINE_AA)

    def handle_input(self, key):
        if self.battle_state == BattleState.BATTLE_ENDED:
            if key == ord('r'):  # Reiniciar juego
                self.reset_battle()
            return
                
        if self.battle_state == BattleState.SELECTING_ACTION:
            if key == ord('w') or key == 82:  # Arriba
                self.selected_option = (self.selected_option - 2) % 4
            elif key == ord('s') or key == 84:  # Abajo
                self.selected_option = (self.selected_option + 2) % 4
            elif key == ord('a') or key == 81:  # Izquierda
                if self.selected_option % 2 == 1:
                    self.selected_option -= 1
            elif key == ord('d') or key == 83:  # Derecha
                if self.selected_option % 2 == 0 and self.selected_option + 1 < 4:
                    self.selected_option += 1
            elif key == ord('\r') or key == ord(' '):  # Enter o espacio
                self.execute_move()
            elif key == ord('r'):  # Enter o espacio
                self.reset_battle()

# Variables globales para el estado del juego
_pokemon_battle = None

def handle_key(key):
    global _pokemon_battle
    if _pokemon_battle:
        _pokemon_battle.handle_input(key)

def get_frames():
    global _pokemon_battle
    
    # Inicializar el juego si es la primera vez
    if _pokemon_battle is None:
        _pokemon_battle = PokemonBattle()
    
    # Crear y retornar los frames
    return _pokemon_battle.draw()

# Codigo para prueba independiente
if __name__ == "__main__":
    cv2.namedWindow('Pokemon Battle')
    cv2.namedWindow('Battle Menu')
    
    while True:
        battle_frame, menu_frame = get_frames()
        cv2.imshow('Pokemon Battle', battle_frame)
        cv2.imshow('Battle Menu', menu_frame)
        
        key = cv2.waitKey(1) & 0xFF
        if key == 27:  # Esc
            break
        handle_key(key)
    
    cv2.destroyAllWindows()