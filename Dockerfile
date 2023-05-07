FROM python:3.8.16-alpine3.17


COPY requirements.txt /
RUN pip --no-cache-dir install --upgrade pip setuptools
RUN pip --no-cache-dir install -r requirements.txt
RUN pip --no-cache-dir install "Flask[async]"

COPY . /webapps
WORKDIR /webapps