import pytest
from unittest import mock
from conftest import *
from exrates import main_impl, parse_args


@pytest.fixture()
def history_ok_inputs(history_ok_args):
    return [
        parse_args(item.split())
        for item in history_ok_args
    ]


@pytest.fixture()
def convert_ok_inputs(convert_ok_args):
    return [
        parse_args(item.split())
        for item in convert_ok_args
    ]


@mock.patch("exrates.parse_args")
def test_full_history_for_ok_inputs(
        args,
        history_ok_inputs
):
    for item in history_ok_inputs:
        args.return_value = item
        main_impl()


@mock.patch("exrates.parse_args")
def test_full_convert_for_ok_inputs(
        args,
        convert_ok_inputs
):
    for item in convert_ok_inputs:
        args.return_value = item
        main_impl()
