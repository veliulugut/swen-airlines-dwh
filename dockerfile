FROM apache/airflow:2.7.3-python3.10

COPY requirements.txt ./
RUN pip install --upgrade pip && \
    pip install --no-cache-dir --timeout=300 --retries=5 -r requirements.txt