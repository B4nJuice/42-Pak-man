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

    background: tuple[int, int, int] = Field(
        default=(13, 16, 38),
        description="Color of the backgound"
    )

    maze_backgroud_color: tuple[int, int, int] = Field(
        default=(13, 16, 38),
        description="Color of the maze tile"
    )

    maze_wall_color: tuple[int, int, int] = Field(
        default=(46, 46, 255),
        description="Color of the maze walls"
    )

    level_bar_color: tuple[int, int, int] = Field(
        default=(251, 218, 30),
        description="Color of the level's progression bar"
    )
    level_bar_border_color: tuple[int, int, int] = Field(
        default=(53, 64, 95),
        description="Color of the border level's progression bar"
    )

    timer_color: tuple[int, int, int] = Field(
        default=(248, 245, 233),
        description="timer font color"
    )

    stats_border_color: tuple[int, int, int] = Field(
        default=(53, 64, 95),
        description="Color of the border of the stats"
    )

    stats_background_color: tuple[int, int, int] = Field(
        default=(13, 16, 48),
        description="Color of the background of the stats"
    )

    stats_text_color: tuple[int, int, int] = Field(
        default=(248, 245, 233),
        description="Color of the text of the stats"
    )

    pause_menu_overlay_color: tuple[int, int, int] = Field(
        default=(0, 0, 0),
        description="Color of the pause menu overlay"
    )
    menu_panel_color: tuple[int, int, int] = Field(
        default=(16, 22, 44),
        description="Color of the pause menu panel"
    )

    pause_menu_background_color: tuple[int, int, int] = Field(
        default=(13, 16, 48),
        description="Color of the pause menu panel"
    )
    pause_menu_border_color: tuple[int, int, int] = Field(
        default=(53, 64, 95),
        description="Color of the pause menu border"
    )
    pause_menu_button_color: tuple[int, int, int] = Field(
        default=(32, 40, 61),
        description="Color of the pause menu buttons"
    )
    pause_menu_button_hover_color: tuple[int, int, int] = Field(
        default=(251, 218, 30),
        description="Color of the pause menu buttons"
    )
    pause_menu_text_primary: tuple[int, int, int] = Field(
        default=(251, 218, 30),
        description="Color of the pause menu text"
    )
    pause_menu_text_secondary: tuple[int, int, int] = Field(
        default=(162, 172, 201),
        description="Color of the pause menu text"
    )
    pause_menu_text_button: tuple[int, int, int] = Field(
        default=(248, 245, 233),
        description="Color of the pause menu text"
    )
    pause_menu_text_button_hover: tuple[int, int, int] = Field(
        default=(13, 16, 38),
        description="Color of the pause menu text"
    )

    amelioration_common_color: tuple[int, int, int] = Field(
        default=(196, 196, 196),
        description="Color of common ameliorations"
    )
    amelioration_uncommon_color: tuple[int, int, int] = Field(
        default=(85, 230, 65),
        description="Color of uncommon ameliorations"
    )
    amelioration_rare_color: tuple[int, int, int] = Field(
        default=(95, 163, 216),
        description="Color of rare ameliorations"
    )
    amelioration_epic_color: tuple[int, int, int] = Field(
        default=(191, 102, 239),
        description="Color of epic ameliorations"
    )
    amelioration_legendary_color: tuple[int, int, int] = Field(
        default=(255, 227, 75),
        description="Color of legendary ameliorations"
    )
    amelioration_mythic_color: tuple[int, int, int] = Field(
        default=(237, 42, 113),
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

    placeholder_amelioration_color: tuple[int, int, int] = Field(
        default=(32, 40, 61),
        description="background placholder color"
    )

    placeholder_amelioration_border_color: tuple[int, int, int] = Field(
        default=(53, 64, 95),
        description="background placholder color"
    )

    skill_interface_background_color: tuple[int, int, int] = Field(
        default=(32, 40, 61),
        description="background skill color"
    )

    skill_interface_border_color: tuple[int, int, int] = Field(
        default=(53, 64, 95),
        description="border skill color"
    )

    skill_interface_title_color: tuple[int, int, int] = Field(
        default=(162, 172, 201),
        description="skill title color"
    )

    skill_interface_value_color: tuple[int, int, int] = Field(
         default=(248, 245, 233),
         description="skill value color"
     )

    lives_text_color: tuple[int, int, int] = Field(
         default=(162, 172, 201),
         description="skill value color"
    )

    lives_number_color: tuple[int, int, int] = Field(
         default=(248, 245, 233),
         description="skill value color"
    )

    lives_bar_border_color: tuple[int, int, int] = Field(
        default=(53, 64, 95),
        description="skill value color"
    )

    lives_bar_fill_color: tuple[int, int, int] = Field(
        default=(230, 89, 178),
        description="skill value color"
    )

    back_level_up_color: tuple[int, int, int] = Field(
        default=(138, 80, 28)
    )

    level_up_color: tuple[int, int, int] = Field(
        default=(255, 227, 75)
    )

    amelioration_card_color: tuple[int, int, int] = Field(
        default=(32, 32, 44)
    )

    amelioration_card_border_color: tuple[int, int, int] = Field(
        default=(53, 64, 95)
    )

    amelioration_name: tuple[int, int, int] = Field(
        default=(248, 245, 233)
    )

    amelioration_description: tuple[int, int, int] = Field(
        default=(162, 172, 201)
    )

    amelioration_effect_background_color: tuple[int, int, int] = Field(
        default=(9, 14, 28)
    )

    choose_button_background_color: tuple[int, int, int] = Field(
        default=(32, 41, 66)
    )

    choose_button_text_color: tuple[int, int, int] = Field(
        default=(246, 246, 246)
    )

    amelioration_rarity_text_color: tuple[int, int, int] = Field(
        default=(196, 196, 196)
    )

    skill_name_color: tuple[int, int, int] = Field(
        default=(162, 172, 201)
    )

    skill_upgrade_color: tuple[int, int, int] = Field(
        default=(248, 245, 233)
    )

    skill_change_color: tuple[int, int, int] = Field(
        default=(101, 114, 147)
    )

    selected_choose_button_color: tuple[int, int, int] = Field(
        default=(31, 31, 31)
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

    # leaderboard
