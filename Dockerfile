#FROM python:alpine3.7
#
#COPY . /app
#WORKDIR /app
#RUN apk update
#RUN apk add make automake gcc g++ subversion python3-dev
#RUN pip3.7 install --upgrade pip
#RUN pip3.7 install Cython
##RUN pip3.7 install -U spacy
#RUN pip3.7 install Flask~=1.1.2
##RUN pip3.6 install -r requirements.txt
#EXPOSE 5001
#CMD python ./app.py

#FROM tiangolo/uwsgi-nginx:python3.8-alpine
#COPY . /app
#WORKDIR /app
#RUN apk update
#RUN apk add make automake gcc g++ subversion python3-dev
#RUN pip3.8 install --upgrade pip
#RUN pip3.8 install Cython
##RUN pip3.7 install -U spacy
#RUN pip3.8 install ChatterBot~=1.0.5
##RUN pip3.6 install -r requirements.txt
#EXPOSE 5001
#CMD python ./app.py

FROM tiangolo/uwsgi-nginx-flask:python3.7

COPY requirements.txt .
RUN pip3.7 install -r requirements.txt

COPY . /app
WORKDIR /app

EXPOSE 5001
CMD python3.7 ./app.py

