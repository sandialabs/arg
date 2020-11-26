FROM python:3.8.6-slim-buster

RUN apt-get update -y
RUN apt-get install -y texlive texlive-latex-extra dvipng latexmk texlive-science git wget curl gcc
RUN apt-get install -y imagemagick make libbz2-dev libffi-dev zlib1g-dev dvipng libc6-dev libsqlite3-dev
RUN apt-get install -y xvfb build-essential libncursesw5-dev libreadline-gplv2-dev libssl-dev libgdbm-dev
RUN apt-get install -y libgl1-mesa-dev libglu1-mesa xvfb latexmk

RUN curl -sL https://deb.nodesource.com/setup_14.x | bash -
RUN apt-get install -y nodejs

RUN python -m pip install --upgrade pip
RUN git clone https://gitlab.com/AutomaticReportGenerator/arg.git
WORKDIR /arg
RUN git checkout develop
RUN pip install -r requirements.txt

WORKDIR /arg/web/angular
RUN npm install
RUN npm audit fix
RUN npm install -g @angular/cli
RUN ng build --prod --base-href ../static/

RUN mkdir /arg/web/api/static && mkdir /arg/web/api/templates
RUN cp /arg/web/angular/dist/ARG-GUI-angular/index.html /arg/web/api/templates/index.html
RUN cp -a /arg/web/angular/dist/ARG-GUI-angular/. /arg/web/api/static/
RUN rm /arg/web/api/static/index.html

RUN sed -i 's/\/opt\/local\/bin\/python3.7/\/usr\/local\/bin\/python/g' /arg/arg/GUI/Logic/ARG-GUI-config.yml
RUN sed -i 's/\/opt\/local\/Library\/Frameworks\/Python.framework\/Versions\/3.7\/lib\/python3.7\/site-packages/\/usr\/local\/lib\/python3.8\/site-packages/g' /arg/arg/GUI/Logic/ARG-GUI-config.yml
RUN sed -i 's/\/Users\/myuser\/arg\/Applications\/ARG.py/\/arg\/Applications\/ARG.py/g' /arg/arg/GUI/Logic/ARG-GUI-config.yml
RUN sed -i 's/\/Users\/myuser\/Latex\/bin/\/usr\/bin\/latex/g' /arg/arg/GUI/Logic/ARG-GUI-config.yml
RUN mkdir /root/ARG/
RUN cp -a /arg/arg/GUI/Logic/ARG-GUI-config.yml /root/ARG/ARG-GUI-config.yml

ENV PYTHONPATH /usr/local/lib/python3.8/site-packages:/arg:/arg/arg:/arg/web/api
ENV FLASK_APP /arg/web/api
ENV FLASK_ENV development
ENV FLASK_RUN_PORT 5000

WORKDIR /arg/web/api

EXPOSE 5000

CMD ["/usr/local/bin/python", "-m", "flask", "run"]
