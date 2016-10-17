FROM python:3.5

WORKDIR /app

RUN curl -sL https://deb.nodesource.com/setup_4.x | bash -
RUN apt-get install -y nodejs \
    && npm install -g gulp

# If package.json is modified, then cache will be invalidated and subsequent instructions won't use cache
# Therefore, npm install will run
COPY package.json /app

RUN npm install

# Idem for requirements.txt
COPY requirements.txt /app

RUN pip install -r requirements.txt

# And for gulp assets : gulp will rerun only if assets, package.json or requirements.txt are modified
COPY assets/ Gulpfile.js /app/

RUN gulp build

# Then copy the rest of the app
COPY . /app
