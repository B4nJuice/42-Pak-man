import pygame
from pydantic import BaseModel, Field


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
    reroll: list[int] = Field(
        default=[pygame.K_r],
        description='Reroll'
    )


class DisplaySettingsModel(BaseModel):
    full_screen: bool = Field(
        default=False,
        description=''
    )
    resolution: tuple[int, int] = Field(
        default=(1280, 720),
        description=''
    )


class SettingsModel(BaseModel):
    controls: ControlSettingsModel = Field(
        default=ControlSettingsModel(),
        description=''
    )
    display: DisplaySettingsModel = Field(
        default=DisplaySettingsModel(),
        description=''
    )
