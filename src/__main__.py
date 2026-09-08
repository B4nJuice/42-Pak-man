from .graphics import Screen, Position, Color, OperationEnum

import pygame


if __name__ == "__main__":
    pygame.init()

    pygame_screen = pygame.display.set_mode((600, 800))

    screen: Screen = Screen(600, 800, pygame_screen)
    screen.put_polygon(
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
            Color(255, 255, 0, 255),
            thickness=5
        )
    
    screen.put_polygon(
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
            Color(255, 100, 0, 50),
            thickness=5,
            operation=OperationEnum.AVERAGE
        )

    while True:
        pygame.display.flip()

