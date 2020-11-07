##FROM python:alpine3.7
##
##COPY . /app
##WORKDIR /app
##RUN apk update
##RUN apk add make automake gcc g++ subversion python3-dev
##RUN pip3.7 install --upgrade pip
##RUN pip3.7 install Cython
###RUN pip3.7 install -U spacy
##RUN pip3.7 install Flask~=1.1.2
###RUN pip3.6 install -r requirements.txt
##EXPOSE 5001
##CMD python ./app.py
#
##FROM tiangolo/uwsgi-nginx:python3.8-alpine
##COPY . /app
##WORKDIR /app
##RUN apk update
##RUN apk add make automake gcc g++ subversion python3-dev
##RUN pip3.8 install --upgrade pip
##RUN pip3.8 install Cython
###RUN pip3.7 install -U spacy
##RUN pip3.8 install ChatterBot~=1.0.5
###RUN pip3.6 install -r requirements.txt
##EXPOSE 5001
##CMD python ./app.py
#
##FROM tiangolo/uwsgi-nginx-flask:python3.7
##
##COPY requirements.txt .
##RUN pip3.7 install -r requirements.txt
##
##COPY . /app
##WORKDIR /app
##
##EXPOSE 5001
##CMD python3.7 ./app.py
#
#
#FROM python:3.7
#
## Copy application dependency manifests to the container image.
## Copying this separately prevents re-running pip install on every code change.
#COPY requirements.txt ./
#
## Install production dependencies.
#RUN set -ex; \
#    pip install -r requirements.txt; \
#    pip install gunicorn
#
## Copy local code to the container image.
#ENV APP_HOME /app
#WORKDIR $APP_HOME
#COPY . ./
#
## Run the web service on container startup. Here we use the gunicorn
## webserver, with one worker process and 8 threads.
## For environments with multiple CPU cores, increase the number of workers
## to be equal to the cores available.
#CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 -k uvicorn.workers.UvicornWorker main:app
#
FROM python:3.7-stretch
RUN apt-get update -y
RUN apt-get install -y python-pip python-dev build-essential
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
ENTRYPOINT ["python"]
CMD ["app.py"]