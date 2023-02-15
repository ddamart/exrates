import pytest
import os
import json
import shutil
import requests
import typing as t
from unittest import mock
from conftest import *
from exrates import frankfurter_get_call


@pytest.fixture()
def get_ok_response():
    mock_response = mock.Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {'test':'test'}
    return mock_response


@pytest.fixture()
def get_bad_responses():
    mock_response_not_found = mock.Mock()
    mock_response_not_found.status_code = 404
    mock_response_not_found.raise_for_status.side_effect = requests.exceptions.HTTPError

    mock_response_server_error = mock.Mock()
    mock_response_server_error.status_code = 500
    mock_response_server_error.raise_for_status.side_effect = requests.exceptions.HTTPError

    return [
        mock_response_not_found,
        mock_response_server_error
    ]


@pytest.fixture()
def get_chunked_encoding_exc():
    mock_response = mock.Mock()
    mock_response.raise_for_status.side_effect = requests.exceptions.ChunkedEncodingError

    return mock_response


@pytest.fixture()
def frankfurter_full_requests():

    return [
        (
            "2021-02-02..2021-02-02?from=USD&to=EUR",
            {
                "amount": 1.0,
                "base": "USD",
                "start_date": "2021-02-02",
                "end_date": "2021-02-02",
                "rates": {"2021-02-02": {"EUR": 0.83029}}
            }
        ),
        (
            "2021-02-02?from=USD&to=EUR",
            {
                "amount": 1.0,
                "base": "USD",
                "date": "2021-02-02",
                "rates": {"EUR": 0.83029}
            }
        ),
        (
            "2021-02-02?from=USD&to=EUR&amount=50.0",
            {
               "amount": 50.0,
               "base": "USD",
               "date": "2021-02-02",
               "rates": {"EUR": 41.514}
            }
        )
    ]

@mock.patch("requests.get")
def test_ok_status(
        request,
        get_ok_response
):
    request.return_value = get_ok_response
    response = frankfurter_get_call(get_ok_response.url)
    assert response == get_ok_response.json()


@mock.patch("requests.get")
def test_wrong_status(
        request,
        get_bad_responses
):
    for response in get_bad_responses:
        request.return_value = response
        with pytest.raises(requests.exceptions.HTTPError):
            frankfurter_get_call(response.url)


@mock.patch("requests.get")
def test_chunked_encoding_error(
        request,
        get_chunked_encoding_exc
):
    request.return_value = get_chunked_encoding_exc
    with pytest.raises(requests.exceptions.ChunkedEncodingError):
        frankfurter_get_call(get_chunked_encoding_exc.url)


def test_full_api_calls(
        frankfurter_full_requests
):
    for full_request in frankfurter_full_requests:
        url, response = full_request
        data = frankfurter_get_call(url)
        assert data == response



