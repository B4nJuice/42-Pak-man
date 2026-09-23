import os
import re
from datetime import UTC, datetime

from pydantic import ValidationError

from .color import TColor


class Logger:
    '''Lightweight logger for console output.

    Attributes:
        print_log (bool): Whether logging is enabled.
        name (str): Name displayed in log messages.
        color (TColor): TColor used for the name tag.
    '''

    verbose: bool
    name: str
    color: TColor

    def __init__(
        self,
        name: str = 'Logger',
        color: TColor = TColor.GRAY,
        verbose: bool = False,
    ) -> None:
        '''Initialize a logger instance.

        Args:
            verbose: Whether to enable logging output. Defaults to False.
            name: Display name for log messages. Defaults to 'Logger'.
            color: ANSI color for the name tag. Defaults to TColor.GRAY.
        '''
        self.verbose = verbose
        self.name = name
        self.color = color

    def log_format(self, message: str) -> str:
        '''Return a formatted log message string.

        Args:
            message (str): The main content of the log message.
            end (str | None): End character appended to the message.

        Returns:
            str: Formatted log message with prefix and color.
        '''
        return f'{self._get_format()} {message}'

    def log(self, message: str, end: str | None = '\n') -> None:
        '''Print a debug/info message when logging is enabled.

        Args:
            message (str): Message to print.
            end (str | None): End character appended to the message.
        '''
        if self.verbose:
            print(self.log_format(message), end=end)

    def error(self, message: str, end: str | None = '\n') -> None:
        '''Print an error message (always shown).

        Args:
            message (str): Error message to print.
            end (str | None): End character appended to the message.
        '''
        print(
            f'{self._get_format()} {TColor.RED}[ERROR]{TColor.RESET} {message}',
            end=end
        )

    def warning(self, message: str, end: str | None = '\n') -> None:
        '''Print a warning message (always shown).

        Args:
            message (str): Warning message to print.
            end (str | None): End character appended to the message.
        '''
        print(
            f'{self._get_format()} {TColor.YELLOW}[WARNING]{TColor.RESET} '
            f'{message}',
            end=end,
        )

    @staticmethod
    def warning_static(
        name: str,
        message: str,
        color: TColor = TColor.WHITE,
        end: str | None = '\n',
    ) -> None:
        '''Print a warning message from a static context (always shown).

        Args:
            name (str): Name to include in the log prefix.
            message (str): Warning message to print.
            color (TColor): TColor to use for the name tag in the log prefix.
            end (str | None): End character appended to the message.
        '''
        print(
            f'{Logger.get_format_static(color, name)} {TColor.YELLOW}[WARNING]'
            f'{TColor.RESET} {message}',
            end=end,
        )

    def info(self, message: str, end: str | None = '\n') -> None:
        '''Print an informational message (always shown).

        Args:
            message (str): Message to print.
            end (str | None): End character appended to the message.
        '''
        print(
            f'{self._get_format()} [{TColor.BRIGHT_CYAN}INFO{TColor.RESET}] '
            f'{message}',
            end=end,
        )

    def _get_format(self) -> str:
        '''Return the formatted prefix used for all log lines.

        Returns:
            str: Formatted prefix including time and colored name tag.
        '''
        return self.get_format_static(self.color, self.name)

    @staticmethod
    def get_format_static(color: TColor, name: str) -> str:
        '''Return the formatted prefix for static contexts.

        Args:
            name (str): Name to include in the prefix.
        Returns:
            str: Formatted prefix including time and colored name tag.
        '''
        return (
            f'{TColor.GRAY}[{Logger.get_date_time()}] {color}[' +
            f'{name}]{TColor.RESET}'
        )

    @staticmethod
    def get_date_time() -> str:
        '''Return the current time string used in the log prefix.

        Returns:
            str: Formatted time string (HH:MM:SS).
        '''
        now = datetime.now(UTC).astimezone()
        return now.strftime('%X')

    def pydantic_error(self, e: ValidationError, message: str = '') -> None:
        '''Print detailed error messages from a Pydantic ValidationError.

        Args:
            e (ValidationError): The ValidationError instance to process.
            message (str): Optional custom message to display before error
            details.
        '''
        if message:
            self.error(message)

        for error in e.errors():
            loc: tuple[int | str, ...] = error.get('loc') or ('',)
            field = str(loc[0]) if loc else ''
            ctx = error.get('ctx') or {}

            if ctx_error := ctx.get('error'):
                self.error(f'Error: {ctx_error}')
            elif msg := error.get('msg'):
                if field:
                    self.error(f'Error: {field}: {msg}')
                else:
                    self.error(f'Error: {msg}')

    def pydantic_warning(
        self, e: ValidationError, message: str = '', prefix: str = ''
    ) -> None:
        '''Print detailed error messages from a Pydantic ValidationError.

        Args:
            e (ValidationError): The ValidationError instance to process.
            message (str): Optional custom message to display before error
            details.
        '''
        if message:
            self.warning(message)

        for error in e.errors():
            loc: tuple[int | str, ...] = error.get('loc') or ('',)
            field = str(loc[0]) if loc else ''
            ctx = error.get('ctx') or {}

            if ctx_error := ctx.get('error'):
                self.warning(f'Error: {ctx_error}')
            elif msg := error.get('msg'):
                if field:
                    self.warning(
                        f'{prefix + ' ' if prefix else ''}{field}: {msg}'
                    )
                else:
                    self.warning(f'{prefix + ' ' if prefix else ''}{msg}')

    def _generate_box(
        self,
        content: list[str],
        title: str,
        width: int | None = None,
        max_width: int | None = None,
    ) -> list[str]:
        '''Generate a box around the given content.

        Args:
            content (str): The content to place inside the box.
            width (int): The total width of the box.
            title (str): The title to display in the top border of the box.

        Returns:
            list[str]: A list of strings representing the lines of the box.
        '''
        cleaned_content: list[str] = [
            part for item in content for part in item.split('\n')
        ]

        splited_content: list[str]
        if not max_width:
            splited_content = cleaned_content
        else:
            splited_content = self._max_width(cleaned_content, max_width)

        if width is None:
            width = max(len(line) for line in splited_content) + 4
        width = max(width, len(title) + 4)

        result: list[str] = []
        title_line = f'┌─ {title} ' + f'{'─' * (width - len(title) - 3)}┐'
        result.append(title_line)

        for line in splited_content:
            line_len: int = len(self._strip_ansi(line))
            result.append(f'│ {line} ' + f'{' ' * (width - line_len - 2)}│')
        result.append(f'└{'─' * width}┘')
        return result

    def box_info(
        self,
        content: list[str],
        title: str,
        width: int | None = None,
        max_width: int | None = (os.get_terminal_size().columns - 39),
    ) -> None:
        '''Print a box with the given content and title.

        Args:
            content (str): The content to place inside the box.
            width (int): The total width of the box.
            title (str): The title to display in the top border of the box.
        '''
        box_lines = self._generate_box(content, title, width, max_width)
        for line in box_lines:
            self.info(line)

    def _strip_ansi(self, text: str) -> str:
        '''Remove ANSI escape codes for accurate length measurement.'''
        return re.sub(r'\x1b\[[0-9;]*m', '', text)

    def _max_width(self, texts: list[str], width: int) -> list[str]:
        return [
            chunk
            for s in texts
            for chunk in (
                [s]
                if len(s) <= width
                else [s[i: i + width] for i in range(0, len(s), width)]
            )
        ]

    def _generate_table(
        self,
        headers: list[str],
        rows: list[list[str]],
        column_widths: list[int] | None = None,
        prefix: str = ' ',
    ) -> list[str]:
        '''Generate a borderless table with the given headers and rows.
        Args:
            headers (list[str]): The list of column headers.
            rows (list[list[str]]): The list of rows, where each row is a list
            of cell values.
            column_widths (list[int] | None): Optional list of column widths.
            If not provided, widths will be calculated based on content.
            prefix (str): String to prefix each line of the table with.
        Returns:
            list[str]: A list of strings representing the lines of the table.
        '''
        if not headers:
            return []

        if column_widths is None:
            column_widths = [len(self._strip_ansi(h)) for h in headers]
            for row in rows:
                for i, cell in enumerate(row):
                    if i < len(column_widths):
                        column_widths[i] = max(
                            column_widths[i], len(self._strip_ansi(str(cell)))
                        )

        lines: list[str] = []

        def format_row(cells: list[str]) -> str:
            padded = []
            for i, cell in enumerate(cells):
                cell_str = str(cell)
                visible_len = len(self._strip_ansi(cell_str))
                padding = ' ' * (column_widths[i] - visible_len)
                padded.append(cell_str + padding)
            return '  '.join(padded).rstrip()

        lines.append(prefix + format_row(headers))

        separator = '  '.join('─' * w for w in column_widths)
        lines.append(prefix + separator.rstrip())

        for row in rows:
            lines.append(prefix + format_row(row))

        return lines

    def table_info(
        self,
        headers: list[str],
        rows: list[list[str]],
        column_widths: list[int] | None = None,
    ) -> None:
        '''Print a table with the given headers and rows.

        Args:
            headers (list[str]): The list of column headers.
            rows (list[list[str]]): The list of rows, where each row is a list
            of cell values.
            column_widths (list[int] | None): Optional list of column widths.
            If not provided, widths will be calculated based on content.
        '''

        table_lines = self._generate_table(headers, rows, column_widths)
        for line in table_lines:
            self.info(line)

    def table_log(
        self,
        headers: list[str],
        rows: list[list[str]],
        column_widths: list[int] | None = None,
    ) -> None:
        '''Print a table with the given headers and rows.

        Args:
            headers (list[str]): The list of column headers.
            rows (list[list[str]]): The list of rows, where each row is a list
            of cell values.
            column_widths (list[int] | None): Optional list of column widths.
            If not provided, widths will be calculated based on content.
        '''

        table_lines = self._generate_table(headers, rows, column_widths)
        for line in table_lines:
            self.log(line)
