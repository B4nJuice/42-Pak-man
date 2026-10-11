from pydantic import BaseModel, Field


class ConfigModel(BaseModel):
    highscore_path: str = Field(
        default='data/highscores.json',
        description='Path to the highscore file'
    )
    level_width: int = Field(
        default=20,
        description='Width of the level'
    )
    level_height: int = Field(
        default=20,
        description='Height of the level'
    )

    screen_width: int = Field(
        gt=100,
        default=800,
        description='Width of the screen'
    )
    screen_height: int = Field(
        gt=100,
        default=600,
        description='Height of the screen'
    )

    maze_color: tuple[int, int, int] = Field(
        default=(255, 255, 255),
        description="Color of the maze"
    )

    level_bar_color: tuple[int, int, int] = Field(
        default=(255, 180, 45),
        description="Color of the level's progression bar"
    )
    level_bar_border_color: tuple[int, int, int] = Field(
        default=(255, 255, 255),
        description="Color of the border level's progression bar"
    )

    timer_color: tuple[int, int, int] = Field(
        default=(255, 255, 255),
        description="timer font color"
    )

    stats_border_color: tuple[int, int, int] = Field(
        default=(255, 255, 255),
        description="Color of the border of the stats"
    )

    font_path: str = Field(
        default="assets/fonts/Bold Frame.ttf"
    )

    #           Exp params

    # rewards

    pacgum_reward: float = Field(
        default=3
    )
    super_pacgum_reward: float = Field(
        default=30
    )
    ghost_reward: float = Field(
        default=60
    )

    # player

    player_level_exp_multiplier: float = Field(
         default=1.1
     )
    player_first_level_exp: float = Field(
        default=100
    )
    player_exp_per_second: float = Field(
        default=0.5
    )
