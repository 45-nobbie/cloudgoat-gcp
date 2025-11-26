FROM python:3.11-slim
WORKDIR /app
COPY mock-gcs.py /app/
RUN pip install --no-cache-dir flask
EXPOSE 5000
CMD ["python","mock-gcs.py"]
