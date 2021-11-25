"""Implements generic exceptions for the package."""


class DBException(Exception):
    """
    Exception raised for errors while creating the stocks table in the DB.

    Atributes
    ----------
        message: str
             explanation of the error
    """

    def __init__(self) -> None:
        """Constructor of the class."""

        message = "There was some kind of problem creating the table"
        Exception.__init__(self, message)


class StocksDownloadException(Exception):
    """
    Exception raised for errors while downloading stocks data not related to the API.

    Attributes
    ----------
        message: str
             explanation of the error
    """

    def __init__(self, e):
        message = f"There was some kind of problem while downloading stocks data: {e}"
        Exception.__init__(self, message)


class StocksProcessingException(Exception):
    """
    Exception raised for errors while processing stocks data.

    Attributes
    ----------
        message: str
             explanation of the error
    """

    def __init__(self, e):
        message = f"There was some kind of problem while proccesing stocks data: {e}"
        Exception.__init__(self, message)


class StocksAvailabilityException(Exception):
    """
    Exception raised when there is no information for the given day.

    Attributes
    ----------
        message: str
             explanation of the error
    """

    def __init__(self):
        message = "There was no information for the required date."
        Exception.__init__(self, message)


class StocksApiException(Exception):
    """
    Exception raised for errors while getting data from the API.

    Attributes
    ----------
        message: str
             explanation of the error with the returned status code from the API
    """

    def __init__(self, code):
        message = f"There was some kind of problem using the Stocks API. Returned code: {code}"
        Exception.__init__(self, message)


class UploadException(Exception):
    """
    Exception raised for errors while uploading stocks data.

    Attributes
    ----------
        message: str
             explanation of the error
    """

    def __init__(self):
        message = "There was some kind of problem uploading the data to the DB."
        Exception.__init__(self, message)
