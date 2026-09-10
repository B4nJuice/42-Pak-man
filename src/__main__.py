from .graphics import Screen, Position, Color, OperationEnum
from src.graphics.meshes import Plane, Polygon

import random
import pygame


if __name__ == "__main__":
    pygame.init()
    # print("ok")

    width, height = 800, 600
    pygame_screen = pygame.display.set_mode(
        (width, height),
        pygame.OPENGL | pygame.DOUBLEBUF
    )
    pygame.display.set_caption("Plane refresh test")
    clock = pygame.time.Clock()

    screen: Screen = Screen(width, height, pygame_screen)

    background = Plane(
        Color(255, 0, 0),
        (Position(0, 0), Position(width, height))
    )

    poly = Polygon(
            Color(0, 255, 0, 50),
            [
                Position(80, 100),
                Position(250, 50),
                Position(470, 120),
                Position(540, 300),
                Position(450, 500),
                Position(500, 700),
                Position(300, 750),
                Position(120, 650),
                Position(60, 450),
                Position(140, 300),
            ],
            thickness=15,
            operation=OperationEnum.MULTIPLY,
            is_dynamic=True
        )

    plane_one = Plane(
        Color(0, 255, 0),
        (Position(100, 100), Position(300, 250)),
        is_dynamic=True,
        operation=OperationEnum.DIFFERENCE
    )
    plane_two = Plane(
        Color(0, 0, 255),
        (Position(450, 300), Position(700, 500)),
        is_dynamic=True,
        operation=OperationEnum.AVERAGE
    )

    screen.add_mesh(background)
    screen.add_mesh(plane_one)
    screen.add_mesh(plane_two)
    screen.add_mesh(poly)
    screen.init()
    pygame.display.flip()

    running = True
    elapsed = 0
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False


        for plane in (plane_one, plane_two):
            plane.color = Color(
                random.randrange(256),
                random.randrange(256),
                random.randrange(256)
            )

            x_start = random.randrange(width - 80)
            y_start = random.randrange(height - 80)
            plane.positions = (
                Position(x_start, y_start),
                Position(
                    random.randrange(x_start + 20, min(width, x_start + 300)),
                    random.randrange(y_start + 20, min(height, y_start + 300))
                )
            )
            screen.dynamic_mesh_layer.refresh_mesh(plane)

        poly.positions = [
                Position(random.randint(0,800), random.randint(0,600)),
                Position(random.randint(0,800), random.randint(0,600)),
                Position(random.randint(0,800), random.randint(0,600)),
                Position(random.randint(0,800), random.randint(0,600)),
                Position(random.randint(0,800), random.randint(0,600)),
                Position(random.randint(0,800), random.randint(0,600)),
                Position(random.randint(0,800), random.randint(0,600)),
                Position(random.randint(0,800), random.randint(0,600)),
                Position(random.randint(0,800), random.randint(0,600)),
                Position(random.randint(0,800), random.randint(0,600)),
            ]
        screen.dynamic_mesh_layer.refresh_mesh(poly)

        screen.refresh_dynamic()
        pygame.display.flip()

    pygame.quit()
