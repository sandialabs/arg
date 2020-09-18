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
2. *Python site-packages folder* awaits the full path to `site-packages` folder corresponding to that installation of Python.
3. *ARG.py script* awaits the full path to the main script of ARG program. It can easily be fetched with `python -c "from arg.Applications, import ARG; print(ARG)"`.
4. *Latexmk processor* awaits the full path to the Latexmk installation. 

**N.B.**: If any dependency is missing, please refer to appropriate installation instructions among [Linux]({% link installing-on-linux.md %}), [macOS]({% link installing-on-macos.md %}) and [Windows]({% link installing-on-windows.md %}. 

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
    
From there, every user is invited to test all existing options and parameter combinations to discover how ARG can help you generate reports! 

# Eclipse RCP plug-in GUI

The Eclipse RCP plug-in GUI is package as a plug-in as the name suggests. It is hence totally integrated in Eclipse IDE:  
![RCP-report-information]({{ site.baseurl }}/assets/images/RCP-report-information.png){:width="680"}  
![RCP-general-options]({{ site.baseurl }}/assets/images/RCP-general-options.png){:width="680"}  
![RCP-data-options]({{ site.baseurl }}/assets/images/RCP-data-options.png){:width="680"}  
![RCP-inserts]({{ site.baseurl }}/assets/images/RCP-inserts.png){:width="680"}  

## Installing the Eclipse RCP plug-in GUI

For now, ARG Eclipse RCP plug-in GUI needs to be downloaded [here](), and manually installed in the Eclipse IDE as follows: 
- ![RCP-install-new-software]({{ site.baseurl }}/assets/images/RCP-install-new-software.png){:width="680"}  
- ![RCP-add]({{ site.baseurl }}/assets/images/RCP-add.png){:width="680"}  
- ![RCP-archive]({{ site.baseurl }}/assets/images/RCP-archive.png){:width="680"}  
- ![RCP-archive2]({{ site.baseurl }}/assets/images/RCP-archive2.png){:width="680"}  


An easier installation process is coming soon to allow users to connect to the Market Place directly from their Eclipse IDE!

## Running the plug-in GUI

In `Window`Menu, select `Show View` then `Other`. From that list, select `ARG` and `ARG-GUI`. This opens a new view in the Eclipse IDE, displaying the first tab of ARG plug-in GUI. 

![RCP-view]({{ site.baseurl }}/assets/images/RCP-view.png){:width="680"}  
![RCP-ARGGUI]({{ site.baseurl }}/assets/images/RCP-ARGGUI.png){:width="680"}  

However, this GUI needs to be configured. Some `ARG-GUI-config.yml` should be created in your `AppData/Roaming/ARG` folder by this step.   
This file requires four values:
1. `python_executable` awaits the full path to the Python to be used to run ARG once parameters are properly configured. 
2. `python_site_package` awaits the full path to `site-packages` folder corresponding to that installation of Python.
3. `arg_script` awaits the full path to the main script of ARG program. It can easily be fetched with `python -c "from arg.Applications, import ARG; print(ARG)"`.
4. `latex_processor` awaits the full path to the Latexmk installation.

**N.B.**: If any dependency is missing, please refer to appropriate installation instructions among [Linux]({% link installing-on-linux.md %}), [macOS]({% link installing-on-macos.md %}) and [Windows]({% link installing-on-windows.md %}. Also, despite running an Eclipse RCP plug-in GUI, Python dependencies described in these installation instructions are required. 

## List of features covered in Eclipse RCP plug-in GUI

This Qt GUI covers the above list of feature: 
- **Open** to loads an existing parameters file.  
- **Reload** to reset every parameter to its initial value **when** a parameters file has been loaded during current session. Otherwise, clicking on that button has no effect.   
- **Save** to save the current set of parameters as displayed in each tab in the loaded file **when** such file has been loaded during current session. Otherwise, clicking on that button leads to next feature.   
- **Run** to run ARG with the current set of parameters.   
- **Logger clean** to flush logs. 

More user-friendly feature such as the addition of file browser for parameters requiring file names or folder paths are yet to come. 