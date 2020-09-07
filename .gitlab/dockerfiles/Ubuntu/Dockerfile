FROM ubuntu:latest

ARG TZ=America/Denver
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN apt-get update && apt-get upgrade -y
RUN apt-get install -y python3 python3-pip texlive texlive-latex-extra wget curl gcc make libbz2-dev libffi-dev zlib1g-dev
RUN apt-get install -y dvipng texlive-science imagemagick libgl1-mesa-dev libglu1-mesa xvfb libc6-dev libsqlite3-dev
RUN apt-get install -y build-essential libncursesw5-dev libreadline-gplv2-dev libssl-dev libgdbm-dev latexmk
RUN apt-get install -y --no-install-recommends libxkbcommon-x11-0

RUN cd ~/
RUN wget https://www.python.org/ftp/python/3.8.5/Python-3.8.5.tgz
RUN tar xvf Python-3.8.5.tgz
RUN cd Python-3.8.5 && ./configure --enable-optimizations --enable-loadable-sqlite-extensions && make altinstall

RUN python3.8 -m pip install --upgrade pip
RUN pip3.8 install virtualenv