"""Function to retrieve stocks data from DB."""
from sqlalchemy.sql import text


def query_db(dbclient, ds):
    """Retrieves stocks data from the DB.

    Parameters
    ----------
    dbclient: lbpackages.models.dbclient
        is a dbclient object to interact with the db.
    ds: str
        the date of the report.
    Returns
    -------
    pd.DataFrame
        a DataFrame containing the required information.
    """
    query = text(
        f"select date, symbol, close from stock_value where date > (DATE('{ds}') - 7) AND date <= DATE('{ds}') order by date asc"
    )

    return dbclient.to_frame(sql=query)
