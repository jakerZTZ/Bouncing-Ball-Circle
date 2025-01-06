import pygame
import random
import math

# Inicializar pygame
pygame.init()

# Configuración de la ventana
WIDTH, HEIGHT = 800, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Círculo con pelota rebotando")

# Colores
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BALL_COLOR = (255, 50, 50)
CIRCLE_COLORS = [(0, 255, 0), (0, 200, 255), (255, 200, 0), (255, 50, 200)]

# Configuración del círculo
circle_center = (WIDTH // 2, HEIGHT // 2)
initial_radius = 100
radius_increment = 10
circle_layers = 5

# Configuración de la pelota
ball_radius = 10
ball_x = random.randint(initial_radius, WIDTH - initial_radius)
ball_y = random.randint(initial_radius, HEIGHT - initial_radius)
ball_speed = 5
ball_angle = random.uniform(0, 2 * math.pi)  # Dirección inicial aleatoria

# Configuración de la "salida"
exit_angle_start = math.pi / 4  # Ángulo inicial del sector de salida
exit_angle_end = math.pi / 3   # Ángulo final del sector de salida

running = True
clock = pygame.time.Clock()

def draw_circle_with_layers():
    for i in range(circle_layers):
        radius = initial_radius + i * radius_increment
        color = CIRCLE_COLORS[i % len(CIRCLE_COLORS)]  # Colores cíclicos
        pygame.draw.circle(screen, color, circle_center, radius, 2)  # Círculo con borde

def draw_exit_sector():
    start_x = circle_center[0] + math.cos(exit_angle_start) * (initial_radius + (circle_layers - 1) * radius_increment)
    start_y = circle_center[1] + math.sin(exit_angle_start) * (initial_radius + (circle_layers - 1) * radius_increment)
    end_x = circle_center[0] + math.cos(exit_angle_end) * (initial_radius + (circle_layers - 1) * radius_increment)
    end_y = circle_center[1] + math.sin(exit_angle_end) * (initial_radius + (circle_layers - 1) * radius_increment)
    pygame.draw.line(screen, WHITE, circle_center, (start_x, start_y), 2)
    pygame.draw.line(screen, WHITE, circle_center, (end_x, end_y), 2)

def move_ball():
    global ball_x, ball_y, ball_angle

    # Mover la pelota
    ball_x += math.cos(ball_angle) * ball_speed
    ball_y += math.sin(ball_angle) * ball_speed

    # Detectar colisiones con los bordes
    if ball_x - ball_radius <= 0 or ball_x + ball_radius >= WIDTH:
        ball_angle = math.pi - ball_angle + random.uniform(-0.2, 0.2)  # Rebote aleatorio en X
    if ball_y - ball_radius <= 0 or ball_y + ball_radius >= HEIGHT:
        ball_angle = -ball_angle + random.uniform(-0.2, 0.2)  # Rebote aleatorio en Y

    # Limitar el ángulo dentro de 0 a 2pi
    ball_angle %= 2 * math.pi

    # Detectar si pasa por el sector de salida
    detect_exit()

def detect_exit():
    global circle_layers

    # Calcular el ángulo actual de la pelota con respecto al centro
    dx, dy = ball_x - circle_center[0], ball_y - circle_center[1]
    ball_angle_to_center = math.atan2(dy, dx)
    if ball_angle_to_center < 0:
        ball_angle_to_center += 2 * math.pi

    # Verificar si la pelota está dentro del sector de salida
    if exit_angle_start <= ball_angle_to_center <= exit_angle_end:
        # Añadir una nueva capa al círculo
        add_circle_layer()

def add_circle_layer():
    global circle_layers
    circle_layers += 1

def main():
    global running

    while running:
        screen.fill(BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Dibujar círculo, sector de salida y pelota
        draw_circle_with_layers()
        draw_exit_sector()
        pygame.draw.circle(screen, BALL_COLOR, (int(ball_x), int(ball_y)), ball_radius)

        # Mover la pelota
        move_ball()

        # Actualizar la pantalla
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
