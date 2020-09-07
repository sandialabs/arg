---
layout: default
title: Installing on Linux
subitem: Using
---

This provides instructions to install ARG on a a Linux distribution (we note that ARG's continuous integration pipeline tests on the following distributions: Debian, CentOS, Fedora, and Ubuntu).

## Update your system:

-   Debian/Ubuntu:
```
sudo apt update && sudo apt upgrade -y
```
-   Fedora:  
```
sudo dnf update -y
```
-   Centos/RHEL:  
```
sudo yum update -y
```

# ARG dependencies:

## 1. Install dependencies (LaTeX, ImageMagick, etc..):

-   Debian/Ubuntu:
```
sudo apt install -y git python3 python3-pip texlive texlive-latex-extra 
sudo apt install -y dvipng texlive-science imagemagick
```
-   Fedora:  
```
sudo dnf install -y dnf-plugins-core git texlive texlive-collection-latexextra 
sudo dnf install -y dvipng latexmk texlive-stmaryrd ImageMagick
```
-   Centos/RHEL:  
```
sudo yum install -y yum-utils wget epel-release gcc openssl-devel bzip2-devel 
sudo yum -y groupinstall "Development Tools"
sudo yum install -y libffi-devel git wget latexmk texlive texlive-lastpage
sudo yum install -y texlive-stmaryrd texlive-pdftex texlive-latex-bin
sudo yum install -y texlive-texconfig* texlive-latex* texlive-metafont*
sudo yum install -y texlive-cmap* texlive-ec texlive-fncychap* texlive-pdftex-def
sudo yum install -y texlive-fancyhdr* texlive-titlesec* texlive-multirow
sudo yum install -y texlive-framed* texlive-wrapfig* texlive-parskip* 
sudo yum install -y texlive-caption texlive-ifluatex* texlive-collection-fontsrecommended  
sudo yum install -y mesa-libGL-devel mesa-libGLU xorg-x11-server-Xvfb glx-utils
sudo yum install -y mesa-dri-drivers dvipng ImageMagick texlive-collection-latexrecommended
wget https://cbs.centos.org/kojifiles/packages/texlive/2014/18.20140525_r34255.el7/noarch/texlive-spverbatim-svn15878.v1.0-18.el7.noarch.rpm
sudo yum -y install ./texlive-spverbatim-svn15878.v1.0-18.el7.noarch.rpm
rm texlive-spverbatim-svn15878.v1.0-18.el7.noarch.rpm
```

## 2. Python 3

- ARG requires Python3 version 3.7 or higher

- check your Python3 current version Debian/Fedora/Centos/RHEL:
  - `python -V`
  - `python3 -V`

- Resolving Python versions:

  - 1.) if `python -V` output was `Command python not found` but `python3 -V` returned version 3.7 or higher, then:
    - check for binary `which python3` should output `/usr/bin/python3`
    - make a link `sudo ln -s /usr/bin/python3 /usr/bin/python`
    
  - 2.) if both `python -V` and `python3 -V` outputs were `Command python not found`, then:
    - install python3 `sudo <apt/yum/dnf> install python3 -y`
    - if now `python3 -V` returned version 3.7 or higher, follow point 1.)

  - 3.) if `python -V` output was `Python 2.7.xx` but `python3 -V` returned version 3.7 or higher, then:
    - use `python3` command instead of `python` for pip installation and Virtualenv creation

  - 4.) if `python -V` or `python3 -V` returned version 3.6 or lower, Python has to be build from source

- Building from source:

  - At the moment making this instruction newest Python version is 3.8.5

  - for the newer numbers can be substituted (3.8.5 => 3.8.6, etc..)
  ```
  cd ~/
  wget https://www.python.org/ftp/python/3.8.5/Python-3.8.5.tgz
  tar xvf Python-3.8.5.tgz
  cd Python-3.8.5
  sudo ./configure --enable-optimizations --enable-loadable-sqlite-extensions
  sudo make altinstall
  ```

- Install Virtualenv:

  - if Python was built from source:
      ```
      python3.8 -m pip install --upgrade pip
      pip3.8 install virtualenv
      cd ~/
      git clone https://gitlab.com/AutomaticReportGenerator/arg.git
      cd arg/
      virtualenv venv
      source venv/bin/activate
      python -m pip install --upgrade pip
      pip install -r requirements.txt
      export PYTHONPATH=~/arg/venv/lib/python3.8/site-packages:~/arg:${PYTHONPATH}
      ```

  - if Python version 3.7 or higher is installed:
      ```
      sudo python3 -m pip install --upgrade pip
      sudo pip3 install virtualenv
      cd ~/
      git clone https://gitlab.com/AutomaticReportGenerator/arg.git
      cd arg/
      virtualenv venv
      source venv/bin/activate
      python -m pip install --upgrade pip
      pip install -r requirements.txt
      ```

    - if Python 3.7 is installed then change `<x>` to `7`, if 3.8, then change `<x>` to `8`
      ```
      export PYTHONPATH=~/arg/venv/lib/python3.<x>/site-packages:~/arg:${PYTHONPATH}
      ```

  - if the only Python installed is Python3 version 3.7 or higher and previous step does not work:
      ```
      sudo python -m pip install --upgrade pip
      sudo pip install virtualenv
      cd ~/
      git clone https://gitlab.com/AutomaticReportGenerator/arg.git
      cd arg/
      virtualenv venv
      source venv/bin/activate
      python -m pip install --upgrade pip
      pip install -r requirements.txt
      ```
    - if Python 3.7 is installed then change `<x>` to `7`, if 3.8, then change `<x>` to `8`
      ```
      export PYTHONPATH=~/arg/venv/lib/python3.<x>/site-packages:~/arg:${PYTHONPATH}
      ```

## 3. Post installation checks

To make sure everything was installed correctly, some tests can be built:
- if Virtualenv is activated and PYTHONPATH is exported:
    ```
    cd ~/arg/tests/build_tests
    python test.py
    ```

- if not, then activate Virtualenv and export PYTHONPATH, change `<x>` as before
    ```
    cd ~/arg
    source venv/bin/activate
    export PYTHONPATH=~/arg/venv/lib/python3.<x>/site-packages:~/arg:${PYTHONPATH}
    cd ~/arg/tests/build_tests
    python test.py
    ```
  
Any errors during tests will be reported to console.
After successful built results (pdf and docx reports) can be found here: `~/arg/tests/build_tests` in each case directory