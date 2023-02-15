import pytest
from datetime import datetime, timedelta


def get_date_days_away(days: int):
    now = datetime.now()
    next_week = now + timedelta(days=days)
    return next_week.strftime('%Y-%m-%d')


@pytest.fixture
def yesterday_date():
    return get_date_days_away(-1)


@pytest.fixture
def today_date():
    return get_date_days_away(0)


@pytest.fixture
def tomorrow_date():
    return get_date_days_away(1)


@pytest.fixture
def after_tomorrow_date():
    return get_date_days_away(2)


@pytest.fixture
def history_ok_args(today_date, yesterday_date):
    return [
        "history --symbol EUR",
        "history --symbol EUR CAD",
        f"history --start {yesterday_date} --symbol EUR",
        f"history --start {yesterday_date} --end {today_date} --symbol EUR",
        "history --base USD --symbol EUR",
        "history --start 2021-02-01 --end 2021-02-02 --base USD --symbol EUR",
        f"history --start {yesterday_date} --end {today_date} --base USD --symbol EUR"
    ]


@pytest.fixture
def history_wrong_dates(tomorrow_date, after_tomorrow_date):
    return [
        "history --start 1999-01-01 --symbol EUR",
        "history --start 1999-01-01 --end 1999-01-02 --symbol EUR",
        "history --end 1999-01-02 --symbol EUR",
        "history --start 2021-02-01 --end 2021-01-01 --symbol EUR"
        f"history --start {tomorrow_date} --symbol EUR",
        f"history --end {tomorrow_date} --symbol EUR",
        f"history --start {tomorrow_date} --end {after_tomorrow_date} --symbol EUR",
    ]


@pytest.fixture
def history_wrong_symbols():
    return [
        "history --base ZZZ --symbol EUR",
        "history --symbol EUR ZZZ",
        "history --symbol ZZZ",
    ]


@pytest.fixture
def convert_ok_args(today_date):
    return [
        "convert --symbol EUR --amount 50",
        "convert --symbol EUR --amount 50.06",
        "convert --symbol EUR --amount 50.9999999",
        "convert --symbol EUR --amount -50",
        "convert --base USD --symbol EUR --amount 50",
        "convert --date 2021-02-01 --symbol EUR --amount 50",
        "convert --date 2021-02-01 --base USD --symbol EUR --amount 50",
        f"convert --date {today_date} --base USD --symbol EUR --amount 50"
    ]


@pytest.fixture
def convert_wrong_dates(tomorrow_date, after_tomorrow_date):
    return [
        "convert --date 1999-01-01 --symbol EUR --amount 50",
        f"convert --date {tomorrow_date} --symbol EUR --amount 50",
        f"convert --date {after_tomorrow_date} --symbol EUR --amount 50",
    ]


@pytest.fixture
def convert_wrong_symbols():
    return [
        "convert --base ZZZ --symbol EUR --amount 50",
        "convert --symbol ZZZ --amount 50"
    ]