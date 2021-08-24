ARG APP_IMAGE=python:3.9.5-alpine

FROM $APP_IMAGE AS base

FROM base as builder

RUN mkdir /install
WORKDIR /install

COPY requirements.txt /requirements.txt

RUN pip install -r /requirements.txt

FROM base
ENV FLASK_APP flask.py
WORKDIR /project
COPY --from=builder /install /usr/local
ADD . /project

ENTRYPOINT ["python", "-m", "flask", "run"]
