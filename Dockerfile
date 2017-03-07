FROM python:3.5

WORKDIR /app

# Idem for requirements.txt
COPY requirements.txt /app

RUN pip install -r requirements.txt

# Then copy the rest of the app
COPY . /app
