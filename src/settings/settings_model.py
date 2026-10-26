import pygame
from pydantic import BaseModel, Field


class ControlSettingsModel(BaseModel):
    move_up: list[int] = Field(
        default=[pygame.K_w, pygame.K_UP],
        description=''
    )
    move_down: list[int] = Field(
        default=[pygame.K_s, pygame.K_DOWN],
        description=''
    )
    move_left: list[int] = Field(
        default=[pygame.K_a, pygame.K_LEFT],
        description=''
    )
    move_right: list[int] = Field(
        default=[pygame.K_d, pygame.K_RIGHT],
        description=''
    )
    select: list[int] = Field(
        default=[pygame.K_SPACE, pygame.K_KP_ENTER, pygame.K_RETURN],
        description=''
    )
    back_pause_resume: list[int] = Field(
        default=[pygame.K_ESCAPE],
        description=''
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
