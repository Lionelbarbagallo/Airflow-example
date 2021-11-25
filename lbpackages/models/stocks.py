"""Data model definition to interact with the stocks DB."""

from sqlalchemy import Column, Date, Float, Integer, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class StockValue(Base):
    """Stock value data model.

    Attributes
    ----------
        symbol: str
            the ticker of the stock
        date: str
            the date in a format compatible with the standard module datetime
        open: float
            the opening value of the stock
        high: float
            the higest value of the stock during the trading day
        low: float
            the lowest value of the stock during the trading day
        close:
            the closing price of the stock
    """

    __tablename__ = "stock_value"
    id = Column(Integer, primary_key=True)
    symbol = Column(String)
    date = Column(Date)
    open = Column(Float)
    high = Column(Float)
    low = Column(Float)
    close = Column(Float)

    def __init__(
        self, symbol: str, date: str, open: float, high: float, low: float, close: float
    ) -> None:
        """Constructor of the class.

        Parameters
        ----------
            symbol: str
                the tocker of the stock
            date: str
                the date in a format compatible with the standard module datetime
            open: float
                the opening value of the stock
            high: float
                the higest value of the stock during the trading day
            low: float
                the lowest value of the stock during the trading day
            close:
                the closing price of the stock
        """
        self.symbol = symbol
        self.date = date
        self.open = open
        self.high = high
        self.low = low
        self.close = close

    def __repr__(self) -> str:
        """Shows what the class is.

        Returns
        -------
            str
                str showing the ticker of the stock
        """
        return f"<StockValue(symbol='{self.symbol}')>"
