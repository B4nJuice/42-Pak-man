from json.decoder import JSONDecodeError
from .config_model import ConfigModel
from pathlib import Path
import json
import os


class ConfigManager:
    config_path: Path
    _config: ConfigModel
    _in_comment_block: int

    COMMENTS_LINE: list[str] = ['#', '//']
    COMMENTS_BLOCK: list[tuple[str, str]] = [('/*', '*/')]

    def __init__(self, config_path: str) -> None:
        self._set_config_path(config_path)

        try:
            self._load_config()
        except (FileNotFoundError, PermissionError) as e:
            raise RuntimeError(f'Failed to load config: {e}')
        except JSONDecodeError as e:
            raise RuntimeError(f'Failed to parse config: {e}')

    def get_config(self) -> ConfigModel:
        return self._config

    def _set_config_path(self, path: str) -> None:
        self.config_path = Path(path)
        if not self.config_path.is_file():
            raise FileNotFoundError(
                f'Config file not found: {self.config_path}'
            )
        if not os.access(path, os.R_OK):
            raise PermissionError(
                f'Config file is not readable: {self.config_path}'
            )

    def _init_formater(self) -> None:
        self._in_comment_block = -1

    def _load_config(self) -> None:
        self._init_formater()

        with self.config_path.open('r') as f:
            lines: list[str] = [
                self._format_line(line.strip())
                for line in f
            ]

        self._config = ConfigModel.model_validate(
            json.loads(''.join(lines))
        )

    def _format_line(self, line: str) -> str:
        formatted_line: list[str] = []
        in_string: bool = False
        escaped: bool = False
        idx: int = 0

        while idx < len(line):
            if self._in_comment_block != -1:
                idx, closed = self._consume_comment_block(
                    line,
                    idx,
                    self._in_comment_block
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
                self,
                line: str,
                idx: int,
                block_idx: int
            ) -> tuple[int, bool]:
        """Advance past the closing token of an open block comment.

        Returns (new_idx, closed) — closed=False means the line ended
        before the comment closed.
        """
        end_token = self.COMMENTS_BLOCK[block_idx][1]
        end_idx = line.find(end_token, idx)
        if end_idx == -1:
            return idx, False
        return end_idx + len(end_token), True

    def _starts_line_comment(self, line: str, idx: int) -> bool:
        return any(line.startswith(c, idx) for c in self.COMMENTS_LINE)

    def _match_block_comment_start(
                self,
                line: str,
                idx: int
            ) -> tuple[int, str, str] | None:
        return next(
            (
                (block_idx, start, end)
                for block_idx, (start, end) in enumerate(self.COMMENTS_BLOCK)
                if line.startswith(start, idx)
            ),
            None,
        )
