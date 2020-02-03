FROM python:3.8.1-alpine3.10 as base


# Download and resolve any dependencies
FROM base as builder

RUN mkdir /install
WORKDIR /install
COPY requirements.txt /requirements.txt
RUN apk add --virtual .build-deps gcc musl-dev && \
    pip install --prefix=/install -r /requirements.txt --no-warn-script-location


# Build our final image using the resolved dependencies and the application
FROM base

EXPOSE 5000
COPY --from=builder /install /usr/local
COPY . /TakeOnUi
WORKDIR /TakeOnUi
ENV PYTHONUNBUFFERED=0
#CMD python -u application.py runserver
#GUnicorn
COPY gunicorn_config.py /gunicorn_config.py
#EXPOSE 5000

ENTRYPOINT ["/usr/local/bin/gunicorn", "--config", "/TakeOnUi/gunicorn_config.py", "application:app"]
