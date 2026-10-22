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

    max_player_ameliorations: int = Field(
        default=3,
        description='Maximum different amelioration a player can have.'
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

    menu_overlay_color: tuple[int, int, int] = Field(
        default=(0, 0, 0),
        description="Color of the pause menu overlay"
    )
    menu_panel_color: tuple[int, int, int] = Field(
        default=(20, 20, 20),
        description="Color of the pause menu panel"
    )
    menu_border_color: tuple[int, int, int] = Field(
        default=(255, 255, 255),
        description="Color of the pause menu border"
    )
    menu_button_color: tuple[int, int, int] = Field(
        default=(35, 35, 35),
        description="Color of the pause menu buttons"
    )
    menu_text_color: tuple[int, int, int] = Field(
        default=(255, 255, 255),
        description="Color of the pause menu text"
    )
    amelioration_common_color: tuple[int, int, int] = Field(
        default=(120, 120, 120),
        description="Color of common ameliorations"
    )
    amelioration_uncommon_color: tuple[int, int, int] = Field(
        default=(70, 180, 90),
        description="Color of uncommon ameliorations"
    )
    amelioration_rare_color: tuple[int, int, int] = Field(
        default=(70, 130, 220),
        description="Color of rare ameliorations"
    )
    amelioration_epic_color: tuple[int, int, int] = Field(
        default=(155, 80, 210),
        description="Color of epic ameliorations"
    )
    amelioration_legendary_color: tuple[int, int, int] = Field(
        default=(230, 150, 35),
        description="Color of legendary ameliorations"
    )
    amelioration_mythic_color: tuple[int, int, int] = Field(
        default=(220, 50, 70),
        description="Color of mythic ameliorations"
    )
    amelioration_title_font_size: int = Field(
        default=28,
        gt=0,
        description="Title font size of amelioration buttons"
    )
    amelioration_rarity_font_size: int = Field(
        default=18,
        gt=0,
        description="Rarity font size of amelioration buttons"
    )
    amelioration_skill_font_size: int = Field(
        default=16,
        gt=0,
        description="Skill font size of amelioration buttons"
    )

    placeholder_amelioration_color: tuple[int, int, int, int] = Field(
        default = (255, 255, 255, 50),
        description="background placholder color"
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
