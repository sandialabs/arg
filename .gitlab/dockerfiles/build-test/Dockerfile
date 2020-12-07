FROM python:3.8-buster

RUN apt-get update -y
RUN apt-get install -y texlive texlive-latex-extra dvipng latexmk texlive-science
RUN apt-get install -y imagemagick make
RUN apt-get install -y xvfb
RUN apt-get install -y libgl1-mesa-dev libglu1-mesa xvfb
RUN apt-get install -y wget
RUN apt-get install -y latexmk libreoffice diffutils libreoffice-java-common
RUN python -m pip install --upgrade pip
RUN pip install virtualenv
RUN sed -i 's/<policy domain="coder" rights="none" pattern="PDF" \/>/<policy domain="coder" rights="read \| write" pattern="PDF" \/>/g' /etc/ImageMagick-6/policy.xml
