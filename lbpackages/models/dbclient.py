"""Implements a client definition to interact with the DB."""
import pandas as pd
from sqlalchemy import create_engine


class DBApi:
    """Parent class to conect to a DB using SQLAlchemy.

    Attributes
    ----------
        dialect: str
            dialect to use in the SQALChemy engine
        host: str
            dns name of the host of the DB
        port: int
            port where the DB is listening
        user: str
            username to conect to the DB
        password: str
            password for this username
        db: str
            DB to connect
    """

    def __init__(
        self, dialect: str, host: str, port: int, user: str, password: str, db: str
    ) -> None:
        """Constructor method for this class.

        Parameters
        ----------
            dialect: str
                dialect to use in the SQALChemy engine
            host: str
                dns name of the host of the DB
            port: int
                port where the DB is listening
            user: str
                username to conect to the DB
            password: str
                password for this username
            db: str
                DB to connect
        """
        self.dialect = dialect
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.db = db
        self._engine = None

    def get_engine(self):
        """Creates engine to handle DBAPI connections.

        Returns
        -------
            Engine: object
                manages many individual DBAPI connections.
        """
        db_uri = f"""{self.dialect}://{self.user}:{self.password}@{self.host}:{self.port}/{self.db}"""
        if not self._engine:
            self._engine = create_engine(db_uri)
        return self._engine

    def connect(self):
        """Conects to a DB.

        Returns
        -------
            Conection: object
                is a proxy object for an actual DBAPI connection.
        """
        return self.get_engine().connect()


class DBClient(DBApi):
    """Implements methods to interact with the DB.

    Attributes
    ----------
        dialect: str
            dialect to use in the SQALChemy engine
        host: str
            dns name of the host of the DB
        port: int
            port where the DB is listening
        user: str
            username to conect to the DB
        password: str
            password for this username
        db: str
            DB to connect
    """

    def __init__(
        self, dialect: str, host: str, port: int, user: str, password: str, db: str
    ) -> None:
        """Constructor method for this class.

        Parameters
        ----------
            dialect: str
                dialect to use in the SQALChemy engine
            host: str
                dns name of the host of the DB
            port: int
                port where the DB is listening
            user: str
                username to conect to the DB
            password: str
                password for this username
            db: str
                DB to connect
        """
        DBApi.__init__(self, dialect, host, port, user, password, db)

    @staticmethod
    def _cursor_columns(cursor):
        """Gets cursor columns.

        Parameters
        ----------
            cursor: object
                DB cursor to traverse the data
        Returns
        -------
            list:
                list of columns in the table, if there are any
        """
        if hasattr(cursor, "keys"):
            return cursor.keys()
        else:
            return [c[0] for c in cursor.description]

    def execute(self, sql, connection=None):
        """Executes SQL queries against the DB.

        Parameters
        ----------
            sql: object
                SQLAlchemy TextClause object representing an sql statement.
            connection: None or object
                proxy for an actual DBAPI connection. If None, one is created.
        Returns
        -------
            ResultProxy: object
                DB-API cursor object to provide easier access to row columns.
        """
        if connection is None:
            connection = self.connect()
        return connection.execute(sql)

    def insert_from_frame(self, df, table, if_exists="append", index=False, **kwargs):
        """Inserts a pandas Data Frame into the DB.

        Parameters
        ----------
            df: pandas Data Frame
                a dataframe to be inserted into the DB
            table: str
                table where to insert the dataframe
            if_exists: {"append", "fails", "replace"}
                what to do if the table already exists in DB.
            index: bool
                wheather to consider the dataframe index as a column or not
            **kwargs:
                arbitrary dictionary with params. See also https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.to_sql.html
        Raises
        ------
            ValueError:
               When the table already exists and if_exists is ‘fail'.
        """
        connection = self.connect()
        with connection:
            df.to_sql(table, connection, if_exists=if_exists, index=index, **kwargs)

    def to_frame(self, *args, **kwargs):
        """Executes a SQL query and returns a Data Frame.

        Parameters
        ----------
            *args:
                arbitrary list with params.
            **kwargs:
                arbitrary dictionary with params.
        Returns
        -------
            df: pandas.DataFrame
                a pandas DataFrame representing the result of the query.
        """
        cursor = self.execute(*args, **kwargs)
        if not cursor:
            return
        data = cursor.fetchall()
        if data:
            df = pd.DataFrame(data, columns=self._cursor_columns(cursor))
        else:
            df = pd.DataFrame()
        return df
