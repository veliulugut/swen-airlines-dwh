FROM python:3.10-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir \
    streamlit==1.38.0 \
    pandas==2.1.4 \
    plotly==5.17.0 \
    altair==5.1.2 \
    sqlalchemy \
    psycopg2-binary

# Copy application files
COPY dashboard/ ./dashboard/
COPY data_gen/ ./data_gen/

# Set Python path
ENV PYTHONPATH=/app

# Expose port
EXPOSE 8501

# Run Streamlit
CMD ["streamlit", "run", "dashboard/app.py", "--server.port=8501", "--server.address=0.0.0.0"] 