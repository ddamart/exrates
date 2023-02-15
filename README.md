# Exrates

This is a CLI Tool that uses Frankfurter API to retrieve historical exchange rates between multiple currencies as well as doing exchange rate conversions for specific values and
dates.

It provides two subcommands to work with:

* history: Retrieves historical exchange conversions in a date range for a base currency and multiple other currencies
* convert: Does currency conversion from one currency to another on a given date

## Quick Start

* Install

   ```
   pip install exrates
   ```

* CLI help

   ```
   >exrates -h
   usage: exrates [-h] {history,convert} ...

        Exrates provides historical information
        for a given currency exchange rates to a set of other
        currencies in an interval of dates. Also it can provide a
        conversion of currencies in any given day.

        Supported currencies are:
        {'AUD': 'Australian Dollar', 'BGN': 'Bulgarian Lev', 'BRL': 'Brazilian Real', 'CAD': 'Canadian Dollar', 'CHF': 'Swiss Franc', 'CNY': 'Chinese Renminbi Yuan', 'CZK': 'Czech Koruna', 'DKK': 'Danish Krone', 'EUR': 'Euro', 'GBP': 'British Pound', 'HKD': 'Hong Kong Dollar', 'HUF': 'Hungarian Forint', 'IDR': 'Indonesian Rupiah', 'ILS': 'Israeli New Sheqel', 'INR': 'Indian Rupee', 'ISK': 'Icelandic Króna', 'JPY': 'Japanese Yen', 'KRW': 'South Korean Won', 'MXN': 'Mexican Peso', 'MYR': 'Malaysian Ringgit', 'NOK': 'Norwegian Krone', 'NZD': 'New Zealand Dollar', 'PHP': 'Philippine Peso', 'PLN': 'Polish Złoty', 'RON': 'Romanian Leu', 'SEK': 'Swedish Krona', 'SGD': 'Singapore Dollar', 'THB': 'Thai Baht', 'TRY': 'Turkish Lira', 'USD': 'United States Dollar', 'ZAR': 'South African Rand'}

        Data is only available for working days (M-F).
        Also current day data might not be available until 16 CET

        Minimum date available is: 1999-01-04

        Dates are always inclusive.


   positional arguments:
     {history,convert}  Available subcommands: history/convert
       history          Retrieves historical exchange conversions in a date range for a base currency and multiple other currencies
       convert          Does currency conversion from one currency to another on a given date
   
   optional arguments:
     -h, --help         show this help message and exit
   ```
  
   ```
   >exrates history -h
   usage: exrates history [-h] [--start START] [--end END]
                          [--base {AUD,BGN,BRL,CAD,CHF,CNY,CZK,DKK,EUR,GBP,HKD,HUF,IDR,ILS,INR,ISK,JPY,KRW,MXN,MYR,NOK,NZD,PHP,PLN,RON,SEK,SGD,THB,TRY,USD,ZAR}]
                          --symbol
                          {AUD,BGN,BRL,CAD,CHF,CNY,CZK,DKK,EUR,GBP,HKD,HUF,IDR,ILS,INR,ISK,JPY,KRW,MXN,MYR,NOK,NZD,PHP,PLN,RON,SEK,SGD,THB,TRY,USD,ZAR}
                          [{AUD,BGN,BRL,CAD,CHF,CNY,CZK,DKK,EUR,GBP,HKD,HUF,IDR,ILS,INR,ISK,JPY,KRW,MXN,MYR,NOK,NZD,PHP,PLN,RON,SEK,SGD,THB,TRY,USD,ZAR} ...]
                          [--output OUTPUT]
   
   optional arguments:
     -h, --help            show this help message and exit
     --start START, -f START
                           Start date (YYYY-MM-DD). Inclusive. By default today
     --end END, -t END     End date (YYYY-MM-DD). Inclusive. By default today
     --base {AUD,BGN,BRL,CAD,CHF,CNY,CZK,DKK,EUR,GBP,HKD,HUF,IDR,ILS,INR,ISK,JPY,KRW,MXN,MYR,NOK,NZD,PHP,PLN,RON,SEK,SGD,THB,TRY,USD,ZAR}, -b {AUD,BGN,BRL,CAD,CHF,CNY,CZK,DKK,EUR,GBP,HKD,HUF,IDR,ILS,INR,ISK,JPY,KRW,MXN,MYR,NOK,NZD,PHP,PLN,RON,SEK,SGD,THB,TRY,USD,ZAR}
                           Base currency symbol. Defaults to USD
     --symbol {AUD,BGN,BRL,CAD,CHF,CNY,CZK,DKK,EUR,GBP,HKD,HUF,IDR,ILS,INR,ISK,JPY,KRW,MXN,MYR,NOK,NZD,PHP,PLN,RON,SEK,SGD,THB,TRY,USD,ZAR} [{AUD,BGN,BRL,CAD,CHF,CNY,CZK,DKK,EUR,GBP,HKD,HUF,IDR,ILS,INR,ISK,JPY,KRW,MXN,MYR,NOK,NZD,PHP,PLN,RON,SEK,SGD,THB,TRY,USD,ZAR} ...], -s {AUD,BGN,BRL,CAD,CHF,CNY,CZK,DKK,EUR,GBP,HKD,HUF,IDR,ILS,INR,ISK,JPY,KRW,MXN,MYR,NOK,NZD,PHP,PLN,RON,SEK,SGD,THB,TRY,USD,ZAR} [{AUD,BGN,BRL,CAD,CHF,CNY,CZK,DKK,EUR,GBP,HKD,HUF,IDR,ILS,INR,ISK,JPY,KRW,MXN,MYR,NOK,NZD,PHP,PLN,RON,SEK,SGD,THB,TRY,USD,ZAR} ...]
                           Currencies to convert to. Accepts a space separated list of symbols. Required
     --output OUTPUT, -o OUTPUT
                           Path of file to write output to. JSONL format
   ```

   ```
   >exrates convert -h
   usage: exrates convert [-h] [--date DATE]
                          [--base {AUD,BGN,BRL,CAD,CHF,CNY,CZK,DKK,EUR,GBP,HKD,HUF,IDR,ILS,INR,ISK,JPY,KRW,MXN,MYR,NOK,NZD,PHP,PLN,RON,SEK,SGD,THB,TRY,USD,ZAR}]
                          --symbol
                          {AUD,BGN,BRL,CAD,CHF,CNY,CZK,DKK,EUR,GBP,HKD,HUF,IDR,ILS,INR,ISK,JPY,KRW,MXN,MYR,NOK,NZD,PHP,PLN,RON,SEK,SGD,THB,TRY,USD,ZAR}
                          --amount AMOUNT
   
   optional arguments:
     -h, --help            show this help message and exit
     --date DATE, -d DATE  Currency exchange date (YYYY-MM-DD). By default today
     --base {AUD,BGN,BRL,CAD,CHF,CNY,CZK,DKK,EUR,GBP,HKD,HUF,IDR,ILS,INR,ISK,JPY,KRW,MXN,MYR,NOK,NZD,PHP,PLN,RON,SEK,SGD,THB,TRY,USD,ZAR}, -b {AUD,BGN,BRL,CAD,CHF,CNY,CZK,DKK,EUR,GBP,HKD,HUF,IDR,ILS,INR,ISK,JPY,KRW,MXN,MYR,NOK,NZD,PHP,PLN,RON,SEK,SGD,THB,TRY,USD,ZAR}
                           Base currency symbol. Defaults to USD
     --symbol {AUD,BGN,BRL,CAD,CHF,CNY,CZK,DKK,EUR,GBP,HKD,HUF,IDR,ILS,INR,ISK,JPY,KRW,MXN,MYR,NOK,NZD,PHP,PLN,RON,SEK,SGD,THB,TRY,USD,ZAR}, -s {AUD,BGN,BRL,CAD,CHF,CNY,CZK,DKK,EUR,GBP,HKD,HUF,IDR,ILS,INR,ISK,JPY,KRW,MXN,MYR,NOK,NZD,PHP,PLN,RON,SEK,SGD,THB,TRY,USD,ZAR}
                           Currency to convert to. Required
     --amount AMOUNT, -a AMOUNT
                           Amount to convert. Required
                           
   ```

