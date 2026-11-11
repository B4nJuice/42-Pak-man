from datetime import UTC, datetime


def utc_now() -> datetime:
    """
    Return the current UTC date and time.

    Returns:
        The value produced by the utc now operation.
    """
    return datetime.now(UTC).astimezone()
