import os
from pathlib import Path
from typing import Any, ClassVar

import json5
from pydantic import ValidationError

from ..utils import Logger, TColor
from .config_model import ConfigModel
from .level_model import LevelModel


class ConfigManager:
    _config_path: Path
    _config: ConfigModel
    _in_comment_block: int
    _logger: Logger

    COMMENTS_LINE: ClassVar[list[str]] = ['#', '//']
    COMMENTS_BLOCK: ClassVar[list[tuple[str, str]]] = [('/*', '*/')]

    def __init__(self, config_path: str, verbose: bool = False) -> None:
        """
        Initialize the instance.

        Args:
            config_path: Config path used by the operation.
            verbose: Whether verbose logging is enabled.
        """
        self._init_logger(verbose)
        self._logger.log('Initializing config manager')

        try:
            self._set_config_path(config_path)
            self._load_config()
        except (FileNotFoundError, PermissionError, ValueError):
            self._logger.warning(
                'Failed to load config, using default settings'
            )
            self._config = ConfigModel()
        self._logger.info('Configuration loaded successfully')

    def get_config(self) -> ConfigModel:
        """
        Return the current config.

        Returns:
            The current config.
        """
        return self._config

    def display_config(self) -> None:
        """
        Handle display config.
        """
        print(self._config.model_dump_json(indent=2))

    def _init_logger(self, verbose: bool) -> None:
        """
        Handle init logger.

        Args:
            verbose: Whether verbose logging is enabled.
        """
        self._logger = Logger(
            verbose=verbose, name='ConfigManager', color=TColor.BRIGHT_BLUE
        )

    def _set_config_path(self, path: str) -> None:
        """
        Handle set config path.

        Args:
            path: Filesystem path used to load or save the data.
        """
        self._config_path = Path(path)
        if not self._config_path.is_file():
            raise FileNotFoundError(
                f'Config file not found: {self._config_path}'
                )
        if not os.access(path, os.R_OK):
            raise PermissionError(
                f'Config file is not readable: {self._config_path}'
            )

    def _init_formater(self) -> None:
        """
        Handle init formater.
        """
        self._in_comment_block = -1

    def _load_config(self) -> None:
        """
        Handle load config.
        """
        self._logger.log(
            f'Loading config from {self._config_path.absolute().as_posix()!r}'
        )
        self._init_formater()

        with self._config_path.open('r') as f:
            lines: list[str] = [self._format_line(line.strip()) for line in f]

        self._logger.log(f'Formatted {len(lines)} lines for JSON parsing')
        raw_data = json5.loads(''.join(lines))

        if not isinstance(raw_data, dict):
            self._logger.warning(
                'Config file is not a dictionary, using default settings'
            )
            self._config = ConfigModel()
            return

        validated_data: dict[str, Any] = {}
        default_instance = ConfigModel()

        for key, value in raw_data.items():
            if key == 'levels':
                levels = self._validate_levels(value)
                if levels:
                    validated_data[key] = levels
                else:
                    self._logger.warning(
                        'No valid level found, falling back to default '
                        'levels'
                    )
                continue
            if key in ConfigModel.model_fields:
                try:
                    test_obj = ConfigModel.model_validate(
                        {**default_instance.model_dump(), key: value}
                    )
                    validated_data[key] = getattr(test_obj, key)
                except ValidationError as e:
                    self._logger.pydantic_warning(
                        e, prefix='Invalid value for'
                    )
                    self._logger.log(
                        f'Falling back to default value for {key} ({value} ->'
                        f' {default_instance.model_dump()[key]})'
                    )
                    continue

        self._config = ConfigModel(**validated_data)

    def _validate_levels(self, value: object) -> list[LevelModel]:
        """
        Validate each level independently.

        Invalid fields of a level fall back to their default value, so one
        faulty value does not discard the whole list of levels.

        Args:
            value: Raw value of the ``levels`` key.

        Returns:
            The list of valid levels (empty if none could be built).
        """
        if not isinstance(value, list):
            self._logger.warning(
                f'Invalid value for levels: expected a list, got '
                f'{type(value).__name__}'
            )
            return []

        levels: list[LevelModel] = []
        default_level = LevelModel().model_dump()
        for index, raw_level in enumerate(value):
            if not isinstance(raw_level, dict):
                self._logger.warning(
                    f'Ignoring level {index}: expected an object'
                )
                continue
            level_data: dict[str, object] = {}
            for key, field_value in raw_level.items():
                if key not in LevelModel.model_fields:
                    continue
                try:
                    LevelModel.model_validate(
                        {**default_level, key: field_value}
                    )
                    level_data[key] = field_value
                except ValidationError as e:
                    self._logger.pydantic_warning(
                        e, prefix=f'Invalid value in level {index} for'
                    )
                    self._logger.log(
                        f'Falling back to default value for {key} '
                        f'({field_value} -> {default_level[key]})'
                    )
            levels.append(LevelModel.model_validate(level_data))
        return levels

    def _format_line(self, line: str) -> str:
        """
        Handle format line.

        Args:
            line: Line used by the operation.

        Returns:
            The value produced by the format line operation.
        """
        formatted_line: list[str] = []
        in_string: bool = False
        escaped: bool = False
        idx: int = 0

        while idx < len(line):
            if self._in_comment_block != -1:
                idx, closed = self._consume_comment_block(
                    line, idx, self._in_comment_block
                )
                if not closed:
                    return ''.join(formatted_line)
                self._in_comment_block = -1
                continue

            if in_string:
                char = line[idx]
                formatted_line.append(char)
                if escaped:
                    escaped = False
                elif char == '\\':
                    escaped = True
                elif char == '"':
                    in_string = False
                idx += 1
                continue

            if line[idx] == '"':
                in_string = True
                formatted_line.append(line[idx])
                idx += 1
                continue

            if self._starts_line_comment(line, idx):
                break

            block_start = self._match_block_comment_start(line, idx)
            if block_start is not None:
                block_idx, start_token, end_token = block_start
                idx += len(start_token)
                end_idx = line.find(end_token, idx)
                if end_idx == -1:
                    self._in_comment_block = block_idx
                    return ''.join(formatted_line)
                idx = end_idx + len(end_token)
                continue

            formatted_line.append(line[idx])
            idx += 1

        return ''.join(formatted_line)

    def _consume_comment_block(
        self, line: str, idx: int, block_idx: int
    ) -> tuple[int, bool]:
        '''Advance past the closing token of an open block comment.

        Returns (new_idx, closed) — closed=False means the line ended
        before the comment closed.
        '''
        end_token = self.COMMENTS_BLOCK[block_idx][1]
        end_idx = line.find(end_token, idx)
        if end_idx == -1:
            return idx, False
        return end_idx + len(end_token), True

    def _starts_line_comment(self, line: str, idx: int) -> bool:
        """
        Handle starts line comment.

        Args:
            line: Line used by the operation.
            idx: Idx used by the operation.

        Returns:
            Whether the operation succeeded or the condition is true.
        """
        return any(line.startswith(c, idx) for c in self.COMMENTS_LINE)

    def _match_block_comment_start(
        self, line: str, idx: int
    ) -> tuple[int, str, str] | None:
        """
        Handle match block comment start.

        Args:
            line: Line used by the operation.
            idx: Idx used by the operation.

        Returns:
            The value produced by the match block comment start operation.
        """
        return next(
            (
                (block_idx, start, end)
                for block_idx, (start, end) in enumerate(self.COMMENTS_BLOCK)
                if line.startswith(start, idx)
            ),
            None,
        )
