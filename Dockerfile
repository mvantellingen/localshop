FROM python:2.7

RUN apt-get update && apt-get install libmysqlclient-dev -y && \
    apt-get clean

ADD requirements.txt /tmp/
RUN pip install -r /tmp/requirements.txt

RUN mkdir /localshop
WORKDIR /localshop

RUN pip install mysqlclient==1.3.6

RUN mkdir /root/.localshop
ADD docker.conf.py /root/.localshop/localshop.conf.py

ADD . /localshop/
RUN python setup.py develop

ENTRYPOINT ["localshop"]
