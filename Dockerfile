FROM python:3.7.2-alpine3.9
# ENV PORT=0
ENV MOCKING=True
WORKDIR /TakeOnUi
copy . /TakeOnUi
RUN apk add --no-cache --virtual .build-deps gcc musl-dev && \
	pip install -r requirements.txt && \
	apk del .build-deps gcc musl-dev && \
	chmod +x entry.sh

ENTRYPOINT ["/TakeOnUi/entry.sh"]
