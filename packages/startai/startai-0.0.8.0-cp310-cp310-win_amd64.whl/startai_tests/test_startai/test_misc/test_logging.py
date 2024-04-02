import pytest
import logging
import startai


def test_invalid_logging_mode():
    with pytest.raises(AssertionError):
        startai.set_logging_mode("INVALID")


def test_set_logging_mode():
    startai.set_logging_mode("DEBUG")
    assert logging.getLogger().level == logging.DEBUG

    startai.set_logging_mode("INFO")
    assert logging.getLogger().level == logging.INFO

    startai.set_logging_mode("WARNING")
    assert logging.getLogger().level == logging.WARNING

    startai.set_logging_mode("ERROR")
    assert logging.getLogger().level == logging.ERROR


def test_unset_logging_mode():
    startai.set_logging_mode("DEBUG")
    startai.set_logging_mode("INFO")
    startai.unset_logging_mode()
    assert logging.getLogger().level == logging.DEBUG
