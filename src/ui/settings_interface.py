from collections.abc import Callable, Iterator
from pathlib import Path
from typing import TYPE_CHECKING

import pygame

from src.app import App
from src.errors import PackError
from src.fonts import FontKey
from src.graphics import Color, Mesh, Position
from src.graphics.meshes import Line, Plane
from src.graphics.super_meshes import AlignEnum, Button, Rectangle
from src.graphics.super_meshes.button import ButtonTextConfig
from src.graphics.super_meshes.font_sequence import FontSequence
from src.settings import ActionKey
from src.settings.settings_model import (
    ControlSettingsModel,
    DisplaySettingsModel,
)
from src.texture.texture_keys import TextureKeys

if TYPE_CHECKING:
    from src.game.game import Game

from src.core.displayable import SimpleDisplayable
from src.graphics.mesh_layer import MeshLayer
from src.ui.interface import Interface


class SettingsInterface(Interface):
    app: App
    game: 'Game'
    layer: MeshLayer

    _bindings: dict[str, list[int]]
    _capture_action: ActionKey | None
    _capture_slot: int | None
    _control_buttons: list[Button]
    _pending_pack_path: Path

    def __init__(self, game: 'Game') -> None:
        super().__init__(game)
        self.game = game
        self.app = game._app
        self.layer = MeshLayer()
        self._bindings = {}
        self._capture_action = None
        self._capture_slot = None
        self._control_buttons = []

        screen_width = self.game._screen.width
        screen_height = self.game._screen.height
        config = self.game._config
        size = self.game._app.size
        fonts = self.game._app.fonts

        self.layer.meshes.append(SimpleDisplayable(
            app=game._app,
            texture_key=TextureKeys.MAIN_BACKDROP.str(),
            position=Position(screen_width // 2, screen_height // 2),
            width=screen_width,
            height=screen_height
        ))

        align_left: float = size.get(120)

        def _settings_texts() -> Iterator[FontSequence]:
            def make(
                        text: str,
                        font_key: FontKey,
                        color: tuple[int, int, int],
                        y_offset: float,
                        x_offset: float = 0.0
                    ) -> FontSequence:
                return FontSequence(
                    text=text,
                    font=fonts.get(font_key),
                    color=Color(*color),
                    position=Position(
                        screen_width / 2,
                        size.get(y_offset),
                    ),
                )

            yield make(
                'PAK-MAN / OPTIONS',
                FontKey.TITLE_SECONDARY_9,
                config.settings_text_secondary,
                44 + 9
            )
            yield make(
                'SETTINGS',
                FontKey.TITLE_42,
                config.settings_text_accent,
                70 + 40
            )
            yield make(
                'Your maze. Your rules. Fine-tune your next run.',
                FontKey.TEXT_13,
                config.settings_text_secondary,
                128 + 15
            )

        self.layer.meshes.extend(_settings_texts())

        def _settings_box() -> Iterator[tuple[Mesh, ...]]:
            def make(
                    x: float,
                    y: float,
                    w: float,
                    h: float,
                    title: str,
                    categorie: str
            ) -> tuple[Mesh, ...]:
                x = size.get(x)
                y = size.get(y)
                w = size.get(w)
                h = size.get(h)
                return (
                    Plane(
                        color=Color(*config.settings_bg),
                        positions=(
                            Position(
                                x,
                                y
                            ),
                            Position(
                                x + w,
                                y + h
                            )
                        )
                    ),
                    Rectangle(
                        color=Color(*config.settings_border),
                        position=Position(
                            x,
                            y
                        ),
                        width=w,
                        height=h,
                        thickness=size.get(1),
                    ),
                    FontSequence(
                        text=title,
                        font=fonts.get(FontKey.TITLE_20),
                        color=Color(*config.settings_text),
                        position=Position(
                            x + size.get(20),
                            y + size.get(40)
                        ),
                        align=AlignEnum.LEFT
                    ),
                    FontSequence(
                        text=categorie,
                        font=fonts.get(FontKey.TITLE_SECONDARY_8),
                        color=Color(*config.settings_text_secondary),
                        position=Position(
                            x + w - size.get(20),
                            y + size.get(36)
                        ),
                        align=AlignEnum.RIGHT
                    ),
                    Line(
                        color=Color(*config.settings_border),
                        start_position=Position(
                            x + size.get(20),
                            y + size.get(56)
                        ),
                        end_position=Position(
                            x + size.get(468 + 20),
                            y + size.get(56)
                        ),
                        thickness=size.get(1)
                    )
                )

            yield make(
                x=120,
                y=168,
                w=508,
                h=416,
                title='DISPLAY',
                categorie='VIDEO'
            )

            yield make(
                x=652,
                y=168,
                w=508,
                h=416,
                title='CONTROLS',
                categorie='KEYBOARD'
            )

        for meshs in _settings_box():
            self.layer.meshes.extend(meshs)

        display_x: int = size.get(140)
        display_y: int = size.get(237)
        display_button_x: int = size.get(420)
        display_button_w: int = size.get(188)
        display_button_h: int = size.get(30)
        display_gap: int = size.get(8)

        def _display_settings() -> Iterator[tuple[Mesh, ...]]:
            display_settings = self.app.settings.get().display
            resolution_values = (
                DisplaySettingsModel.standard_16_9_resolutions()
            )
            resolution_labels = [
                DisplaySettingsModel.resolution_label(resolution)
                for resolution in resolution_values
            ]

            def make(
                idx: int,
                description: str,
                values: list[str],
                current_id: int,
                cb: Callable[[int], None]
            ) -> tuple[Mesh, ...]:
                _status: dict[int, int] = {idx: current_id}

                value: FontSequence = FontSequence(
                    text=values[current_id],
                    font=fonts.get(FontKey.TITLE_SECONDARY_9),
                    color=Color(*config.settings_text),
                    position=Position(
                        display_button_x + display_button_w / 2,
                        display_y
                        + size.get(13 + 7)
                        + (display_button_h + display_gap) * idx,
                    ),
                )

                def _next() -> None:
                    _status[idx] = (_status[idx] + 1) % len(values)
                    value.set_sequence_text(values[_status[idx]])
                    cb(_status[idx])

                def _prev() -> None:
                    _status[idx] = (_status[idx] - 1) % len(values)
                    value.set_sequence_text(values[_status[idx]])
                    cb(_status[idx])

                return (
                    FontSequence(
                        text=description,
                        font=fonts.get(FontKey.TEXT_14),
                        color=Color(*config.settings_text),
                        position=Position(
                            display_x,
                            display_y
                            + size.get(13 + 5)
                            + (display_button_h + display_gap) * idx,
                        ),
                        align=AlignEnum.LEFT
                    ),
                    Button(
                        position=Position(
                            display_button_x,
                            display_y + (display_button_h + display_gap) * idx
                        ),
                        width=display_button_w,
                        height=display_button_h,
                        normal_color=Color(*config.settings_bg_secondary),
                        border_color=Color(*config.settings_border),
                        border_thickness=size.get(1),
                    ),
                    Button(
                        position=Position(
                            display_button_x + size.get(1),
                            display_y + (display_button_h + display_gap) * idx
                            + size.get(1)
                        ),
                        width=display_button_h - size.get(2),
                        height=display_button_h - size.get(2),
                        normal_color=Color(*config.settings_bg_secondary),
                        on_click=_prev,
                        texts=[
                            ButtonTextConfig(
                                text='<',
                                font=fonts.get(FontKey.TITLE_SECONDARY_9),
                                color=Color(*config.settings_text_secondary),
                                offset_y=size.get(5),
                            )
                        ]
                    ),
                    Button(
                        position=Position(
                            display_button_x + size.get(1) + display_button_w
                            - display_button_h,
                            display_y + (display_button_h + display_gap) * idx
                            + size.get(1)
                        ),
                        width=display_button_h - size.get(2),
                        height=display_button_h - size.get(2),
                        normal_color=Color(*config.settings_bg_secondary),
                        on_click=_next,
                        texts=[
                            ButtonTextConfig(
                                text='>',
                                font=fonts.get(FontKey.TITLE_SECONDARY_9),
                                color=Color(*config.settings_text_secondary),
                                offset_y=size.get(5),
                            )
                        ]
                    ),
                    value
                )

            yield make(
                0,
                'Window mode',
                ['WINDOWED', 'FULLSCREEN'],
                int(display_settings.full_screen),
                lambda value_id: setattr(
                    self.app.settings.get().display,
                    'full_screen',
                    bool(value_id)
                )
            )
            yield make(
                1,
                'Resolution',
                resolution_labels,
                next(
                    (
                        idx
                        for idx, resolution in enumerate(resolution_values)
                        if resolution == display_settings.resolution
                    ),
                    0,
                ),
                lambda value_id: setattr(
                    self.app.settings.get().display,
                    'resolution',
                    resolution_values[value_id]
                )
            )

            default_path, pack_paths = (
                self.app.texture.get_available_pack_paths()
            )
            pack_paths.insert(0, default_path)
            pack_labels = [
                'DEFAULT' if path == pack_paths[0] else path.name.upper()
                for path in pack_paths
            ]
            current_pack = self.app.texture.get_pack().root
            current_pack_id = next(
                (
                    idx
                    for idx, path in enumerate(pack_paths)
                    if path == current_pack
                ),
                0,
            )
            self._pending_pack_path = pack_paths[current_pack_id]

            def _load_pack(pack_id: int) -> None:
                self._pending_pack_path = pack_paths[pack_id]

            yield make(
                2,
                'Texture pack',
                pack_labels,
                current_pack_id,
                _load_pack
            )

        for display_setting in _display_settings():
            self.layer.meshes.extend(display_setting)

        control_x: int = size.get(672)
        control_y: int = size.get(238)
        control_button_x: int = size.get(996)
        control_button_w: int = size.get(68)
        control_button_h: int = size.get(30)
        control_gap: int = size.get(8)
        controls = self.app.settings.get().controls.model_dump()
        self._bindings = controls
        actions: list[ActionKey] = [
            ActionKey.MOVE_UP,
            ActionKey.MOVE_DOWN,
            ActionKey.MOVE_LEFT,
            ActionKey.MOVE_RIGHT,
            ActionKey.SELECT,
            ActionKey.BACK_PAUSE_RESUME,
            ActionKey.REROLL,
        ]

        def _key_label(keys: list[int]) -> str:
            if not keys:
                return '-'
            labels = [
                (
                    pygame.key.name(code).upper()
                    if code != pygame.K_SPACE else 'SPACE'
                )
                for code in keys
            ]
            return ' / '.join(labels)

        def _bind_action(action: ActionKey, slot: int = 0) -> None:
            self._capture_action = action
            self._capture_slot = slot
            self._refresh_control_buttons()

        def _get_action_keys(action: ActionKey) -> list[int]:
            return self.app.key_manager.get_keys(action)

        for idx, action in enumerate(actions):
            key_list = _get_action_keys(action)
            label = ControlSettingsModel.model_fields[
                self._action_to_field_name(action)
            ].description or ''

            self.layer.meshes.append(FontSequence(
                text=label,
                font=fonts.get(FontKey.TEXT_13),
                color=Color(*config.settings_text),
                position=Position(
                    control_x,
                    control_y
                    + size.get(13 + 5)
                    + (control_button_h + control_gap) * idx,
                ),
                align=AlignEnum.LEFT,
            ))

            first_button = Button(
                position=Position(
                    control_button_x,
                    control_y + (control_button_h + control_gap) * idx
                ),
                width=control_button_w,
                height=control_button_h,
                normal_color=Color(*config.settings_bg_secondary),
                selected_color=Color(*config.settings_bg_accent2),
                border_color=Color(*config.settings_border),
                selected_border_color=Color(*config.settings_border_accent),
                border_thickness=size.get(1),
                on_click=(
                    lambda action=action, slot=0: _bind_action(action, slot)
                ),
                texts=[
                    ButtonTextConfig(
                        text=_key_label(key_list[:1]),
                        font=fonts.get(FontKey.TITLE_SECONDARY_8),
                        color=Color(*config.settings_text),
                        offset_y=size.get(5),
                    )
                ]
            )
            self.layer.meshes.append(first_button)
            self._control_buttons.append(first_button)

            second_button = Button(
                position=Position(
                    control_button_x + control_button_w + control_gap,
                    control_y + (control_button_h + control_gap) * idx
                ),
                width=control_button_w,
                height=control_button_h,
                normal_color=Color(*config.settings_bg_secondary),
                selected_color=Color(*config.settings_bg_accent2),
                border_color=Color(*config.settings_border),
                selected_border_color=Color(*config.settings_border_accent),
                border_thickness=size.get(1),
                on_click=(
                    lambda action=action, slot=1: _bind_action(action, slot)
                ),
                texts=[
                    ButtonTextConfig(
                        text=_key_label(key_list[1:2]),
                        font=fonts.get(FontKey.TITLE_SECONDARY_8),
                        color=Color(*config.settings_text),
                        offset_y=size.get(5),
                    )
                ]
            )
            self.layer.meshes.append(second_button)
            self._control_buttons.append(second_button)

        def _settings_buttons() -> Iterator[Button]:
            def make(
                        w: float,
                        h: float,
                        x: float,
                        y: float,
                        cb: Callable,
                        txt: str,
                        key: str = '',
                        bg_color: tuple[int, int, int] =
                        config.settings_bg_secondary,
                        border_color: tuple[int, int, int] =
                        config.settings_border,
                        txt_color: tuple[int, int, int] =
                        config.settings_text,
                        key_color: tuple[int, int, int] =
                        config.settings_text_secondary

                    ) -> Button:
                return Button(
                    position=Position(
                        x,
                        y
                    ),
                    width=size.get(w),
                    height=size.get(h),
                    normal_color=Color(*bg_color),
                    hover_color=Color(*bg_color),
                    border_color=Color(*border_color),
                    border_thickness=size.get(1),
                    on_click=cb,
                    texts=[
                        ButtonTextConfig(
                            text=txt,
                            font=fonts.get(FontKey.TITLE_18),
                            color=Color(*txt_color),
                            alignment=AlignEnum.LEFT,
                            offset_y=size.get(6),
                            offset_x=size.get((-w / 2) + 18),
                        ),
                        ButtonTextConfig(
                            text=key,
                            font=fonts.get(FontKey.TITLE_SECONDARY_9),
                            color=Color(*key_color),
                            alignment=AlignEnum.RIGHT,
                            offset_x=size.get((w / 2) - 18),
                            offset_y=size.get(5),
                        )
                    ]
                )

            yield make(
                w=180,
                h=52,
                x=align_left,
                y=size.get(608),
                cb=self._exit,
                txt='Back',
                key='ESC'
            )

            yield make(
                w=272,
                h=52,
                x=size.get(312),
                y=size.get(608),
                cb=self._restore_default,
                txt='RESTORE DEFAULT',
                key=''
            )

            yield make(
                w=240,
                h=52,
                x=size.get(920),
                y=size.get(608),
                cb=self._apply,
                txt='> APPLY',
                key='ENTER',
                bg_color=config.settings_bg_accent,
                border_color=config.settings_border_accent,
                txt_color=config.settings_button_text_accent,
                key_color=config.settings_button_text_accent
            )

        self.layer.meshes.extend(_settings_buttons())

        self.layer.meshes.append(FontSequence(
            text='ARROW KEYS  MOVE   /   ENTER  SELECT   /   ESC  BACK',
            font=fonts.get(FontKey.TITLE_SECONDARY_9),
            color=Color(*config.settings_text_secondary),
            position=Position(
                size.get(40),
                size.get(700.5)
            ),
            align=AlignEnum.LEFT
        ))
        self.layer.meshes.append(FontSequence(
            text=f'V. {config.get_version()}',
            font=fonts.get(FontKey.TITLE_SECONDARY_9),
            color=Color(*config.settings_text_secondary),
            position=Position(
                screen_width - size.get(40),
                size.get(700.5)
            ),
            align=AlignEnum.RIGHT
        ))

    def _action_to_field_name(self, action: ActionKey) -> str:
        match action:
            case ActionKey.MOVE_UP:
                return 'move_up'
            case ActionKey.MOVE_DOWN:
                return 'move_down'
            case ActionKey.MOVE_LEFT:
                return 'move_left'
            case ActionKey.MOVE_RIGHT:
                return 'move_right'
            case ActionKey.SELECT:
                return 'select'
            case ActionKey.BACK_PAUSE_RESUME:
                return 'back_pause_resume'
            case ActionKey.REROLL:
                return 'reroll'
            case _:
                raise ValueError(f'Unknown action {action!r}')

    def _refresh_control_buttons(self) -> None:
        actions = [
            ActionKey.MOVE_UP,
            ActionKey.MOVE_DOWN,
            ActionKey.MOVE_LEFT,
            ActionKey.MOVE_RIGHT,
            ActionKey.SELECT,
            ActionKey.BACK_PAUSE_RESUME,
            ActionKey.REROLL,
        ]

        for index, action in enumerate(actions):
            keys = self.app.key_manager.get_keys(action)
            first_button = self._control_buttons[index * 2]
            second_button = self._control_buttons[index * 2 + 1]

            first_button.texts[0].text = self._key_label(keys[:1])
            second_button.texts[0].text = self._key_label(keys[1:2])

            first_button.set_selected(
                self._capture_action == action and self._capture_slot == 0
            )
            second_button.set_selected(
                self._capture_action == action and self._capture_slot == 1
            )

            first_button.refresh()
            second_button.refresh()

    def _key_label(self, keys: list[int]) -> str:
        if not keys:
            return '-'
        labels = [
            (
                pygame.key.name(code).upper()
                if code != pygame.K_SPACE else 'SPACE'
            )
            for code in keys
        ]
        return ' / '.join(labels)

    def handle_key(self, key: int) -> bool:
        if self.hidden:
            return False

        if self._capture_action is not None:
            if key in self.game._app.key_manager.get_keys(
                ActionKey.BACK_PAUSE_RESUME
            ):
                self._capture_action = None
                self._capture_slot = None
                return True

            current_keys = self.app.key_manager.get_keys(self._capture_action)
            if key in current_keys:
                self._capture_action = None
                self._capture_slot = None
                return True

            slot = self._capture_slot if self._capture_slot is not None else 0
            if not current_keys:
                new_keys = [key]
            elif slot == 1:
                if len(current_keys) >= 2:
                    new_keys = [current_keys[0], key]
                else:
                    new_keys = [current_keys[0], key]
            else:
                new_keys = [key]

            self.app.key_manager.set_keys(self._capture_action, new_keys)
            self._capture_action = None
            self._capture_slot = None
            self._refresh_control_buttons()
            return True

        if key in self.game._app.key_manager.get_keys(
                ActionKey.BACK_PAUSE_RESUME
        ):
            self._exit()
            return True
        return False

    def refresh(self) -> None:
        self._refresh_control_buttons()

    def _exit(self) -> None:
        previous_status = self.game._interface_manager.get_previous_status()
        if previous_status is None:
            self.hide()
            return
        self.game.set_status(previous_status)

    def _restore_default(self) -> None:
        self.app.settings.get().controls = ControlSettingsModel()
        self.app.settings.get().display = DisplaySettingsModel()
        self.app.settings.save()
        self._refresh_control_buttons()

    def _apply(self) -> None:
        try:
            user_pack, _ = self.app.texture.get_available_pack_paths()
            if self._pending_pack_path == user_pack:
                if self.app.texture.get_pack().root != self._pending_pack_path:
                    self.game.unload_pack()
            elif self.app.texture.get_pack().root != self._pending_pack_path:
                self.game.load_pack(str(self._pending_pack_path))
        except PackError:
            return

        self.app.settings.save()
        self._exit()

    def get_layer(self) -> MeshLayer:
        return self.layer
