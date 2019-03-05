FROM python:3.7.2-alpine3.9
ENV PORT=0
WORKDIR /TakeOnUi
copy . /TakeOnUi
RUN apk add --no-cache --virtual .build-deps gcc musl-dev && \
	pip install -r requirements.txt && \
	apk del .build-deps gcc musl-dev

ENTRYPOINT ["/TakeOnUi/entry.sh"]
