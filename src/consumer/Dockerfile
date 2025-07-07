FROM python:3.12-slim

WORKDIR /app

COPY . .
RUN pip install --no-cache-dir -r requirements.txt
RUN rm requirements.txt

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN adduser --disabled-password --gecos '' --uid 1001 appuser && chown -R appuser /app
USER 1001

EXPOSE 9991


ENTRYPOINT ["python", "consumer.py"]


# Image Metadata
LABEL version="1.0.0"
LABEL description="Dockerfile for the GTFS RT consumer"