FROM fedora:latest

RUN dnf update -y
RUN dnf install -y dnf-plugins-core git texlive texlive-collection-latexextra dvipng latexmk texlive-stmaryrd ImageMagick
RUN dnf install -y mesa-libGL-devel mesa-libGLU xorg-x11-server-Xvfb glx-utils mesa-dri-drivers wget libxkbcommon-x11
RUN python3 -m pip install --upgrade pip
RUN pip3 install virtualenv