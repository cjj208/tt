FROM python:3.7.9
USER root
WORKDIR /root/tt

RUN \
apt-get update\
&& pip install --upgrade pip\
&& pip install numpy==1.14.5\
&& pip install pandas==0.23.4\
&& pip install python-dateutil==2.7.3\
&& pip install pytz==2018.5\
&& pip install six==1.11.0\
&& pip install forexconnect==1.6.3\
&& pip install DingtalkChatbot==1.5.1\
&& pip install ta==0.5.25\
&& pip install mplfinance==0.12.7a0
ENV TZ=Asia/Shanghai
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

ENV LANG C.UTF-8
#COPY ./main.py /tt/
#ENTRYPOINT ["python3"]
#CMD python main.py

#工作流程：
##检查后台进程和镜像
#docker images
#建立镜像
#docker build -t mm ./
#跑容器
#--交互式容器
#sudo docker container run --rm -it mm
#
#--守护式容器 
#可在DOCKERFILE中加入CMD运行python main.py 直接运行容器就能跑起来
# docker run -di --name=tt -v /home/jimc/tt:/root/tt fx 
#进入目录 ：sudo docker exec -it mm01 /bin/bash
#映射目录创建容器
#docker run -di --name=fx -v /home/jimc/tt:/root/tt mm:latest
#进入目录 ：sudo docker exec -it fx /bin/bash