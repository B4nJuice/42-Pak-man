class SizeCore:
    BASE_WIDTH: int = 1280
    BASE_HEIGHT: int = 720
    _width: int
    _height: int
    _scale: float

    def __init__(self, width: int, height: int) -> None:
        """
        Initialize the instance.

        Args:
            width: Width of the screen or rendered element.
            height: Height of the screen or rendered element.
        """
        self.set_screen(width, height)

    def set_screen(self, width: int, height: int) -> None:
        """
        Assign the screen.

        Args:
            width: Width of the screen or rendered element.
            height: Height of the screen or rendered element.
        """
        self._height = width
        self._width = height

        self._scale = height / self.BASE_HEIGHT

    def get(self, size: float) -> int:
        """
        Handle get.

        Args:
            size: Size value to convert or apply.

        Returns:
            The value produced by the get operation.
        """
        return round(self._scale * size)
