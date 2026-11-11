from itertools import chain

import pygame

from src.settings.action_key import ActionKey
from src.settings.settings_manager import SettingsManager


class KeyManager:
    _settings: SettingsManager
    _pressed_keys: pygame.key.ScancodeWrapper

    def __init__(self, settings: SettingsManager) -> None:
        """
        Initialize the instance.

        Args:
            settings: Settings used by the operation.
        """
        self._settings = settings

    def get_keys(self, action: ActionKey | list[ActionKey]) -> list[int]:
        """
        Return the current keys.

        Args:
            action: Action whose key bindings or state are queried.

        Returns:
            The current keys.
        """
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
                case ActionKey.REROLL:
                    return self._settings.get().controls.reroll
        return list(chain.from_iterable(
            [self.get_keys(_action) for _action in action]
        ))

    def is_pressed(self, action: ActionKey | list[ActionKey]) -> bool:
        """
        Check whether the pressed condition holds.

        Args:
            action: Action whose key bindings or state are queried.

        Returns:
            Whether the operation succeeded or the condition is true.
        """
        if isinstance(action, ActionKey):
            return any(
                self._pressed_keys[key]
                for key in self.get_keys(action)
            )
        return any(self.is_pressed(_action) for _action in action)

    def is_pressed_event(self, action: ActionKey, event: pygame.Event) -> bool:
        """
        Check whether the pressed event condition holds.

        Args:
            action: Action whose key bindings or state are queried.
            event: Pygame event being handled.

        Returns:
            Whether the operation succeeded or the condition is true.
        """
        return event.key in self.get_keys(action)

    def update(self) -> None:
        """
        Handle update.
        """
        self._pressed_keys = pygame.key.get_pressed()

    def add_key(self, action: ActionKey, key: int) -> None:
        """
        Add the key to the collection.

        Args:
            action: Action whose key bindings or state are queried.
            key: Keyboard key code associated with the action.
        """
        current = self.get_keys(action)
        if key not in current:
            current.append(key)
            self._settings.save()

    def remove_key(self, action: ActionKey, key: int) -> None:
        """
        Remove the key from the collection.

        Args:
            action: Action whose key bindings or state are queried.
            key: Keyboard key code associated with the action.
        """
        if key in self.get_keys(action):
            self.get_keys(action).remove(key)
            self._settings.save()

    def set(self, action: ActionKey, key: int) -> None:
        """
        Handle set.

        Args:
            action: Action whose key bindings or state are queried.
            key: Keyboard key code associated with the action.
        """
        keys = self.get_keys(action)
        keys.clear()
        keys.append(key)
        self._settings.save()

    def set_keys(self, action: ActionKey, keys: list[int]) -> None:
        """
        Assign the keys.

        Args:
            action: Action whose key bindings or state are queried.
            keys: Keyboard key codes associated with the action.
        """
        for other_action in self._iter_actions():
            if other_action is action:
                continue
            for key in list(self.get_keys(other_action)):
                if key in keys and key in self.get_keys(other_action):
                    self.get_keys(other_action).remove(key)

        target = self.get_keys(action)
        target.clear()
        target.extend(keys)
        self._settings.save()

    def clear(self, action: ActionKey) -> None:
        """
        Handle clear.

        Args:
            action: Action whose key bindings or state are queried.
        """
        self.get_keys(action).clear()
        self._settings.save()

    def _iter_actions(self) -> list[ActionKey]:
        """
        Handle iter actions.

        Returns:
            The value produced by the iter actions operation.
        """
        return [
            ActionKey.MOVE_UP,
            ActionKey.MOVE_DOWN,
            ActionKey.MOVE_LEFT,
            ActionKey.MOVE_RIGHT,
            ActionKey.SELECT,
            ActionKey.BACK_PAUSE_RESUME,
            ActionKey.REROLL,
        ]
