FROM ubuntu:22.04

MAINTAINER Kirill Cymbaliuk <tsimbaliukk@ya.ru>

RUN apt-get update
RUN apt-get install -y git

ENV TZ=Europe/Moscow
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN apt-get install -y software-properties-common
RUN add-apt-repository ppa:deadsnakes/ppa
RUN apt-get install -y python3.9
RUN apt-get install -y curl
RUN curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
RUN apt-get install -y python3.9-distutils
RUN python3.9 get-pip.py

COPY . .

RUN python3.9 -m pip install -r requirements.txt

