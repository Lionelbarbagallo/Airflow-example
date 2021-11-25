"""Implements a function to create a DB stock table."""
from lbpackages.constants import DB_KWARGS
from lbpackages.exceptions.exceptions import DBException
from lbpackages.models.dbclient import DBApi
from lbpackages.models.stocks import Base


def create_tables():
    """Creates the 'stock_value' table into the stocks db.

    Returns
    -------
        DBError:
            If the functions fails, it raises a DBException. Otherwise it prints a success message.
    """
    try:
        engine = DBApi(**DB_KWARGS).get_engine()
        Base.metadata.create_all(engine)

        print("Table created succesfully")
    except:
        raise DBException from None
