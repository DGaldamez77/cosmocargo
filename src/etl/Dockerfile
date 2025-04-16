FROM python:3.14-rc-slim-bullseye

RUN apt-get update \
    && apt-get -y install libpq-dev gcc \
    && apt-get update && apt-get install -y cron \
    && pip install psycopg2 \
    && apt-get install -y --no-install-recommends --no-install-suggests \
  build-essential default-libmysqlclient-dev pkg-config \
  && pip install --no-cache-dir --upgrade pip

WORKDIR /app
COPY ./requirements.txt /app
RUN pip install --no-cache-dir --requirement /app/requirements.txt
COPY . /app

COPY ./scripts/cron /etc/cron.d/etl-cron
RUN chmod 0644 /etc/cron.d/etl-cron
RUN crontab /etc/cron.d/etl-cron
COPY ./scripts/entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/scripts/entrypoint.sh
RUN chmod +x /app/scripts/runjob-for-docker.sh

VOLUME /app/etl_data

# CMD ["sh"]
CMD ["cron", "-f"]
