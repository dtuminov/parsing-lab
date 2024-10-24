FROM apache/airflow:latest
LABEL authors="dmitrijtuminov"

COPY requirements.txt ./
RUN pip install -r requirements.txt
COPY ./dags /opt/airflow/dags
