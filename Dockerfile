FROM python:3.7.9
USER root
WORKDIR /root/tt
RUN \
apt-get update\
&& pip install numpy==1.14.5\
&& pip install pandas==0.23.4\
&& pip install python-dateutil==2.7.3\
&& pip install pytz==2018.5\
&& pip install six==1.11.0\
&& pip install forexconnect==1.6.3\
&& pip install DingtalkChatbot==1.5.1\
&& pip install ta==0.5.9
COPY ./main.py /tt/
ENTRYPOINT ["python"]
CMD ["/tt/main.py"]