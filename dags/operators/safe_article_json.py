from airflow.decorators import task
import pandas as pd
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',  # Формат сообщений
    handlers=[
        logging.FileHandler('app.log'),  # Сохранение логов в файл
        logging.StreamHandler()          # Вывод логов в консоль
    ]
)

@task
def save_df_to_json(df, file_name):
    logging.info('Try to safe data')
    df.to_json(file_name, orient='records', lines=True)
    logging.info('Data saved')