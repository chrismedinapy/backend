FROM perrygeo/gdal-base:latest as builder

# Python dependencies that require compilation
COPY requirements.txt .
RUN python -m pip install cython numpy -c requirements.txt
RUN python -m pip install --no-binary fiona,rasterio,shapely -r requirements.txt
RUN pip uninstall cython --yes

FROM python:3.8-slim-buster as final
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
# Install the previously-built shared libaries from the builder image

RUN apt-get update \
    && apt-get install --yes --no-install-recommends \
        libfreexl1 libxml2 libpng16-16\
    && rm -rf /var/lib/apt/lists/*

# Install the previously-built shared libaries from the builder image
COPY --from=builder /usr/local /usr/local
RUN ldconfig
