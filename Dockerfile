FROM python:2.7

MAINTAINER  Michael van Tellingen <michaelvantellingen@gmail.com>

# Install required packages
RUN apt-get update

# Create user / env
RUN useradd -r localshop -d /opt/localshop
RUN mkdir -p /opt/localshop/var && \
    chown -R localshop:localshop /opt/localshop/
RUN easy_install -U pip

WORKDIR /opt/localshop


ENV DJANGO_STATIC_ROOT /opt/localshop/static

# Install uWSGI / Honcho
run pip install psycopg2==2.6.0
run pip install uwsgi==2.0.10
run pip install honcho==0.6.6

# Install localshop
COPY ./ /opt/localshop/src/localshop
RUN cd /opt/localshop/src/localshop && \
  pip install .

# Switch to user
USER localshop

# Initialize the app
RUN DJANGO_SECRET_KEY=tmp localshop collectstatic --noinput

EXPOSE 8000

CMD uwsgi --http 0.0.0.0:8000 --module localshop.wsgi --master --die-on-term
