FROM ubuntu
RUN apt-get -y update
RUN apt-get -y install python3-pip
RUN pip3 install paho-mqtt
RUN pip3 install python-telegram-bot --upgrade

ADD numbers.csv /
ADD conf.py /
ADD run.py /

CMD [ "python3", "./run.py" ]
