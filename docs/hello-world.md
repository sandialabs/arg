---
layout: default
title: Hello World!
---

# Hello World!
The goal of this page is to provide the classic "Hello World!" example in the context of ARG.

## Report Structure
The structure of this report will be extremely simple, containing a single chapter with a single paragraph as follows:
```
---
chapters:
- n: chapter
  title: 'Hello, world!'
```
The above code snippet can be found in:
[tests/build_tests/hello_world/Report-hello_world.yml]({{ site.baseurl }}@@@../tests/build_tests/hello_world/Report-hello_world.yml@@@)

## Parameters File
Albeit able to process a large variety of options, ARG is designed to be able to produce reports even with minimal input of the user. However,
you will need to specify at least the following three options:
1. the name of the report structure file: e.g., `Report-hello_world.yml`;
2. the desired *type* of report: this version of ARG only supports the type `Report`;
3. the desired report *backend* to be used amongst `LaTeX` and `Word`.  

These values must be stored in a *parameters file*, for instance:
```
___
structure: Report-hello_world.yml
report_type: Report
backend_type: LaTeX
```
By default, ARG will look for a file called `parameters.yml`; if you want to use another parameters file name, you will have to specify it with the `-p` command line argument. Otherwise, simply executing the following command:
```
python ${PATH_TO_ARG}/Applications/ARG.py
```
where `PATH_TO_ARG` is the path to your local installation of ARG, will produce a report similar to the [expected one]() (dates and author name will vary).