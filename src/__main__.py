from .graphics import Screen, Position, Color

import pygame


if __name__ == "__main__":
    pygame.init()

    pygame_screen = pygame.display.set_mode((800, 600))

    screen: Screen = Screen(800, 600, pygame_screen)
    screen.put_line(Position(10, 10), Position(500, 500), Color(255, 255, 255), thickness=50)
    # screen.put_line(Position(10, 11), Position(500, 501), Color(255, 255, 255), thickness=1)
    # screen.put_line(Position(10, 12), Position(500, 502), Color(255, 255, 255), thickness=1)
    # screen.put_line(Position(10, 13), Position(500, 503), Color(255, 255, 255), thickness=1)
    # screen.put_line(Position(10, 14), Position(500, 504), Color(255, 255, 255), thickness=1)
    # screen.put_line(Position(10, 15), Position(500, 505), Color(255, 255, 255), thickness=1)
    # screen.put_line(Position(10, 16), Position(500, 506), Color(255, 255, 255), thickness=1)
    # screen.put_line(Position(10, 17), Position(500, 507), Color(255, 255, 255), thickness=1)
    # screen.put_line(Position(10, 18), Position(500, 508), Color(255, 255, 255), thickness=1)
    # screen.put_line(Position(10, 19), Position(500, 509), Color(255, 255, 255), thickness=1)
    # screen.put_line(Position(20, 20), Position(500, 510), Color(255, 255, 255), thickness=1)
    # screen.put_line(Position(20, 21), Position(500, 511), Color(255, 255, 255), thickness=1)

    while True:
        pygame.display.flip()

