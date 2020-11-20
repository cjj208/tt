# alpine为musl libc核心，虽然小巧，但一部分功能受限，下面的numpy安装时需要UnixCCompiler编译才可通过
#FROM python:3.8.0-alpine3.10
FROM python:3.7
RUN python -m pip install forexconnect
RUN pip3 install -r requirements.txt
RUN mkdir -p /workfolder
COPY ./main.py /workfolder/

CMD [ "python", "/workfolder/main.py" ]
