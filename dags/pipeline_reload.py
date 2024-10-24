import logging
from airflow import DAG
import datetime as dt
import pandas as pd

from operators.parsing import fetch_arxiv_titles_with_safari
from operators.safe_article_json import save_df_to_json

path = 'https://arxiv.org/list/q-fin/2024-01?skip=0&show=2000'
file_path = '/opt/airflow/dags/data/page_info.json'

with DAG(
        dag_id='parse_article_from_page',
        start_date=dt.datetime(2024, 10, 16),
        schedule='@daily'
) as dag:

    # Вызов функции и сохранение в DataFrame
    df = fetch_arxiv_titles_with_safari(path)
    save_df_to_json(df, file_path)


