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
            f'{self._get_format()} {TColor.RED}[ERROR]{TColor.RESET} '
            + message,
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
                        f"{prefix + ' ' if prefix else ''}{field}: {msg}"
                    )
                else:
                    self.warning(f"{prefix + ' ' if prefix else ''}{msg}")
