import typing as t
import argparse
import requests
import logging
import os
import sys
import json
from datetime import datetime

logger = logging.getLogger(__name__)

DEFAULT_SYMBOL = "USD"
DEFAULT_DATE = datetime.now().strftime('%Y-%m-%d')
FRANKFURTER_API_BASE_URL = "https://api.frankfurter.app"
MIN_DATE = "1999-01-04"
MIN_DATETIME = datetime.strptime(MIN_DATE, '%Y-%m-%d')


def supported_currencies() -> t.Dict[str, str]:
    """
    Retrieves supported currencies by the Frankfurter API
    :return: Dict with currencies symbols as keys and description as value
    """
    response = requests.get(f"{FRANKFURTER_API_BASE_URL}/currencies")
    try:
        response.raise_for_status()
    except requests.exceptions.HTTPError as ex:
        logger.error(f"Cannot get currency list, API unavailable: {ex}")

    return response.json()


def valid_date(s: str) -> datetime:
    """
    Checks if a string is a valid YYYY-MM-DD date
    Valid dates are not less than a given MIN_DATE nor higher than current date
    :param s: string to check date for
    :return:
    """
    try:
        date = datetime.strptime(s, "%Y-%m-%d")
        if date <= MIN_DATETIME:
            raise ValueError(f"Given date is earlier than minimum supported date: {MIN_DATE}")
        if date > datetime.now():
            raise ValueError(f"Given date is higher than today's date")
        return s
    except ValueError as ex:
        raise argparse.ArgumentTypeError(str(ex))


def frankfurter_get_call(url) -> t.Dict:
    """
    Calls Frankfurter API via GET on given path
    :param url: path to call to
    :return: API response as a Dict
    """
    try:
        response = requests.get(f"{FRANKFURTER_API_BASE_URL}/{url}")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as ex:
        logger.error(f"Cannot get currency list, API unavailable: {ex}")
        raise
    # This error might occur instead of a 404 in the Frankfurter API
    # Assume this means empty data
    except requests.exceptions.ChunkedEncodingError as ex:
        logger.warning(f"Invalid chunk encoding when calling API: {ex}")
        return {}
    # General exception handling for improper cases
    except Exception as ex:
        logger.error(f"Found unhandled exception when calling API: {ex}")
        raise


def exrates_history(
        start: str,
        end: str,
        base: str,
        symbol: t.List[str],
        output: t.Optional[str] = None,
        printable: bool = True
) -> t.List[t.Dict]:
    """
    Retrieves a list of historic exchange rates for a given currency
    to a set of currencies on a given period
    Uses Frankfurter API
    :param start: Date of first day to get data (YYYY-MM-DD format)
    :param end: Date of last day to get data (YYYY-MM-DD format)
    :param base: Original currency
    :param symbol: List of currencies to convert to
    :param output: Name of file to print result to.
                If None, no file is created/written to.
                None by default
    :param printable: If true, prints result to console. True by default.
    :return: List of dicts containing the retrieved info
    """
    # Build URL
    if (end == DEFAULT_DATE and end == start) or end == start:
        # When end date and start date is equal to today's date
        # We build without .. param which causes ChunkEncodingError in API request
        # Also for simplicity of response, when both end and start are the same date
        data_url = f"{start}" \
                   f"?from={base}" \
                   f"&to={','.join(symbol)}"
    else:
        data_url = f"{start}" \
                   f".." \
                   f"{end}" \
                   f"?from={base}" \
                   f"&to={','.join(symbol)}"
    logger.debug(f"Formed URL is: {data_url}")
    # Get request
    raw_data = frankfurter_get_call(data_url)

    # Parse data to desired format
    # The format received varies if an end date is given

    # Check that dates within response are between our params
    # For example, if start = today and API data is not yet live
    # we are sent yesterday's data
    # In this case, sent empty response
    if len(raw_data) == 0:
        output_data = []
    elif 'end_date' in raw_data:
        output_data = [
            {
                'date': date,
                'base': raw_data['base'],
                'symbol': symbol,
                'rate': raw_data['rates'][date][symbol]
            }
            for date in raw_data['rates']
            for symbol in raw_data['rates'][date]
            if start <= date <= end
        ]
    else:
        if raw_data['date'] >= start:
            output_data = [
                {
                    'date': raw_data['date'],
                    'base': raw_data['base'],
                    'symbol': symbol,
                    'rate': raw_data['rates'][symbol]
                }
                for symbol in raw_data['rates']
            ]
        else:
            output_data = []

    if printable:
        for line in output_data:
            print(json.dumps(line))

    # Write to output file if param is received
    if output is not None:
        # Get path of given output file
        file_name = os.path.abspath(f"{output}.jsonl")
        base_dir = os.path.dirname(file_name)
        try:
            if not os.path.isdir(base_dir):
                raise OSError(f"Cannot write to file, path does not exist: {base_dir}")
            logger.debug(f"Writing to file: {file_name}")
            with open(file_name, 'w', encoding='utf-8') as outfile:
                for line in output_data:
                    outfile.write(json.dumps(line))
                    outfile.write('\n')
        except OSError as ex:
            logger.error(str(ex))
            raise

    return output_data


