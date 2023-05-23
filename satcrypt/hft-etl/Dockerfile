FROM python:3.8-alpine

RUN apk update && apk add gcc musl-dev

RUN mkdir /app
ADD . /hft-etl
WORKDIR /hft-etl

RUN pip install -r requirements.txt

CMD ["python3", "/hft-etl/src/main.py"]
