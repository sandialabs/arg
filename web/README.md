This page aims to provide instructions to install ARG-GUI development environments.

[Go back to Wiki home page](home)

## Contents

[[_TOC_]]

## Overview

ARG currently has two types of GUI. Both use the same engine but do not run in the same environments. 

# Python Qt GUI

The Python GUI is coded in Qt which provides generic graphical results:  
![Qt](uploads/776b1af1520bb59145c6efc1b79ddcb4/Qt.gif)

## Installing the Qt GUI for development
On Qt, development environment does not differ much from production environment except the [repository clone part](https://gitlab.com/AutomaticReportGenerator/arg/-/wikis/Obtaining-ARG):
- clone repository as instructed [here](https://gitlab.com/AutomaticReportGenerator/arg/-/wikis/Obtaining-ARG), appending `PYTHONPATH`,
- `cd $ARG_HOME` where `ARG_HOME` is the root path where to clone the repository,
- `pip install pyARG-dep`.  

## Running the Qt GUI
As illustrated [here](https://automaticreportgenerator.gitlab.io/arg/gui-examples.html), it is quite easy to run with a single-line command:   
```
cd $ARG_HOME/arg/GUI/
python argGui.main()
```

However, this GUI also needs to be configured.  
![Qt-user-settings](uploads/40357afcdbe1b486bdea7e1bcde91444/Qt-user-settings.png)  
![Qt-ARG-settings](uploads/95c127081dc917c6dbd5001786337f97/Qt-ARG-settings.png)  
In `ARG` > `ARG settings`, four fields are required:
1. *Python executable* awaits the full path to the Python to be used to run ARG once parameters are properly configured. 
2. *Python site-packages folder* awaits the full path to `site-packages` folder corresponding to that installation of Python, appended with `ARG_HOME`. It should be close to `PYTHONPATH` as defined [here](https://gitlab.com/AutomaticReportGenerator/arg/-/wikis/arg-gui-installation#running-the-qt-gui). 
3. *ARG.py script* awaits the full path to the main script of ARG program. It should be `$ARG_HOME/arg/Applications/ARG.py`.
4. *Latexmk processor* awaits the full path to the Latexmk installation. 

**N.B.**: All paths above-listed should be extended since the settings cannot parse environment variables yet. 

## List of features covered in Python Qt GUI

This Qt GUI covers the above list of feature: 
- In `File` Menu: 
    - **Open** to loads an existing parameters file.  
        This feature also has its own icon in the Tool bar. 
    - **Open Recent** to unfold a list of recently loaded files **when** such files have already been loaded before. Otherwise, the list appears empty.   
        This list is currently limited to 10 elements but that limit will be editable soon. 
    - **Save** to save the current set of parameters as displayed in each tab in the loaded file **when** such file has been loaded during current session. Otherwise, clicking on that button leads to next feature.  
        This feature also has its own icon in the Tool bar.     
    - **Save As** to save the current set of parameters in a specific file; it is possible to change location and/or rename the file. 
    - **Reload** to reset every parameter to its initial value **when** a parameters file has been loaded during current session. Otherwise, clicking on that button has no effect.  
        This feature also has its own icon in the Tool bar.   
    - **Quit** to quit the Qt GUI. 
- In `ARG` Menu:
    - **Run** to run ARG with the current set of parameters.   
        This feature also has its own icon in the Tool bar. 
    - **Clean** to clean-up the output directory **when** 
- In `?` Menu:
    - **Help...** to provide some guidance
    - **About...** to tell you more about ARG

# Flask-Angular Web GUI

The Flask-Angular Web GUI is packaged as a Flask server and an Angular front-end as the name suggests. It is hence
 required to install the Flask environment on one hand, and the Angular on the other:  
![Web-report-information]({{ site.baseurl }}/assets/images/Web-report-information.png){:width="680"}  
![Web-general-options]({{ site.baseurl }}/assets/images/Web-general-options.png){:width="680"}  
![Web-data-options]({{ site.baseurl }}/assets/images/Web-data-options.png){:width="680"}  
![Web-inserts]({{ site.baseurl }}/assets/images/Web-inserts.png){:width="680"}  

## Installing Flask-Angular Web GUI environment for development

### Flask environment
Flask is using Python dependencies only which are all included in `requirements.txt`.  
It however needs some configuration:
- `FLASK_APP=$ARG_HOME/web/api`
- `FLASK_ENV=development`
- `FLASK_RUN_PORT=5000`. **N.B.**: This port is currently hard-coded but should be dynamically chosen soon.  

**N.B.**: They should be set whenever opening a console, and used with 
[these run instructions](https://gitlab.com/AutomaticReportGenerator/arg/-/wikis/ARG-GUI-installation/#Running-the-Web-GUI). 

### Angular environment 
- install [npm](https://nodejs.org/dist/latest/)
- `npm install -g @angular/cli`
- `npm install --save-dev @angular-devkit/build-angular`
- `npm install file-saver --save`
- `npm install typescript`
- `npm install @angular/compiler`
- `npm install @angular/compiler-cli`

## Building the Angular front-end app
- `cd $ARG_HOME/web/angular`
- `ng build --prod --base-href /static/`. This should generate a `dist/` folder in `$ARG_HOME/web/angular/`
- `cd $ARG_HOME/web`
- `cp angular/dist/ARG-GUI-angular/index.html api/templates`
- Copy all remaining files from `angular/dist/ARG-GUI-angular` to `api/static`

## Running the Web GUI
1. Run `python -m flask run`
2. Open `localhost:5000` in a Web browser

## List of features covered in Flask-Angular plWeb GUI

This Web GUI covers the above list of feature: 
- **Open** to loads an existing parameters file.  
- **Reload** to reset every parameter to its initial value **when** a parameters file has been loaded during current session. Otherwise, clicking on that button has no effect.   
- **Save** to save the current set of parameters as displayed in each tab in the loaded file **when** such file has been loaded during current session. Otherwise, clicking on that button leads to next feature.   
- **Run** to run ARG with the current set of parameters.   
- **Logger clean** to flush logs.   
**N.B.**: The Web GUI runs on localhost server only. A remote client is planned for upcoming releases. 