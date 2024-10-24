FROM apache/airflow:latest
LABEL authors="dmitrijtuminov"

RUN apt-get update && apt-get install -y \
    wget \
    gnupg2 \
    libglib2.0-0 \
    libnss3 \
    libgconf-2-4 \
    libxss1 \
    libappindicator3-1 \
    && rm -rf /var/lib/apt/lists/*

# Установите Chrome
RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb && \
    dpkg -i google-chrome-stable_current_amd64.deb; \
    apt-get -y -f install && \
    rm google-chrome-stable_current_amd64.deb


COPY requirements.txt ./
RUN pip install -r requirements.txt
COPY ./dags /opt/airflow/dags
