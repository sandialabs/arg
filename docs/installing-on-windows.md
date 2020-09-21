---
layout: default
title: Installing on Windows
subitem: Using
---
This page aims to provide instructions to install ARG on a Windows distribution.

# VM's WARNING:
Running ARG in Windows VM's might be not possible, because of OpenGL support.

# System architecture:
Use 64-bit versions of applications if your system supports them.

### Update your system

# ARG dependencies:

## 1. Python 3

- ARG requires Python3 version 3.7 or higher

- Download [Python](https://www.python.org/downloads/windows/)
  - for 64-bit system: Windows x86-64 executable installer
  - for 32-bit system: Windows x86 executable installer

- During installation, check 'Add Python 3.X to PATH' box and at the end, click on 'Disable path length limit'.

- Make sure python is in environment variable PATH.

- Add PYTHONPATH to environment variables:

  - if you installed python 3.8.x to `C:\Users\<YOUR_USER_NAME>\AppData\Local\Programs\Python\Python38\`, environment variable PYTHONPATH should be set as follows:  
    `C:\Users\<YOUR_USER_NAME>\AppData\Local\Programs\Python\Python38;
    C:\Users\<YOUR_USER_NAME>\AppData\Local\Programs\Python\Python38\Scripts;
    C:\Users\<YOUR_USER_NAME>\AppData\Local\Programs\Python\Python38\Lib\site-packages`
    
## 2. MiKTeX (TeX/LaTeX Windows alternative)
- Download [MiKTeX](https://miktex.org/download)
  - go to All downloads tab
  - choose basic installer according to system architecture
- For installation instruction https://miktex.org/howto/install-miktex
  - on settings mark always
- After installation, you will be notified about updates, update MiKTeX

## 3. ImageMagick
- Download [ImageMagick](https://imagemagick.org/script/download.php#windows)
  - for 64-bit system: Win64 static at 16 bits-per-pixel component
  - for 32-bit system: Win32 static at 16 bits-per-pixel component

## 4. Perl
- Download [Perl](http://strawberryperl.com/)
  - for 64-bit system: strawberry-perl-x.xx.x.x-64bit.msi
  - for 32-bit system: strawberry-perl-x.xx.x.x-32bit.msi

## 5. ARG
- In order to install ARG and its Python dependencies, put following commands line by line:  
```
python -m pip install --upgrade pip
pip install pyARG
```

## Post installation checks

To make sure everything was installed correctly, type `python -c "import arg; print(arg.__version__)"`. It should return **the** latest released version number. 