* Example usage
   
   ```
  >exrates history --start 2021-02-01 --end 2021-02-02 --base USD --symbol EUR CAD
  {"date": "2021-02-01", "base": "USD", "symbol": "CAD", "rate": 1.2805}
  {"date": "2021-02-01", "base": "USD", "symbol": "EUR", "rate": 0.82754}
  {"date": "2021-02-02", "base": "USD", "symbol": "CAD", "rate": 1.2805}
  {"date": "2021-02-02", "base": "USD", "symbol": "EUR", "rate": 0.83029}
   ```
  
   ```
   >exrates convert --date 2021-02-01 --base USD --symbol EUR --amount 50
   41.377
   ```
  
## Docker

A Dockerfile is provided to deploy an image of this CLI.

First build the container with

```
>docker build -t exrates .
```

And now, to run:

```
>docker run exrates history --start 2021-02-01 --end 2021-02-02 --base USD --symbol EUR CAD
{"date": "2021-02-01", "base": "USD", "symbol": "CAD", "rate": 1.2805}
{"date": "2021-02-01", "base": "USD", "symbol": "EUR", "rate": 0.82754}
{"date": "2021-02-02", "base": "USD", "symbol": "CAD", "rate": 1.2805}
{"date": "2021-02-02", "base": "USD", "symbol": "EUR", "rate": 0.83029}
```

```
>docker run exrates convert --date 2021-02-01 --base USD --symbol EUR --amount 50
41.377
```


