FROM python:3.11-slim

WORKDIR /app

# Upgrade pip to the latest version
RUN pip install --upgrade pip

COPY requirements.txt .
RUN pip install opentelemetry.instrumentation
# Make sure requirements.txt does not contain 'opentelemetry-instrumentation-nats'
RUN pip install --no-cache-dir -r requirements.txt

COPY main.py .

CMD ["python", "main.py"]