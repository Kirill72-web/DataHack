FROM ubuntu:22.04

ENV TZ=Europe/Moscow
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN apt-get update
RUN apt-get install -y software-properties-common
RUN add-apt-repository ppa:deadsnakes/ppa
RUN apt-get install -y python3.9
RUN apt-get install -y python3-pip

RUN pip3 install numpy
RUN pip3 install pandas
RUN pip3 install spark


#RUN git clone https://github.com/Kirill72-web/DataHack.git
#RUN ['cd', 'DataHack']