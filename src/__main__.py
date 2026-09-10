from .graphics import Screen, Position, Color, OperationEnum
from src.graphics.meshes import Polygon, Plane

import random
import pygame


if __name__ == "__main__":
    pygame.init()

    pygame_screen = pygame.display.set_mode((600, 800), pygame.SRCALPHA)

    screen: Screen = Screen(600, 800, pygame_screen)

    plane = Plane(
        Color(255, 0, 0),
        (Position(0, 0), Position(599, 799))
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
            thickness=2,
            operation=OperationEnum.SUBTRACT,
            is_dynamic=True
        )

    poly2 = Polygon(
            Color(0, 0, 255, 50),
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
            thickness=2,
            operation=OperationEnum.MULTIPLY,
            is_dynamic=True
        )

    screen.add_mesh(plane)
    print("1")
    screen.init()
    print("2")

    pygame.display.flip()

    # poly.color

    while True:
        pygame.display.flip()
