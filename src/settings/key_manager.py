import pygame

from src.settings.action_key import ActionKey
from src.settings.settings_manager import SettingsManager


class KeyManager:
    _settings: SettingsManager
    _pressed_keys: pygame.key.ScancodeWrapper

    def __init__(self, settings: SettingsManager) -> None:
        self._settings = settings

    def get_keys(self, action: ActionKey) -> list[int]:
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

    def is_pressed(self, action: ActionKey) -> bool:
        return any(
            self._pressed_keys[key]
            for key in self.get_keys(action)
        )

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
