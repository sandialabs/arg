---
layout: default
title: GUI Examples
subitem: Using
---

This page aims to provide GUI examples.  

ARG currently has two types of GUI. Both use the same engine but do not run in the same environments. 

# Python Qt GUI

The Python GUI is coded in Qt which provides generic graphical results:  
![Qt-report-information]({{ site.baseurl }}/assets/images/Qt-report-information.png){:width="680"}  
![Qt-general-options]({{ site.baseurl }}/assets/images/Qt-general-options.png){:width="680"}  
![Qt-data-options]({{ site.baseurl }}/assets/images/Qt-data-options.png){:width="680"}  
![Qt-inserts]({{ site.baseurl }}/assets/images/Qt-inserts.png){:width="680"}  

## Running the Qt GUI
It is quite easy to run with a single-line command:   
`python -c "from arg.GUI import argGui; argGui.main()"`

However, this GUI needs to be configured.  
![Qt-user-settings]({{ site.baseurl }}/assets/images/Qt-user-settings.png){:width="680"}  
![Qt-ARG-settings]({{ site.baseurl }}/assets/images/Qt-ARG-settings.png){:width="680"}  
In `ARG` > `ARG settings`, four fields are required:
1. *Python executable* awaits the full path to the Python to be used to run ARG once parameters are properly configured. 
2. *Python site-packages folder* awaits the full path to `site-packages` folder corresponding to that installation of
 Python.
3. *ARG.py script* awaits the full path to the main script of ARG program. It can easily be fetched with `python -c
 "from arg.Applications, import ARG; print(ARG)"`.
4. *Latexmk processor* awaits the full path to the Latexmk installation. 

**N.B.**: If any dependency is missing, please refer to appropriate installation instructions among 
[Linux]({% link installing-on-linux.md %}), 
[macOS]({% link installing-on-macos.md %}) and 
[Windows]({% link installing-on-windows.md %}). 

## List of features covered in Python Qt GUI

This Qt GUI covers the below list of feature: 
- In `File` Menu: 
    - **Open** to loads an existing parameters file.  
        This feature also has its own icon in the Tool bar. 
    - **Open Recent** to unfold a list of recently loaded files **when** such files have already been loaded before
    . Otherwise, the list appears empty.   
        This list is currently limited to 10 elements but that limit will be editable soon. 
    - **Save** to save the current set of parameters as displayed in each tab in the loaded file **when** such file
     has been loaded during current session. Otherwise, clicking on that button leads to next feature.  
        This feature also has its own icon in the Tool bar.     
    - **Save As** to save the current set of parameters in a specific file; it is possible to change location and/or
     rename the file. 
    - **Reload** to reset every parameter to its initial value **when** a parameters file has been loaded during
     current session. Otherwise, clicking on that button has no effect.  
        This feature also has its own icon in the Tool bar.   
    - **Quit** to quit the Qt GUI. 
- In `ARG` Menu:
    - **Run** to run ARG with the current set of parameters.   
        This feature also has its own icon in the Tool bar. 
    - **Clean** to clean-up the output directory **when** 
- In `?` Menu:
    - **Help...** to provide some guidance
    - **About...** to tell you more about ARG
    
From there, every user is invited to test all existing options and parameter combinations to discover how ARG can
 help you generate reports! 

# Flask-Angular Web GUI

The Flask-Angular Web GUI is packaged as a Flask server and an Angular front-end as the name suggests. It is hence
 required to install the Flask environment on one hand, and the Angular on the other:  
![Web-report-information]({{ site.baseurl }}/assets/images/Web-report-information.png){:width="680"}  
![Web-general-options]({{ site.baseurl }}/assets/images/Web-general-options.png){:width="680"}  
![Web-data-options]({{ site.baseurl }}/assets/images/Web-data-options.png){:width="680"}  
![Web-inserts]({{ site.baseurl }}/assets/images/Web-inserts.png){:width="680"}  

## Installing the Flask-Angular Web GUI

ARG Flask-Angular GUI requires the server-side Flask environment setting:
1. Install Python dependencies: `pip install -r requirements.txt`
2. Configure the server environment: edit the `settings.yml` file in `web\api`
3. Configure local environment variables: set `FLASK_APP=$ARG_HOME\web\api`, `FLASK_ENV=development` and `FLASK_RUN_PORT
=5000`

Then to set up and build the Angular front-end environment:
1. Build Angular front-end: `ng build --prod --base-href /static/` at `$ARG_HOME\web\angular`
2. Copy generated `$ARG_HOME\web\angular\dist\ARG-GUI-angular\index.html` to `$ARG_HOME\web\api\templates`
3. Copy remaining files from `$ARG_HOME\web\angular\dist\ARG-GUI-angular` to `ARG_HOME\web\api\static`

## Running the Web GUI
It is very simple to run from here:
1. Run `python -m flask run`
2. Open `localhost:5000` in a Web browser

However, this GUI needs to be configured. Some `ARG-GUI-config.yml` should be created in your `AppData/Roaming/ARG
` folder by this step.   
This file requires four values:
1. `python_executable` awaits the full path to the Python to be used to run ARG once parameters are properly configured. 
2. `python_site_package` awaits the full path to `site-packages` folder corresponding to that installation of Python.
3. `arg_script` awaits the full path to the main script of ARG program. It can easily be fetched with `python -c
 "from arg.Applications, import ARG; print(ARG)"`.
4. `latex_processor` awaits the full path to the Latexmk installation.

**N.B.**: If any dependency is missing, please refer to appropriate installation instructions among 
[Linux]({% link installing-on-linux.md %}), 
[macOS]({% link installing-on-macos.md %}) and 
[Windows]({% link installing-on-windows.md %}). 

## List of features covered in Flask-Angular Web GUI

This Web GUI covers the below list of feature: 
- **Open** to loads an existing parameters file.  
- **Reload** to reset every parameter to its initial value **when** a parameters file has been loaded during current
 session. Otherwise, clicking on that button has no effect.   
- **Save** to save the current set of parameters as displayed in each tab in the loaded file **when** such file has
 been loaded during current session. Otherwise, clicking on that button leads to next feature.   
- **Run** to run ARG with the current set of parameters.   
- **Logger clean** to flush logs. 

More user-friendly feature such as the addition of file browser for parameters requiring file names or folder paths
 are yet to come. Also, despite running on localhost for now, it will soon be available for remote clients. 