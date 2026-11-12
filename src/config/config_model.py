from typing import Self

from pydantic import BaseModel, Field, model_validator

from src.config.level_model import LevelModel


class ConfigModel(BaseModel):
    highscore_path: str = Field(
        default='.pak-man/highscore.json',
        description='Path to the highscore file'
    )
    levels: list[LevelModel] = Field(
        default=[
            LevelModel(
                name=f'level {index + 1}',
                level_width=size,
                level_height=size,
                max_time=90
            )
            for index, size in enumerate(
                [12, 13, 14, 15, 16, 17, 18, 19, 20, 21]
            )
        ],
        min_length=1,
        description='Ordered list of the levels of a run'
    )

    max_player_ameliorations: int = Field(
        default=3,
        description='Maximum different amelioration a player can have.'
    )

    resolution: tuple[int, int] = Field(
        default=(1920, 1080),
        description='Current display resolution in 16:9 aspect ratio.'
    )

    @property
    def screen_width(self) -> int:
        """
        Handle screen width retrieval.

        Returns:
            The value produced by the screen width retrieval operation.
        """
        return self.resolution[0]

    @property
    def screen_height(self) -> int:
        """
        Handle screen height retrieval.

        Returns:
            The value produced by the screen height retrieval operation.
        """
        return self.resolution[1]

    @model_validator(mode='after')
    def check_screen_ratio(self) -> Self:
        if self.screen_width * 9 != self.screen_height * 16:
            raise ValueError(
                'Screen dimensions must be in 16:9 aspect ratio.'
            )

        if self.screen_width < 640 or self.screen_height < 360:
            raise ValueError(
                'Resolution must be at least 640x360.'
            )
            return self
        return self

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

    # cheat menu
    cheat_overlay_color: tuple[int, int, int] = Field(
        default=(0, 0, 0),
        description=''
    )
    cheat_background_color: tuple[int, int, int] = Field(
        default=(13, 16, 48),
        description=''
    )
    cheat_border_color: tuple[int, int, int] = Field(
        default=(53, 64, 95),
        description=''
    )
    cheat_text_color: tuple[int, int, int] = Field(
        default=(248, 245, 233),
        description=''
    )
    cheat_button_background_color: tuple[int, int, int] = Field(
        default=(32, 40, 61),
        description=''
    )
    cheat_button_border_color: tuple[int, int, int] = Field(
        default=(53, 64, 95),
        description=''
    )
    cheat_button_text_color: tuple[int, int, int] = Field(
        default=(248, 245, 233),
        description=''
    )
    cheat_toggle_bg_inactive_color: tuple[int, int, int] = Field(
        default=(16, 22, 43),
        description=''
    )
    cheat_toggle_bg_active_color: tuple[int, int, int] = Field(
        default=(30, 30, 47),
        description=''
    )
    cheat_toggle_button_inactive_color: tuple[int, int, int] = Field(
        default=(32, 40, 61),
        description=''
    )
    cheat_toggle_button_active_color: tuple[int, int, int] = Field(
        default=(251, 218, 30),
        description=''
    )
    cheat_toggle_button_border_inactive_color: tuple[int, int, int] = Field(
        default=(53, 64, 95),
        description=''
    )
    cheat_toggle_button_border_active_color: tuple[int, int, int] = Field(
        default=(251, 218, 30),
        description=''
    )
    cheat_toggle_border_color: tuple[int, int, int] = Field(
        default=(32, 40, 61),
        description=''
    )
    cheat_toggle_text_inactive_color: tuple[int, int, int] = Field(
        default=(162, 172, 201),
        description=''
    )
    cheat_toggle_text_active_color: tuple[int, int, int] = Field(
        default=(13, 16, 38),
        description=''
    )
    cheat_toggle_text_color: tuple[int, int, int] = Field(
        default=(248, 245, 233),
        description=''
    )
    cheat_toggle_text_secondary_color: tuple[int, int, int] = Field(
        default=(162, 172, 201),
        description=''
    )
    cheat_button_label_background_color: tuple[int, int, int] = Field(
        default=(16, 22, 43),
        description=''
    )
    cheat_button_label_border_color: tuple[int, int, int] = Field(
        default=(53, 64, 95),
        description=''
    )
    cheat_button_label_text_color: tuple[int, int, int] = Field(
        default=(248, 245, 233),
        description=''
    )
    cheat_button_label_text_secondary_color: tuple[int, int, int] = Field(
        default=(162, 172, 201),
        description=''
    )
    cheat_button_action_background_color: tuple[int, int, int] = Field(
        default=(32, 40, 61),
        description=''
    )
    cheat_button_action_border_color: tuple[int, int, int] = Field(
        default=(53, 64, 95),
        description=''
    )
    cheat_button_action_text_color: tuple[int, int, int] = Field(
        default=(248, 245, 233),
        description=''
    )

    # Lobby menu
    lobby_text_accent: tuple[int, int, int] = Field(
        default=(251, 218, 30),
        description=''
    )
    lobby_text_primary: tuple[int, int, int] = Field(
        default=(248, 245, 233),
        description=''
    )
    lobby_text_secondary: tuple[int, int, int] = Field(
        default=(162, 172, 201),
        description=''
    )
    lobby_button_bg: tuple[int, int, int] = Field(
        default=(32, 40, 61),
        description=''
    )
    lobby_button_bg_accent: tuple[int, int, int] = Field(
        default=(251, 218, 30),
        description=''
    )
    lobby_button_text: tuple[int, int, int] = Field(
        default=(248, 245, 233),
        description=''
    )
    lobby_button_text_accent: tuple[int, int, int] = Field(
        default=(13, 16, 38),
        description=''
    )
    lobby_button_border: tuple[int, int, int] = Field(
        default=(53, 64, 95),
        description=''
    )
    lobby_button_border_accent: tuple[int, int, int] = Field(
        default=(251, 218, 30),
        description=''
    )

    # victory meunus
    victory_bg: tuple[int, int, int] = Field(
        default=(13, 16, 48),
        description=''
    )
    victory_bg_accent2: tuple[int, int, int] = Field(
        default=(8, 12, 32),
        description=''
    )
    victory_bg_accent: tuple[int, int, int] = Field(
        default=(30, 30, 47),
        description=''
    )
    victory_bg_secondary: tuple[int, int, int] = Field(
        default=(32, 40, 61),
        description=''
    )
    victory_border: tuple[int, int, int] = Field(
        default=(53, 64, 95),
        description=''
    )
    victory_border_accent: tuple[int, int, int] = Field(
        default=(233, 190, 47),
        description=''
    )
    victory_border_secondary: tuple[int, int, int] = Field(
        default=(53, 64, 95),
        description=''
    )
    victory_text: tuple[int, int, int] = Field(
        default=(248, 245, 233),
        description=''
    )
    victory_text_accent: tuple[int, int, int] = Field(
        default=(251, 218, 30),
        description=''
    )
    victory_text_secondary: tuple[int, int, int] = Field(
        default=(162, 172, 201),
        description=''
    )

    # gameover meunus
    gameover_bg: tuple[int, int, int] = Field(
        default=(13, 16, 48),
        description=''
    )
    gameover_bg_accent: tuple[int, int, int] = Field(
        default=(30, 30, 47),
        description=''
    )
    gameover_bg_secondary: tuple[int, int, int] = Field(
        default=(32, 40, 61),
        description=''
    )
    gameover_border: tuple[int, int, int] = Field(
        default=(53, 64, 95),
        description=''
    )
    gameover_border_accent: tuple[int, int, int] = Field(
        default=(233, 190, 47),
        description=''
    )
    gameover_border_secondary: tuple[int, int, int] = Field(
        default=(53, 64, 95),
        description=''
    )
    gameover_text: tuple[int, int, int] = Field(
        default=(248, 245, 233),
        description=''
    )
    gameover_text_accent: tuple[int, int, int] = Field(
        default=(251, 218, 30),
        description=''
    )
    gameover_text_accent2: tuple[int, int, int] = Field(
        default=(255, 183, 255),
        description=''
    )
    gameover_text_secondary: tuple[int, int, int] = Field(
        default=(162, 172, 201),
        description=''
    )

    # how to play
    how_to_play_bg: tuple[int, int, int] = Field(
        default=(13, 16, 48),
        description=''
    )
    how_to_play_text: tuple[int, int, int] = Field(
        default=(248, 245, 233),
        description=''
    )
    how_to_play_text_accent: tuple[int, int, int] = Field(
        default=(251, 218, 30),
        description=''
    )
    how_to_play_text_secondary: tuple[int, int, int] = Field(
        default=(162, 172, 201),
        description=''
    )
    how_to_play_border: tuple[int, int, int] = Field(
        default=(53, 64, 95),
        description=''
    )
    how_to_play_button_bg: tuple[int, int, int] = Field(
        default=(251, 218, 30),
        description=''
    )
    how_to_play_button_text: tuple[int, int, int] = Field(
        default=(13, 16, 38),
        description=''
    )

    # leaderboard
    leaderboard_bg: tuple[int, int, int] = Field(
        default=(13, 16, 48),
        description=''
    )
    leaderboard_bg_secondary: tuple[int, int, int] = Field(
        default=(32, 40, 61),
        description=''
    )
    leaderboard_bg_accent: tuple[int, int, int] = Field(
        default=(30, 30, 37),
        description=''
    )
    leaderboard_text: tuple[int, int, int] = Field(
        default=(248, 245, 233),
        description=''
    )
    leaderboard_text_accent: tuple[int, int, int] = Field(
        default=(251, 218, 30),
        description=''
    )
    leaderboard_text_accent2: tuple[int, int, int] = Field(
        default=(230, 89, 178),
        description=''
    )
    leaderboard_text_secondary: tuple[int, int, int] = Field(
        default=(162, 172, 201),
        description=''
    )
    leaderboard_border: tuple[int, int, int] = Field(
        default=(53, 64, 95),
        description=''
    )
    leaderboard_border_accent: tuple[int, int, int] = Field(
        default=(251, 218, 30),
        description=''
    )

    # Settings
    settings_bg: tuple[int, int, int] = Field(
        default=(13, 16, 48),
        description=''
    )
    settings_bg_secondary: tuple[int, int, int] = Field(
        default=(32, 40, 61),
        description=''
    )
    settings_bg_accent: tuple[int, int, int] = Field(
        default=(251, 218, 30),
        description=''
    )
    settings_bg_accent2: tuple[int, int, int] = Field(
        default=(30, 30, 37),
        description=''
    )
    settings_text: tuple[int, int, int] = Field(
        default=(248, 245, 233),
        description=''
    )
    settings_text_accent: tuple[int, int, int] = Field(
        default=(251, 218, 30),
        description=''
    )
    settings_text_accent2: tuple[int, int, int] = Field(
        default=(230, 89, 178),
        description=''
    )
    settings_text_secondary: tuple[int, int, int] = Field(
        default=(162, 172, 201),
        description=''
    )
    settings_border: tuple[int, int, int] = Field(
        default=(53, 64, 95),
        description=''
    )
    settings_border_accent: tuple[int, int, int] = Field(
        default=(251, 218, 30),
        description=''
    )
    settings_button_text_accent: tuple[int, int, int] = Field(
        default=(13, 16, 48),
        description=''
    )

    # Game version
    game_version: tuple[int, int, int] = Field(
        default=(0, 1, 0)
    )

    def get_version(self) -> str:
        """
        Return the current version.

        Returns:
            The current version.
        """
        return f'{self.game_version[0]}.{self.game_version[1]}.'\
            f'{self.game_version[2]}'
