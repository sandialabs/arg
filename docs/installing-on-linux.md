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
sudo apt install -y python3 python3-pip texlive texlive-latex-extra 
sudo apt install -y dvipng texlive-science imagemagick
```
-   Fedora:  
```
sudo dnf install -y dnf-plugins-core texlive texlive-collection-latexextra 
sudo dnf install -y dvipng latexmk texlive-stmaryrd ImageMagick
```
-   Centos/RHEL:  
```
sudo yum install -y yum-utils wget epel-release gcc openssl-devel bzip2-devel 
sudo yum -y groupinstall "Development Tools"
sudo yum install -y libffi-devel wget latexmk texlive texlive-lastpage
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

- Check your Python3 current version Debian/Fedora/Centos/RHEL:
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
      python -m pip install --upgrade pip
      ```

  - if Python version 3.7 or higher is installed:
      ```
      sudo python3 -m pip install --upgrade pip
      python -m pip install --upgrade pip
      ```

  - if the only Python installed is Python3 version 3.7 or higher and previous step does not work:
      ```
      sudo python -m pip install --upgrade pip
      python -m pip install --upgrade pip
      ```

## 3. ARG 

In order to install ARG and its Python dependencies, put following commands line by line:
```
python -m pip install --upgrade pip
pip install pyARG
```

## Post installation checks

To make sure everything was installed correctly, type `python -c "import arg; print(arg.__version__)"`. It should return **the** latest released version number. 