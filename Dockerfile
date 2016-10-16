FROM python:3.5

WORKDIR /app

RUN curl -sL https://deb.nodesource.com/setup_4.x | bash -
RUN apt-get install -y nodejs \
    && npm install -g gulp

COPY package.json /app

RUN npm install

COPY requirements.txt /app

RUN pip install -r requirements.txt

COPY assets/ Gulpfile.js /app/

RUN gulp build

COPY . /app

CMD bash -c "python manage.py migrate && python manage.py collectstatic --noinput && gunicorn portailva.wsgi -b 0.0.0.0:8000"