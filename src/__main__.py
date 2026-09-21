from .graphics import Screen, Position, Color, OperationEnum
from src.graphics.meshes import Plane, Polygon, ImageTexture

import random
import pygame


if __name__ == "__main__":
    pygame.init()

    pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MAJOR_VERSION, 3)
    pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MINOR_VERSION, 3)
    pygame.display.gl_set_attribute(
        pygame.GL_CONTEXT_PROFILE_MASK, pygame.GL_CONTEXT_PROFILE_CORE
    )
    pygame.display.gl_set_attribute(pygame.GL_CONTEXT_FORWARD_COMPATIBLE_FLAG, True)

    clock = pygame.time.Clock()

    width, height = 1920, 1080
    pygame_screen = pygame.display.set_mode(
        (width, height),
        pygame.OPENGL | pygame.DOUBLEBUF,
    )
    pygame.display.set_caption("Plane refresh test")
    screen: Screen = Screen(width, height, pygame_screen)

    background = Plane(
        Color(255, 0, 0),
        (Position(0, 0), Position(width, height)),
        is_dynamic=True
    )

    poly = Polygon(
            Color(10, 128, 255, 50),
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
            operation=OperationEnum.MAXIMUM,
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
        operation=OperationEnum.ADD
    )

    image = ImageTexture(
        "/home/lgirard/Downloads/PulpLogoInvert.png",
        Position(100, 100),
        width=100,
        height=200,
        is_dynamic=True,
        operation=OperationEnum.ADD
    )

    screen.add_mesh(background)
    screen.add_mesh(plane_one)
    screen.add_mesh(plane_two)
    screen.add_mesh(poly)
    screen.add_mesh(image)
    screen.refresh()
    pygame.display.flip()

    running = True
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

        background.color = Color(
                random.randrange(256),
                random.randrange(256),
                random.randrange(256)
            )

        poly.color = Color(
                random.randrange(256),
                random.randrange(256),
                random.randrange(256)
            )

        poly.positions = [
                Position(random.randint(0, width), random.randint(0, height))
                for _ in range(10)
            ]

        image.width = random.randint(100, width)
        image.height = random.randint(100, height)
        image.position = Position(
            random.randint(image.width // 2, width - image.width // 2),
            random.randint(image.height // 2, height - image.height // 2),
        )
        image.operation = random.choice(list(OperationEnum))

        screen.refresh()
        pygame.display.flip()
        clock.tick(60)

    screen.release()
    pygame.quit()
