from airflow import DAG
import datetime as dt
import pandas as pd

from operators.parsing import fetch_arxiv_titles_with_safari

path = 'https://arxiv.org/list/q-fin/2024-01?skip=0&show=2000'
file_name = 'page_info.json'
df = pd.DataFrame()

with DAG(
        dag_id='parse_article_from_page',
        start_date=dt.datetime(2024, 10, 16),
        schedule='@daily'
) as dag:
    # Вызов функции и сохранение в DataFrame
    fetch_arxiv_titles_with_safari(path)

    # Печатаем DataFrame
    df.to_json(file_name, orient='records', lines=True)  # сохранение в JSON