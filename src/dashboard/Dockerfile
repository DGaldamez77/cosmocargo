FROM python:3.14-rc-slim-bullseye

RUN apt-get update \
    && apt-get -y install libpq-dev gcc \
    && pip install psycopg2 \
    && apt-get install -y --no-install-recommends --no-install-suggests \
    build-essential default-libmysqlclient-dev pkg-config \
    && pip install --no-cache-dir --upgrade pip

WORKDIR /app
COPY ./requirements.txt /app
RUN pip install --no-cache-dir --requirement /app/requirements.txt
COPY . /app

ENV FLASK_APP=app.py
ENV DB_NAME=cosmocargo
ENV DB_USER=cosmocargo_service
ENV DB_PASSWORD=cosmocargo
ENV DB_HOST=172.17.0.1
ENV DB_PORT=5432

EXPOSE 8090

CMD ["flask", "run", "--host=0.0.0.0"]
