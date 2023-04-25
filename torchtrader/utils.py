"""
This module contains various utility functions for the torchtrader app.

Functions: - timeframe_to_seconds(timeframe: str) -> int: Convert a timeframe string into the
number of seconds it represents."""
import datetime
import os
from pathlib import Path
from typing import Dict

# A dictionary that maps each time unit to the number of seconds in that unit
TIMEFRAME_TO_SECONDS: Dict[str, int] = {
    "m": 60,
    "h": 60 * 60,
    "d": 24 * 60 * 60,
    "w": 7 * 24 * 60 * 60,
    "M": 30 * 24 * 60 * 60,
    "y": 365 * 24 * 60 * 60,
}


def timeframe_to_seconds(timeframe: str) -> int:
    """
    Convert a timeframe string into the number of seconds it represents.

    Args: timeframe (str): A string representing the timeframe, e.g., "1m" for 1 minute,
    "1h" for 1 hour, etc.

    Returns:
        int: The number of seconds in the timeframe.

    Raises: ValueError: If the input string is not in a valid format, i.e., it does not end with
    one of the supported time units.

    Example:
        >>> timeframe_to_seconds("1m")
        60
        >>> timeframe_to_seconds("1h")
        3600
    """
    unit = timeframe[-1]
    if unit not in TIMEFRAME_TO_SECONDS:
        raise ValueError(f"Unsupported timeframe: {timeframe}")
    multiplier = int(timeframe[:-1])
    return multiplier * TIMEFRAME_TO_SECONDS[unit]


def generate_name(prefix: str) -> str:
    """
    Generates a string with a timestamp and a given prefix.

    Args:
        prefix (str): The prefix to use for the name.

    Returns:
        str: A string with the current timestamp and the given prefix.
    """

    # Get the current timestamp in UTC
    now = datetime.datetime.now(datetime.timezone.utc)

    # Format the timestamp string using ISO 8601 format
    timestamp_str = now.strftime("%Y%m%dT%H%M%SZ")

    return f"{prefix}_{timestamp_str}"


def find_file(filename: str) -> Path:
    # Check if file exists in current directory
    current_dir = Path.cwd()
    file_path = current_dir / filename
    if file_path.is_file():
        return file_path.resolve()

    # Check if file exists in parent directory
    parent_dir = current_dir.parent
    file_path = parent_dir / filename
    if file_path.is_file():
        return file_path.resolve()

    # Check all subdirectories in parent directory
    for root, dirs, files in os.walk(parent_dir):
        if filename in files:
            return (Path(root) / filename).resolve()


def find_dir(dirname: str) -> Path:
    current_dir = Path.cwd()
    parent_dir = current_dir.parent
    for root, dirs, _ in os.walk(parent_dir):
        if dirname in dirs:
            return (Path(root) / dirname).resolve()
