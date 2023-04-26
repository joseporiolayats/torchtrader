"""
torchtrader/logs/logger.py

Torchtrader Logging Module

This module sets up loggers for different parts of the Torchtrader app. The loggers can
be imported and used in other modules to log messages with different levels of severity.
"""
import logging
import pathlib

import colorlog


def setup_logger(logger_name: str, log_file: str, level: int = logging.INFO) -> logging.Logger:
    """
    Set up a logger with the specified name, log file, and log level.

    Args:
        logger_name (str): The name of the logger.
        log_file (str): The file path where the logger should store logs.
        level (int, optional): The log level. Defaults to logging.INFO.

    Returns:
        logging.Logger: The configured logger instance.
    """

    # Get the absolute path of the 'torchtrader' folder
    base_dir = pathlib.Path(__file__).resolve().parent.parent.parent

    # Create the 'logs' folder if it does not exist
    logs_dir = base_dir / "logs"
    logs_dir.mkdir(exist_ok=True)

    # Get the absolute path of the log file
    log_file_path = logs_dir / log_file

    # Define log colors based on severity
    log_colors = {
        "DEBUG": "white",
        "INFO": "green",
        "WARNING": "yellow",
        "ERROR": "red",
        "CRITICAL": "bold_red",
    }

    logger = logging.getLogger(logger_name)
    logger.setLevel(level)

    # Create a file handler
    file_handler = logging.FileHandler(log_file_path)
    file_handler.setLevel(level)

    # Create a console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)

    # Use colorlog formatter for console handler
    console_formatter = colorlog.ColoredFormatter(
        "%(log_color)s%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        log_colors=log_colors,
        reset=True,
        style="%",
    )

    console_handler.setFormatter(console_formatter)

    # Create a formatter and add it to the file handler
    file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    file_handler.setFormatter(file_formatter)

    # Add the handlers to the logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger


# Set up loggers for different modules
app_logger = setup_logger("torchtrader", "torchtrader.log", logging.INFO)
trade_logger = setup_logger("torchtrader.trade", "torchtrader_trade.log", logging.DEBUG)
