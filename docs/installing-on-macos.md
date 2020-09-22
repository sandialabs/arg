---
layout: default
title: Installing on macOS
subitem: Using
---

This provides instructions to install ARG on a macOS system.

# 1. Python

ARG is implemented in Python, version >= 3.7. It is therefore required to have a working version of Python, which can be done as follows:

<!-- (note that super-user/sudoer/administrator permissions are required to follow the instructions below -- contact sysadmin to get those rights) -->


In order to run ARG on macOS, you must have [Xcode](https://developer.apple.com/xcode/) installed on your system.

It is crucially important that you **not** use the "system Python" that comes with a macOS and is installed at `/usr/bin/python.publish` for the two following reasons:  
1. even with recent versions of macOS (e.g., Mojave) it is an older version than the one required by ARG; and
2. it has non-standard Python package set-up, making it complicated to install/upgrade packages needed by ARG.

As a result, you may build/install Python from scratch (the pros and cons are the same for Linux), but we recommend the simpler MacPorts route, which we are continuously testing and validating, as follows:

-   if you don't have MacPorts see <https://www.macports.org/> for installing instructions
-   install MacPorts Python as follows:
```  
sudo port install python38
sudo port select --set python python38
```
Finally, we also recommend that you use the `pip` Python package installer provided by MacPorts, as follows:
```
sudo port install py38-pip
sudo port select --set pip pip38
```
in order to install **all** Python dependencies required by ARG in a single command:
```
sudo port install pyARG-dep
``` 

Note that if you do not have `sudo` privilege on your system, you may replace `port install` with `pip install --user` in order to obtain a local installation available as opposed to a system-wide one.

# 2. LaTeX

In order to use the LaTeX/PDF backend of ARG, it is required to have a fairly rich installation of LaTeX distribution. On Linux/Debian and macOS, it is recommended to use TeX Live, that is known to work perfectly with ARG. This can be achieved as follows (with the same warnings as above regarding the use of `sudo`):

Using MacPorts:
```
sudo port install texlive-basic texlive-bin texlive-bin-extra texlive-common texlive-fonts-recommended texlive-latex texlive-latex-extra texlive-latex-recommended texlive-math-science texlive-pictures
```

# 3. ImageMagick

This bitmap editing application is mostly used by ARG to trim unnecessary white/transparent outline. Although optional, it is highly recommended to install it to improve visual artifacts.
It may be installed as follows:
```
sudo port install ImageMagick
```

## 4. ARG 

In order to install ARG and its Python dependencies, put following commands line by line:
```
python -m pip install --upgrade pip
pip install pyARG
```

## Post installation checks

To make sure everything was installed correctly, type `python -c "import arg; print(arg.__version__)"`. It should return **the** latest released version number. 