FROM ubuntu:16.04
FROM python:3.5.2

ADD Server.py /
ADD DatabaseOperation.py /
ADD sqlite.db /

ADD static/ /static/
ADD templates/ /templates/
#ADD templates/index.html /templates/
#ADD templates/login.html /templates/
#ADD templates/register.html /templates/

RUN pip install flask -i https://mirrors.ustc.edu.cn/pypi/web/simple
RUN pip install psutil -i https://mirrors.ustc.edu.cn/pypi/web/simple

CMD ["python", "./Server.py"]
