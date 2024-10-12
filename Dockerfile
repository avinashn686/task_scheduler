# Dockerfile

# Use the official Python image.
FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /code
# Install system dependencies
RUN apt-get update && apt-get install -y redis-tools

# Install psql client
RUN apt-get update && apt-get install -y postgresql-client

# Install dependencies
COPY requirements.txt /code/
RUN pip install -r requirements.txt

# Copy project
COPY . /code/
