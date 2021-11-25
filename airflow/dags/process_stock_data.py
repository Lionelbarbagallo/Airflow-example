"""Process Stock Data DAG."""
from datetime import datetime
import os

from constants import DB_KWARGS, STOCKS_API_KEY, STOCKS_LS, PATH, S3_BUCKET

from airflow import DAG
from airflow.hooks.S3_hook import S3Hook
from airflow.operators.bash import BashOperator
from airflow.operators.python_operator import PythonOperator, PythonVirtualenvOperator


def _get_data(STOCKS_API_KEY, STOCKS_LS, ds, PATH):
    """Fetches data from the API, formats and saves it locally."""
    from lbpackages.get_data import get_data

    api_client = get_data.StocksApiClient(STOCKS_API_KEY)
    fn = api_client.process_stock_data(STOCKS_LS, ds, PATH)

    return fn


def _upload_data_db(fn, DB_KWARGS):
    """Reads data saved locally and uploads it to DB."""
    from lbpackages.models import dbclient
    from lbpackages.upload_data import upload_data

    dbclient = dbclient.DBApi(**DB_KWARGS)
    uploader = upload_data.StocksUploaderDB(dbclient, fn)
    uploader.upload_db()


def _create_daily_report(DB_KWARGS, PATH, ds):
    """Creates and saves locally daily report from stock data."""
    from lbpackages.plotting import plotting

    plotting.plot(DB_KWARGS, PATH, ds)


def _upload_file_to_S3(fn, s3_fn, bucket_name):
    """Uploads the report to S3."""
    hook = S3Hook("s3_conn")
    hook.get_conn().upload_file(
        fn, bucket_name, s3_fn, ExtraArgs={"ContentType": "text/html"}
    )


with DAG(
    "process_stock_data",
    schedule_interval="0 0 * * 1-5",
    start_date=datetime(2021, 11, 1),
    catchup=True,
) as dag:

    get_data = PythonVirtualenvOperator(
        task_id="get_data",
        python_callable=_get_data,
        op_kwargs={
            "DB_KWARGS": DB_KWARGS,
            "STOCKS_API_KEY": STOCKS_API_KEY,
            "STOCKS_LS": STOCKS_LS,
            "PATH": PATH,
            "ds": "{{ ds }}",
        },
        requirements=["lbpackages==0.3.1"],
        system_site_packages=False,
    )

    upload_data_db = PythonVirtualenvOperator(
        task_id="upload_data_db",
        python_callable=_upload_data_db,
        op_kwargs={
            "DB_KWARGS": DB_KWARGS,
            "fn": "{{ ti.xcom_pull(task_ids='get_data')}}",
        },
        requirements=["lbpackages==0.3.1"],
        system_site_packages=False,
    )

    remove_data = BashOperator(
        task_id="remove_data",
        bash_command="rm {{ ti.xcom_pull(task_ids=['get_data'])[0]}}",
    )

    create_daily_report = PythonVirtualenvOperator(
        task_id="create_daily_report",
        python_callable=_create_daily_report,
        op_kwargs={
            "DB_KWARGS": DB_KWARGS,
            "PATH": PATH,
            "ds": "{{ ds }}",
        },
        requirements=["lbpackages==0.3.1"],
        system_site_packages=False,
    )

    upload_to_S3 = PythonOperator(
        task_id="upload_to_S3",
        python_callable=_upload_file_to_S3,
        op_kwargs={
            "fn": os.path.join(PATH, "stocks_daily_report.html"),
            "s3_fn": "stocks-daily-report.html",
            "bucket_name": S3_BUCKET,
        },
    )
get_data >> upload_data_db >> remove_data >> create_daily_report >> upload_to_S3
