FROM python:3.8-slim-buster

# set working directory
WORKDIR /app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install python dependencies
COPY ./requirements.txt .

RUN pip install --upgrade -r requirements.txt

# add app
COPY . /app/ 