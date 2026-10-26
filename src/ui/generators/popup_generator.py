from src.graphics import Color, OperationEnum, Position
from src.graphics.meshes.plane import Plane
from src.graphics.super_meshes.rectangle import Rectangle
from src.utils.size import SizeCore


def generate_popup_bg(
            width: int,
            height: int,
            bg_color: Color,
            border_color: Color,
            border_tickness: int,
            screen_width: int,
            screen_height: int,
            size: SizeCore,
            border_inside: bool = True,
            position: Position | None = None
        ) -> tuple[Position, tuple[int, int], Plane, Rectangle]:

    r_width: int = size.get(width)
    r_height: int = size.get(height)
    r_border_tickness: int = size.get(2)

    if position is None:
        position = Position(
            round(screen_width / 2 - r_width / 2),
            round(screen_height / 2 - r_height / 2),
        )

    bg: Plane = Plane(
        color=bg_color,
        dynamic=False,
        operation=OperationEnum.SET,
        positions=(
            position,
            Position(position.x + r_width, position.y + r_height)
        )
    )

    border: Rectangle = Rectangle(
        color=border_color,
        dynamic=False,
        position=Position(
            position.x - (r_border_tickness if not border_inside else 0),
            position.y - (r_border_tickness if not border_inside else 0)
        ),
        width=r_width + (r_border_tickness * 2 if not border_inside else 0),
        height=r_height + (r_border_tickness * 2 if not border_inside else 0),
        operation=OperationEnum.SET,
        thickness=r_border_tickness,
        smooth_end=True
    )

    return (position, (r_width, r_height), bg, border)
