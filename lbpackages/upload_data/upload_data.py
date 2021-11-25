"""Class to read data from .csv files and upload it into th DB."""
from sqlalchemy.orm import sessionmaker

from lbpackages.exceptions.exceptions import UploadException
from lbpackages.models import dbclient, stocks


class StocksUploaderDB:
    """Uploads .csv files with stocks data to the DB.

    Attributes
    ----------
    dbclient: lbpackges.models.dbclients.DBApi
      handles DB conections
    file: str
      the .csv file with stocks data to read
    """

    def __init__(self, dbapi: dbclient.DBApi, file: str) -> None:
        """Constructor for the class.

        Parameters
        ----------
        dbclient: lbpackges.models.dbclients.DBApi
          handles DB conections
        file: str
          the .csv file with stocks data to read
        """
        self.dbapi = dbapi
        self.file = file
        self._session = None

    def _get_session(self) -> None:
        """Creates DB session to interact with DB using SQLAlchemy."""
        self._session = sessionmaker(bind=self.dbapi.get_engine())()

    @staticmethod
    def _read_file(file) -> list:
        """Reads and parses the .csv file with stock data.

        Parameters
        ----------
        file: str
          the .csv file with stocks data to read
        Yields
        ------
        list
          a list containing each of the fields of the parsed .csv lines
        """
        with open(file, "r", encoding="utf-8") as file_handle:
            for row in file_handle:
                yield row.split(",")

    def _create_model(self, args: list) -> None:
        """Adds stock data to the ORM model using StockValue class.

        Parameters
        ----------
        args: list
          list with arbitrary stock data to add to the model
        """
        self._session.add(stocks.StockValue(*args))

    def upload_db(self) -> None:
        """Reads the file, procesess the information and uploads to DB.

        Raises
        ------
        UploadException
          in case of error or exception while processing or uploading data.
        """
        try:
            if not self._session:
                self._get_session()

            for line in self._read_file(self.file):
                self._create_model(line)

            self._session.commit()
            self._session.close()

            print("Data Upload Complete")
        except Exception:
            raise UploadException from None
