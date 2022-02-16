# base image
FROM python:3.9-alpine

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work dir
WORKDIR /code

# Install package
COPY src/Pipfile src/Pipfile.lock /code/
RUN pip install pipenv && pipenv install --system

# Copy project
COPY src/. /code/