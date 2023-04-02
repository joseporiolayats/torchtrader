"""
Random functions to test
"""

from typing import Dict

import pytest


@pytest.fixture
def capture_stdout(monkeypatch: Dict) -> Dict:
    """
    Yes
    :param monkeypatch:
    :return:
    """
    buffer = {"stdout": "", "write_calls": 0}

    def fake_write(s: str) -> None:
        """
        Yes
        :param s:
        """
        buffer["stdout"] += s
        buffer["write_calls"] += 1
        print("Here")

    # monkeypatch.setattr(sys.stdout, "write", fake_write)
    return buffer


@pytest.fixture(scope="session")
def db_conn() -> None:
    """
    Random DB connection
    :return:
    """
    # # noinspection PyCompatibility
    # db = ...
    # # noinspection PyCompatibility
    # url = ...
    # with db.connect(url) as conn:  # connection will stop after tests
    #     yield conn
    print("Nothing")
