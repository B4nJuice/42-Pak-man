from abc import abstractmethod
from typing import Any

from src.core.entity import Entity
from src.core.movable import Movable
from src.core.tile import Tile
from src.utils import Direction, Path


class AI:
    _next_moves: list[Direction]
    _tracking_tile: Tile | None
    _elapsed_tracking_update: float
    _tile_has_change: bool
    _invalid_tracking_time: float | None
    _has_arrive: bool

    def __init__(
                self, *args: Any,
                update_tracking_interval: float | None,
                **kwargs: Any
            ) -> None:
        """
        Initialize the instance.

        Args:
            update_tracking_interval: Update tracking interval used by
            the operation.
            args: Command-line arguments passed to the application.
            kwargs: Kwargs used by the operation.
        """
        self._next_moves = []

        self._tracking_tile = None
        self._elapsed_tracking_update = float('inf')
        self._tile_has_change = False
        self._invalid_tracking_time = update_tracking_interval
        self._has_arrive = True

        super().__init__(*args, **kwargs)

    def get_next_move(self) -> Direction:
        """
        Return the current next move.

        Returns:
            The current next move.
        """
        return self._next_moves.pop(0)

    def set_next_moves(self, next_moves: list[Direction]) -> None:
        """
        Assign the next moves.

        Args:
            next_moves: Next moves used by the operation.
        """
        self._next_moves = next_moves

    def add_next_move(self, direction: Direction) -> None:
        """
        Add the next move to the collection.

        Args:
            direction: Direction in which the entity should move.
        """
        if not isinstance(self, Movable):
            return

        self._next_moves.append(direction)

        if self._direction is None:
            self.move_next()

    def apply_path(self, path: Path) -> None:
        """
        Handle apply path.

        Args:
            path: Filesystem path used to load or save the data.
        """
        for _, direction in path:
            self.add_next_move(direction)

    def has_next_move(self) -> bool:
        """
        Check whether the  next move condition holds.

        Returns:
            Whether the operation succeeded or the condition is true.
        """
        return len(self._next_moves) > 0

    def get_next_moves(self) -> list[Direction]:
        """
        Return the current next moves.

        Returns:
            The current next moves.
        """
        return self._next_moves.copy()

    def clear_next_moves(self) -> None:
        """
        Handle clear next moves.
        """
        self._next_moves.clear()

    def move_next(self) -> bool:
        """
        Handle move next.

        Returns:
            Whether the operation succeeded or the condition is true.
        """
        if not isinstance(self, Movable) or not isinstance(self, Entity):
            return False

        if not self.has_next_move():
            if self.get_tile() == self._tracking_tile and not self._has_arrive:
                self._has_arrive = True
                self.on_arrive_ai()
            return False

        self.try_move(self.get_next_move())
        return True

    def on_arrive_ai(self) -> None:
        """
        Handle the arrive ai event.
        """

    def update_ai(self, dt: float) -> None:
        """
        Update the ai.

        Args:
            dt: Elapsed time since the previous update, in seconds.
        """
        if not isinstance(self, Movable) or not isinstance(self, Entity):
            return

        self.set_tracking_tile(self.get_tracking_tile())

        if self.need_to_update(dt):
            self.update_tracking()

        if not self.is_moving():
            self.move_next()

    def update_tracking(self) -> None:
        """
        Update the tracking.
        """
        self._elapsed_tracking_update = 0.0
        self._tile_has_change = False
        self._need_update_tracking = False

    def force_update_tracking(self) -> None:
        """
        Handle force update tracking.
        """
        self.set_tracking_tile(self.get_tracking_tile())
        self.update_tracking()

    def set_tracking_tile(self, tile: Tile) -> None:
        """
        Assign the tracking tile.

        Args:
            tile: Grid tile occupied by or assigned to the entity.
        """
        if self._tracking_tile != tile:
            self._tracking_tile = tile
            self._tile_has_change = True
            self._has_arrive = False

    def need_to_update(self, dt: float) -> bool:
        """
        Handle need to update.

        Args:
            dt: Elapsed time since the previous update, in seconds.

        Returns:
            Whether the operation succeeded or the condition is true.
        """
        self._elapsed_tracking_update += dt

        return self._tile_has_change and \
            (
                self._invalid_tracking_time is None or
                (self._elapsed_tracking_update >= self._invalid_tracking_time
                    and self._invalid_tracking_time >= 0) or
                not self.has_next_move()
            )

    @abstractmethod
    def get_tracking_tile(self) -> Tile:
        """
        Return the current tracking tile.

        Returns:
            The current tracking tile.
        """
