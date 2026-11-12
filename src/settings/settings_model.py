from typing import Self

import pygame
from pydantic import BaseModel, Field, model_validator


class ControlSettingsModel(BaseModel):
    move_up: list[int] = Field(
        default=[pygame.K_w, pygame.K_UP],
        description='Move up'
    )
    move_down: list[int] = Field(
        default=[pygame.K_s, pygame.K_DOWN],
        description='Move down'
    )
    move_left: list[int] = Field(
        default=[pygame.K_a, pygame.K_LEFT],
        description='Move left'
    )
    move_right: list[int] = Field(
        default=[pygame.K_d, pygame.K_RIGHT],
        description='Move right'
    )
    select: list[int] = Field(
        default=[pygame.K_SPACE, pygame.K_RETURN],
        description='Select'
    )
    back_pause_resume: list[int] = Field(
        default=[pygame.K_ESCAPE],
        description='Pause / Resume / Back'
    )


class DisplaySettingsModel(BaseModel):
    full_screen: bool = Field(
        default=False,
        description='Whether the game should run in fullscreen mode.'
    )
    resolution: tuple[int, int] = Field(
        default=(1920, 1080),
        description='Current display resolution in 16:9 aspect ratio.'
    )

    def get_screen_width(self) -> int:
        """
        Handle screen width retrieval.

        Returns:
            The value produced by the screen width retrieval operation.
        """
        return self.resolution[0]

    def get_screen_height(self) -> int:
        """
        Handle screen height retrieval.

        Returns:
            The value produced by the screen height retrieval operation.
        """
        return self.resolution[1]

    @model_validator(mode='after')
    def check_resolution(self) -> Self:
        """
        Handle resolution validation.
        """
        if self.get_screen_width() * 9 != self.get_screen_height() * 16:
            raise ValueError(
                'Resolution must be in 16:9 aspect ratio.'
            )
        if self.get_screen_width() < 640 or self.get_screen_height() < 360:
            raise ValueError(
                'Resolution must be at least 640x360.'
            )
        return self

    @staticmethod
    def standard_16_9_resolutions() -> list[tuple[int, int]]:
        """
        Handle standard 16 9 resolutions.

        Returns:
            The value produced by the standard 16 9 resolutions operation.
        """
        widths = [3840, 2560, 1920, 1600, 1366, 1280, 1024, 960, 854, 768, 640]
        return [(width, round(width * 9 / 16)) for width in widths]

    @staticmethod
    def resolution_label(resolution: tuple[int, int]) -> str:
        """
        Handle resolution label.

        Args:
            resolution: Screen resolution represented as width and height.

        Returns:
            The value produced by the resolution label operation.
        """
        width, height = resolution
        return f'{width} × {height}'


class SettingsModel(BaseModel):
    controls: ControlSettingsModel = Field(
        default=ControlSettingsModel(),
        description=''
    )
    display: DisplaySettingsModel = Field(
        default=DisplaySettingsModel(),
        description=''
    )
