FROM python:3.7.4-alpine3.10 as base


# Download and resolve any dependencies
FROM base as builder

RUN mkdir /install
WORKDIR /install
COPY requirements.txt /requirements.txt
RUN apk add --virtual .build-deps gcc musl-dev && \
    pip install --install-option="--prefix=/install" -r /requirements.txt


# Build our final image using the resolved dependencies and the application
FROM base

EXPOSE 5000
COPY --from=builder /install /usr/local
COPY . /TakeOnUi
WORKDIR /TakeOnUi
ENV PYTHONUNBUFFERED=0
CMD python -u application.py runserver
