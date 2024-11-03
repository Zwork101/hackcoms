FROM debian:bookworm-slim

# RUN mkdir -p /var/www/Locker
# RUN chown newuser /var/www/Locker
# USER newuser
WORKDIR /var/www/GroupUs

COPY requirements.txt .

COPY hackcoms hackcoms
COPY static static
COPY templates templates
COPY db.sql db.sql

RUN apt-get update && apt-get -y upgrade
RUN apt-get --yes install python3.11 python3-pip curl lsb-release
RUN sh -c 'echo "deb http://apt.postgresql.org/pub/repos/apt $(lsb_release -cs)-pgdg main" > /etc/apt/sources.list.d/pgdg.list'
RUN curl -fsSL https://www.postgresql.org/media/keys/ACCC4CF8.asc | gpg --dearmor -o /etc/apt/trusted.gpg.d/postgresql.gpg
RUN apt-get update
RUN apt-get --yes install postgresql-17
RUN apt clean

ARG POSTGRES_URI

RUN pip install --no-cache-dir -r requirements.txt --break-system-packages

EXPOSE 80

CMD gunicorn hackcoms.app:app --bind 0.0.0.0:80