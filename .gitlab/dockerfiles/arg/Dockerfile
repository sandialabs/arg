FROM fedora:latest

RUN dnf update -y
RUN dnf install -y dnf-plugins-core git texlive texlive-collection-latexextra dvipng latexmk texlive-stmaryrd ImageMagick
RUN dnf install -y mesa-libGL-devel mesa-libGLU xorg-x11-server-Xvfb glx-utils mesa-dri-drivers wget libxkbcommon-x11 git
RUN dnf install -y python3.8
RUN dnf install -y python3-pip
RUN python3 -m pip install --upgrade pip
RUN pip install virtualenv
RUN git clone https://gitlab.com/AutomaticReportGenerator/arg.git
WORKDIR /arg
RUN git checkout master
RUN mkdir /arg/in
RUN mkdir /arg/out
RUN virtualenv --python /usr/bin/python3.8 venv
RUN source venv/bin/activate && pip3 install -r requirements.txt

ENV PYTHONPATH /arg/venv/lib/python3.8/site-packages:/arg:/arg/arg
ENV DISPLAY :99.0
COPY entrypoint.sh /arg/entrypoint.sh
RUN ["chmod", "+x", "/arg/entrypoint.sh"]
ENTRYPOINT ["/arg/entrypoint.sh"]