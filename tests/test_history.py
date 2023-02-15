import pytest
import os
import json
import shutil
from unittest import mock
from conftest import *
from exrates import exrates_history

@pytest.fixture()
def input_data():
    return [
        {
            'start': '2021-02-01',
            'end': '2021-02-01',
            'base': 'USD',
            'symbol': ['EUR']
        },
        {
            'start': '2021-02-01',
            'end': '2021-02-02',
            'base': 'USD',
            'symbol': ['EUR']
        },
    ]


@pytest.fixture()
def frankfurter_response():
    return [
        {
            'amount': 1.0,
            'base': 'USD',
            'date': '2021-02-01',
            'rates': {'EUR': 0.82754}
        },
        {
            'amount': 1.0,
            'base': 'USD',
            'start_date': '2021-02-01',
            'end_date': '2021-02-02',
            'rates':
                {
                    '2021-02-01': {'EUR': 0.82754},
                    '2021-02-02': {'EUR': 0.83029}
                }
        }
    ]


@pytest.fixture()
def final_json():
    return [
        [
            {
                'base': 'USD',
                'date': '2021-02-01',
                'symbol': 'EUR',
                'rate': 0.82754
            }
        ],
        [
            {
                'base': 'USD',
                'date': '2021-02-01',
                'symbol': 'EUR',
                'rate': 0.82754
            },
            {
                'base': 'USD',
                'date': '2021-02-02',
                'symbol': 'EUR',
                'rate': 0.83029
            }
        ]
    ]


@mock.patch("exrates.frankfurter_get_call")
def test_exrates_history(
        frankfurter_get_call,
        input_data,
        frankfurter_response,
        final_json
):
    for data, response, lines in zip(
            input_data,
            frankfurter_response,
            final_json
    ):

        frankfurter_get_call.return_value = response
        data = exrates_history(
            data['start'],
            data['end'],
            data['base'],
            data['symbol']
        )
        assert isinstance(data, list)
        for item in data:
            assert isinstance(item, dict)
        assert data == lines


@mock.patch("exrates.frankfurter_get_call")
def test_exrates_history_file_write(
        frankfurter_get_call,
        input_data,
        frankfurter_response,
        final_json
):
    abspath = os.path.abspath(os.curdir)
    example_file_name = "test"
    example_dir_name = "test_data"
    os.makedirs(example_dir_name, exist_ok=True)
    file_paths = [
        f"{example_file_name}",
        f"{os.path.join(abspath, example_file_name)}",
        f"{example_dir_name}/{example_file_name}"
    ]

    def file_name_with_jsonl_extension(s):
        return f"{s}.jsonl"

    for data, response, lines, file_path in zip(
            input_data,
            frankfurter_response,
            final_json,
            file_paths
    ):
        file_path_extension = file_name_with_jsonl_extension(file_path)
        if os.path.exists(file_path_extension):
            os.remove(file_path_extension)
        frankfurter_get_call.return_value = response
        exrates_history(
            data['start'],
            data['end'],
            data['base'],
            data['symbol'],
            output=file_path
        )

        assert os.path.isfile(file_path_extension)
        with open(file_path_extension, 'r') as read_file:
            file_data = []
            for line in read_file:
                file_data.append(json.loads(line))
            assert file_data == lines
        os.remove(file_path_extension)

    shutil.rmtree(example_dir_name)


@mock.patch("exrates.frankfurter_get_call")
def test_exrates_history_file_write_wrong_path(
        frankfurter_get_call,
        input_data,
        frankfurter_response
):
    example_file_name = "a/b/c/test"
    file_path = f"{example_file_name}"

    frankfurter_get_call.return_value = frankfurter_response[0]
    data = input_data[0]
    with pytest.raises(OSError):
        exrates_history(
            data['start'],
            data['end'],
            data['base'],
            data['symbol'],
            output=file_path
        )
