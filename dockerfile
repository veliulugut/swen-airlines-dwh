FROM apache/airflow:2.7.3-python3.10

USER root
RUN apt-get update && apt-get install -y \
    build-essential \
    librdkafka-dev \
    && rm -rf /var/lib/apt/lists/*

USER airflow
COPY requirements.txt ./
RUN pip install --upgrade pip && \
    pip install --no-cache-dir --timeout=600 --retries=3 -r requirements.txt