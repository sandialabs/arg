FROM python:3.7-buster

ARG PYTHON_VER=3.8
ARG PYTHON_REL=3.8.7
RUN apt-get update -y
RUN apt-get install -y build-essential libncursesw5-dev libreadline-gplv2-dev libssl-dev libgdbm-dev libc6-dev libsqlite3-dev libbz2-dev libffi-dev wget curl gcc make zlib1g-dev
WORKDIR /opt
RUN wget https://www.python.org/ftp/python/${PYTHON_REL}/Python-${PYTHON_REL}.tgz
RUN tar xzf Python-${PYTHON_REL}.tgz
RUN cd Python-${PYTHON_REL} && ./configure --enable-optimizations && make altinstall
RUN rm Python-${PYTHON_REL}.tgz
RUN curl -O https://bootstrap.pypa.io/get-pip.py
RUN python${PYTHON_VER} get-pip.py
RUN /usr/local/bin/python${PYTHON_VER} -m pip install --upgrade pip
RUN pip install virtualenv
WORKDIR /