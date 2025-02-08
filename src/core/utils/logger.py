from logging import Logger

from kestra import Kestra


def get_logger() -> Logger:
    """
    Get a logger instance from Kestra. The Logger instance from Kestra utilizes the
    specialized format that Kestra needs in order to parse and read logs.

    Returns:
        Logger: The logger instance.
    """
    return Kestra.logger()
