from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.graphics import Color


class ColorOperations:
    @staticmethod
    def set_color(
            color: 'Color',
            new_color: 'Color'
        ) -> list[int]:
        return [
            new_color.r,
            new_color.g,
            new_color.b,
            new_color.a
        ]

    @staticmethod
    def add(
            color: 'Color',
            other: 'Color'
        ) -> list[int]:
        return [
            color.r + other.r,
            color.g + other.g,
            color.b + other.b,
            color.a
        ]

    @staticmethod
    def subtract(
            color: 'Color',
            other: 'Color'
        ) -> list[int]:
        return [
            color.r - other.r,
            color.g - other.g,
            color.b - other.b,
            color.a
        ]

    @staticmethod
    def multiply(
            color: 'Color',
            other: 'Color'
        ) -> list[int]:
        return [
            color.r * other.r // 255,
            color.g * other.g // 255,
            color.b * other.b // 255,
            color.a
        ]

    @staticmethod
    def divide(
            color: 'Color',
            other: 'Color'
        ) -> list[int]:
        return [
            255 if other.r == 0 else color.r * 255 // other.r,
            255 if other.g == 0 else color.g * 255 // other.g,
            255 if other.b == 0 else color.b * 255 // other.b,
            color.a
        ]

    @staticmethod
    def minimum(
            color: 'Color',
            other: 'Color'
        ) -> list[int]:
        return [
            min(color.r, other.r),
            min(color.g, other.g),
            min(color.b, other.b),
            min(color.a, other.a)
        ]

    @staticmethod
    def maximum(
            color: 'Color',
            other: 'Color'
        ) -> list[int]:
        return [
            max(color.r, other.r),
            max(color.g, other.g),
            max(color.b, other.b),
            max(color.a, other.a)
        ]

    @staticmethod
    def average(
            color: 'Color',
            other: 'Color'
        ) -> list[int]:
        return [
            (color.r + other.r) // 2,
            (color.g + other.g) // 2,
            (color.b + other.b) // 2,
            (color.a + other.a) // 2
        ]

    @staticmethod
    def screen(
            color: 'Color',
            other: 'Color'
        ) -> list[int]:
        return [
            255 - (255 - color.r) * (255 - other.r) // 255,
            255 - (255 - color.g) * (255 - other.g) // 255,
            255 - (255 - color.b) * (255 - other.b) // 255,
            color.a
        ]

    @staticmethod
    def difference(
            color: 'Color',
            other: 'Color'
        ) -> list[int]:
        return [
            abs(color.r - other.r),
            abs(color.g - other.g),
            abs(color.b - other.b),
            color.a
        ]

    @staticmethod
    def invert(
            color: 'Color'
        ) -> list[int]:
        return [
            255 - color.r,
            255 - color.g,
            255 - color.b,
            color.a
        ]

    @staticmethod
    def alpha(
            color: 'Color',
            background: 'Color'
        ) -> list[int]:
        alpha = color.a

        return [
            (color.r * alpha + background.r * (255 - alpha)) // 255,
            (color.g * alpha + background.g * (255 - alpha)) // 255,
            (color.b * alpha + background.b * (255 - alpha)) // 255,
            255
        ]
