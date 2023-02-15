import pytest
from unittest import mock
from conftest import *
from exrates import exrates_convert


@pytest.fixture()
def input_data():
    return {
        'date': '2023-02-14',
        'base': 'USD',
        'symbol': 'EUR',
        'amount': 50.0,
    }


@pytest.fixture()
def frankfurter_response():
    return {
        'amount': 50.0,
        'base': 'USD',
        'date': '2023-02-14',
        'rates': {'EUR': 46.473}
    }


@mock.patch("exrates.frankfurter_get_call")
def test_exrates_convert(
        frankfurter_get_call,
        input_data,
        frankfurter_response
):
    frankfurter_get_call.return_value = frankfurter_response
    conversion = exrates_convert(
        input_data['date'],
        input_data['base'],
        input_data['symbol'],
        input_data['amount']
    )
    assert isinstance(conversion, float)
    assert conversion == frankfurter_response['rates'][input_data['symbol']]
