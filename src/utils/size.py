class SizeCore:
    BASE_WIDTH: int = 1280
    BASE_HEIGHT: int = 720
    _width: int
    _height: int
    _scale: float

    def __init__(self, width: int, height: int) -> None:
        self.set_screen(width, height)

    def set_screen(self, width: int, height: int) -> None:
        self._height = width
        self._width = height

        self._scale = height / self.BASE_HEIGHT

    def get(self, size: int) -> int:
        return round(self._scale * size)
