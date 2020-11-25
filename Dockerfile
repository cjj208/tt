FROM continuumio/anaconda3:2019.10
MAINTAINER "chanjianjunv1.01"
USER root
RUN apt-get update\
    && python -m pip install forexconnect\
    && pip install DingtalkChatbot\
    && pip install ta\

    && git clone https://github.com/cjj208/tt\
    && cd tt\

CMD [ "python", "/tt/main.py" ]


