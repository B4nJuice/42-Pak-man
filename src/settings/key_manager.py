from itertools import chain

import pygame

from src.settings.action_key import ActionKey
from src.settings.settings_manager import SettingsManager


class KeyManager:
    _settings: SettingsManager
    _pressed_keys: pygame.key.ScancodeWrapper

    def __init__(self, settings: SettingsManager) -> None:
        self._settings = settings

    def get_keys(self, action: ActionKey | list[ActionKey]) -> list[int]:
        if isinstance(action, ActionKey):
            match action:
                case ActionKey.MOVE_UP:
                    return self._settings.get().controls.move_up
                case ActionKey.MOVE_DOWN:
                    return self._settings.get().controls.move_down
                case ActionKey.MOVE_LEFT:
                    return self._settings.get().controls.move_left
                case ActionKey.MOVE_RIGHT:
                    return self._settings.get().controls.move_right
                case ActionKey.SELECT:
                    return self._settings.get().controls.select
                case ActionKey.BACK_PAUSE_RESUME:
                    return self._settings.get().controls.back_pause_resume
        return list(chain.from_iterable([self.get_keys(_action) for _action in action]))

    def is_pressed(self, action: ActionKey | list[ActionKey]) -> bool:
        if isinstance(action, ActionKey):
            return any(
                self._pressed_keys[key]
                for key in self.get_keys(action)
            )
        return any(self.is_pressed(_action) for _action in action)

    def is_pressed_event(self, action: ActionKey, event: pygame.Event) -> bool:
        return event.key in self.get_keys(action)

    def update(self) -> None:
        self._pressed_keys = pygame.key.get_pressed()

    def add_key(self, action: ActionKey, key: int) -> None:
        self.get_keys(action).append(key)
        self._settings.save()

    def remove_key(self, action: ActionKey, key: int) -> None:
        if key in self.get_keys(action):
            self.get_keys(action).remove(key)
            self._settings.save()

    def set(self, action: ActionKey, key: int) -> None:
        self.get_keys(action).clear()
        self.get_keys(action).append(key)
        self._settings.save()

    def clear(self, action: ActionKey) -> None:
        self.get_keys(action).clear()
        self._settings.save()
