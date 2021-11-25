"""Do no set values here, these are only read from environment.

To set these values, modify the setup.sh file in the root directory of the proyect.
"""
import os

# Stocks DB
DB_KWARGS = {
    "dialect": "postgresql",
    "user": os.getenv("STOCKS_DB_USER"),
    "password": os.getenv("STOCKS_DB_PASS"),
    "host": "stock-data-postgres",
    "port": 5432,
    "db": os.getenv("STOCKS_DB_NAME"),
}

# Stocks API Key
STOCKS_API_KEY = os.getenv("STOCKS_API_KEY")

# List of stocks to get
STOCKS_LS = os.getenv("STOCKS_LS").split(",")

# Path to the container directory where staging data is going to be stored
PATH = os.getenv("STAGING_PATH")
