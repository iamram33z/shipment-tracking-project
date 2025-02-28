FROM python:3.10-slim
WORKDIR /app
COPY transform_and_load.py .
RUN pip install google-cloud-bigquery google-cloud-storage
CMD ["python", "transform_and_load.py"]