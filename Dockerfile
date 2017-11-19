FROM alpine:3.6

MAINTAINER  Michael van Tellingen <michaelvantellingen@gmail.com>
ENV LOCALSHOP_ROOT /home/localshop/data/
ENV STATIC_ROOT /home/localshop/static/


# Add user so that we run as non-root
RUN addgroup -S localshop && adduser -S -D -G localshop localshop
RUN mkdir -p /home/localshop && chown localshop:localshop /home/localshop

RUN apk update
RUN apk add \
    gcc \
    gettext \
    imagemagick-dev \
    jpeg \
    jpeg-dev \
    libc-dev \
    linux-headers \
    pcre-dev \
    postgresql-dev \
    python3 \
    python3-dev \
    redis \
    zlib-dev \
    && rm -rf /var/cache/apk/*

RUN pip3 install honcho uwsgi==2.0.15

ADD src /code/src/
ADD setup.py README.rst MANIFEST.in /code/

RUN cd /code/ && pip3 install .

ADD ./docker/ /home/localshop/

USER localshop
WORKDIR /home/localshop/
RUN mkdir /home/localshop/data/
RUN localshop collectstatic

CMD /home/localshop/entrypoint.sh
