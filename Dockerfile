FROM python:3.5

WORKDIR /app
ADD . /app

RUN curl -sL https://deb.nodesource.com/setup_4.x | bash -
RUN apt-get install -y nodejs \
    && pip install -r requirements.txt \
    && npm install -g gulp \
    && npm install \
    && gulp build