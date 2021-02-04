FROM ubuntu:focal-20210119

RUN apt update && apt install -y \
    python3-pip

WORKDIR /src
ADD . /
RUN pip3 install -r requirements.txt
CMD ["python3","app.py"]