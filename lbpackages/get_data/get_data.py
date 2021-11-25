"""Class to download stock data from the API and store it."""
import os
import time

import pandas as pd
import requests

from lbpackages.exceptions.exceptions import (
    StocksApiException,
    StocksAvailabilityException,
    StocksDownloadException,
    StocksProcessingException,
)


class StocksApiClient:
    """Downloads and saves stock information.

    Attributes
    ----------
      api_key: str
        api key to connect to the service
      raw_data: bytes
        raw data received from the API
    """

    def __init__(self, api_key: str) -> None:
        """Constructor of the class.

        Parameters
        ----------
          api_key: str
            api key to connect to the service
          raw_data: bytes
            raw data received from the API
        """
        self.api_key = api_key
        self.raw = None

    def _download_data(self, ticker):
        """Downloads the ticker data for the given date.

        Parameters
        ----------
          ticker: str
            the stock to download information
          date: str
            the date to download in the format YYYY-MM-DD
        Raises
        ------
          StocksApiException
            in case of failure getting the information from the API. Also informs the status code.
          StocksDownloadException
            in case of any other error not related to the API.
        """
        try:
            url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={ticker}&datatype=csv&apikey={self.api_key}"
            r = requests.get(url)
            if r.status_code != 200:
                raise StocksApiException(r.status_code) from None
            self.raw = r
        except Exception as e:
            raise StocksDownloadException(e) from None

    def _format_data(self, ticker: str, date: str) -> pd.DataFrame:
        """Formats the raw data received from the API call.
        Parameters
        ----------
          ticker: str
            the stock to process
          date: str
            the date to filter from the response in the format YYYY-MM-DD
        Returns
        -------
          pd.DataFrame
            DataFrame with the stock data for the given date.
        """
        filtered_lines = [
            line[:-1]
            for line in [
                [ticker] + line.decode("utf-8").split(",")
                for line in self.raw.iter_lines()
            ]
            if line[1] == date
        ]

        return pd.DataFrame(filtered_lines)

    def process_stock_data(self, stocks: list, date: str, path: str) -> None:
        """Downloads the stocks information and stores it in the given path.

        Parameters
        ----------
          stocks: list of str
            list of comma separated tickers to download
          date: str
            the date to download in the format YYYY-MM-DD. Discards all others.
          path: str
            absolute path to the directory where data is to be stored
        Returns
        -------
          fn: str
            name of the saved file
        Raises
        ------
          StocksProcessingException
            in case of failure processing the data
        """
        try:
            stocks_df = []
            for ticker in stocks:
                self._download_data(ticker)
                stocks_df.append(self._format_data(ticker, date))
                time.sleep(30)  # Sleep to avoid Api rate limit
            stocks_df = pd.concat(stocks_df)
            if len(stocks_df) == 0:
                raise StocksAvailabilityException from None
            fn = os.path.join(path, date + "_stocks_data.csv")
            stocks_df.to_csv(fn, index=False, header=False)
            print(f"Data Processed with Success. File saved : {fn}")
            return fn
        except Exception as e:
            raise StocksProcessingException(e) from None
