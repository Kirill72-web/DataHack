FROM ubuntu:18.04

RUN apt update
RUN apt install -y git
RUN git clone https://github.com/Kirill72-web/DataHack.git
RUN ['cd', 'DataHack']
