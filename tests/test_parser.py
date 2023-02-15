import pytest
from exrates import parse_args
from conftest import *


def test_history_args(history_ok_args):
    for item in history_ok_args:
        parse_args(item.split())


def test_history_wrong_symbols(history_wrong_symbols):
    for item in history_wrong_symbols:
        with pytest.raises(SystemExit):
            parse_args(item.split())


def test_history_wrong_dates(history_wrong_dates):
    for item in history_wrong_dates:
        with pytest.raises(SystemExit):
            parse_args(item.split())


def test_convert_args(convert_ok_args):
    for item in convert_ok_args:
        parse_args(item.split())


def test_convert_wrong_dates(convert_wrong_dates):
    for item in convert_wrong_dates:
        with pytest.raises(SystemExit):
            parse_args(item.split())


def test_convert_wrong_symbols(convert_wrong_symbols):
    for item in convert_wrong_symbols:
        with pytest.raises(SystemExit):
            parse_args(item.split())
