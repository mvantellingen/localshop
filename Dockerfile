FROM ubuntu:14.04

MAINTAINER  Michael van Tellingen <michaelvantellingen@gmail.com>

# Install required packages
RUN apt-get update
RUN apt-get install -y python-dev python-setuptools libffi-dev libssl-dev python-psycopg2

# Create user / env
RUN useradd -r localshop -d /localshop
RUN mkdir -p /localshop/.localshop && \
    chown -R localshop:localshop /localshop
RUN touch /localshop/.localshop/localshop.conf.py
RUN easy_install -U pip


ENV DJANGO_STATIC_ROOT /localshop/static


# Install localshop
RUN pip install https://github.com/mvantellingen/localshop/archive/develop.zip#egg=localshop

# Install uWSGI / Honcho
run pip install uwsgi==2.0.10
run pip install honcho==0.6.6


# Switch to user
USER localshop

# Initialize the app
RUN DJANGO_SECRET_KEY=tmp localshop collectstatic --noinput

CMD DJANGO_SECRET_KEY=tmp localshop migrate --noinput

EXPOSE 8000