def exrates_convert(
        date: str,
        base: str,
        symbol: str,
        amount: float,
        printable: bool = True
) -> float:
    """
    Converts an amount of one currency to another on a given day.
    Uses Frankfurter API
    :param date: Date of conversion (YYYY-MM-DD format)
    :param base: Original currency
    :param symbol: Currency to convert to
    :param amount: Amount to be converted
    :param printable: If true, prints result to console. True by default.
    :return: Converted currency value as float
    """
    # Build URL
    data_url = f"{date}" \
               f"?from={base}" \
               f"&to={symbol}" \
               f"&amount={amount}"
    logger.debug(f"Formed URL is: {data_url}")
    # Get request
    raw_data = frankfurter_get_call(data_url)
    conversion_value = raw_data['rates'][symbol]
    if printable:
        print(conversion_value)
    return conversion_value


def parse_args(args: t.List[str]) -> argparse.Namespace:
    """
    Parser for Exrates CLI
    :param args: Args of the execution
    :return: Namespace of the parsed args
    """
    # Get supported currencies from API
    currencies = supported_currencies()
    currency_symbols = list(currencies.keys())

    # Base Parser for CLI
    parser = argparse.ArgumentParser(
        prog='exrates',
        description=f"""
        Exrates provides historical information
        for a given currency exchange rates to a set of other
        currencies in an interval of dates. Also it can provide a
        conversion of currencies in any given day.

        Supported currencies are:
        {currencies}

        Data is only available for working days (M-F).
        Also current day data might not be available until 16 CET

        Minimum date available is: {MIN_DATE}

        Dates are always inclusive. 
        """,
        formatter_class=argparse.RawTextHelpFormatter
    )
    # Subcommands supported by CLI
    subparsers = parser.add_subparsers(help='Available subcommands: history/convert', dest='command')

    # History subcommand arguments
    parser_history = subparsers.add_parser(
        'history',
        help="Retrieves historical exchange conversions"
             " in a date range for a base currency"
             " and multiple other currencies"

    )
    parser_history.add_argument(
        '--start',
        '-f',
        default=DEFAULT_DATE,
        type=valid_date,
        help="Start date (YYYY-MM-DD). Inclusive. By default today"
    )
    parser_history.add_argument(
        '--end',
        '-t',
        default=DEFAULT_DATE,
        type=valid_date,
        help="End date (YYYY-MM-DD). Inclusive. By default today"
    )
    parser_history.add_argument(
        '--base',
        '-b',
        default=DEFAULT_SYMBOL,
        choices=currency_symbols,
        help="Base currency symbol. Defaults to USD"
    )
    parser_history.add_argument(
        '--symbol',
        '-s',
        required=True,
        choices=currency_symbols,
        nargs='+',
        help="Currencies to convert to. Accepts a space separated list of symbols. Required"
    )
    parser_history.add_argument(
        '--output',
        '-o',
        type=str,
        help="Path of file to write output to. JSONL format"
    )

    # Convert subcommand arguments
    parser_convert = subparsers.add_parser(
        'convert',
        help="Does currency conversion from one currency"
             " to another on a given date"
    )
    parser_convert.add_argument(
        '--date',
        '-d',
        default=DEFAULT_DATE,
        type=valid_date,
        help="Currency exchange date (YYYY-MM-DD). By default today"
    )
    parser_convert.add_argument(
        '--base',
        '-b',
        default=DEFAULT_SYMBOL,
        choices=currency_symbols,
        help="Base currency symbol. Defaults to USD"
    )
    parser_convert.add_argument(
        '--symbol',
        '-s',
        required=True,
        choices=currency_symbols,
        help="Currency to convert to. Required"
    )
    parser_convert.add_argument(
        '--amount',
        '-a',
        required=True,
        type=float,
        help="Amount to convert. Required"
    )

    # Parse args
    args = parser.parse_args(args)

    # Extra validation for history command
    # Verify that end is higher than start
    if args.command == "history":
        if args.start > args.end:
            parser_history.error(
                f"Given start ({args.start}) date"
                f" is higher than end date ({args.end})"
            )
    if args.command is None:
        parser.print_help()

    return args


def main_impl() -> t.Any:
    """
    Entry point to Exrates CLI
    :return: None
    """
    args = parse_args(sys.argv[1:])

    if args.command == "history":
        # Get history of exchange rates
        logger.debug(f"Calling history subcommand")
        return exrates_history(
            args.start,
            args.end,
            args.base,
            args.symbol,
            args.output
        )
    elif args.command == "convert":
        logger.debug(f"Calling convert subcommand")
        # Get conversion
        return exrates_convert(
            args.date,
            args.base,
            args.symbol,
            args.amount
        )


def main():
    try:
        main_impl()
    except Exception as ex:
        logger.critical("Uncaught top-level exception", exc_info=ex)
        raise


if __name__ == '__main__':
    main()
