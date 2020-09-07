FROM centos:latest

RUN yum install -y yum-utils wget epel-release gcc openssl-devel
RUN yum -y groupinstall "Development Tools"
RUN yum -y install openssl-devel bzip2-devel sqlite-devel libxkbcommon-x11
RUN yum install -y libffi-devel git latexmk texlive texlive-lastpage libxkbcommon-devel
RUN yum install -y texlive-stmaryrd texlive-pdftex texlive-latex-bin
RUN yum install -y texlive-texconfig* texlive-latex* texlive-metafont*
RUN yum install -y texlive-cmap* texlive-ec texlive-fncychap* texlive-pdftex-def
RUN yum install -y texlive-fancyhdr* texlive-titlesec* texlive-multirow libxkbcommon-devel
RUN yum install -y texlive-framed* texlive-wrapfig* texlive-parskip*
RUN yum install -y texlive-caption texlive-ifluatex* texlive-collection-fontsrecommended
RUN yum install -y mesa-libGL-devel mesa-libGLU xorg-x11-server-Xvfb glx-utils libxcb
RUN yum install -y mesa-dri-drivers dvipng ImageMagick texlive-collection-latexrecommended

RUN cd ~/
RUN wget https://www.python.org/ftp/python/3.8.5/Python-3.8.5.tgz
RUN tar xvf Python-3.8.5.tgz
RUN cd Python-3.8.5 && ./configure --enable-optimizations --enable-loadable-sqlite-extensions && make altinstall

RUN python3.8 -m pip install --upgrade pip
RUN pip3.8 install virtualenv

RUN wget https://cbs.centos.org/kojifiles/packages/texlive/2014/18.20140525_r34255.el7/noarch/texlive-spverbatim-svn15878.v1.0-18.el7.noarch.rpm
RUN yum -y install ./texlive-spverbatim-svn15878.v1.0-18.el7.noarch.rpm
RUN rm texlive-spverbatim-svn15878.v1.0-18.el7.noarch.rpm

