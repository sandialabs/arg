FROM python:3.8.5-slim-buster

RUN apt-get update -y
RUN apt-get install -y texlive texlive-latex-extra dvipng latexmk texlive-science
RUN apt-get install -y imagemagick make
RUN apt-get install -y xvfb
RUN apt-get install -y libgl1-mesa-dev libglu1-mesa xvfb
RUN apt-get install -y wget
RUN apt-get install -y latexmk
RUN python -m pip install --upgrade pip
RUN pip install virtualenv
