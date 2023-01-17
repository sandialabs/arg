# Eclipse RCP plugin

## Install requirements
In Eclipse, install the following features by going under "Help > Install New Software"
- Install chromium feature from http://dl.maketechnology.io/chromium-swt/rls/repository
- Install cef feature from http://dl.maketechnology.io/chromium-cef/rls/repository

## Import io.arg.webgui project

- Import io.arg.webgui as a MAVEN Project "File > Import > Maven > Existing Maven Projects"
- Browse the root directory "<arg_folder>\rcp\src\io.arg.webgui"
- Select all MAVEN projects (9 projects)
- Click Finish

Refresh the projects by right-clicking on one project then "Maven > Update project", Select all and Ok

## Work on the plugin

The "ARG web GUI view" is under the project "io.arg.webgui.plugin" > "src/main/java".

The other MAVEN projects are used to package the application into an Eclipse feature or an Eclipse update site.

## Run the plugin

Right-click the project "io.arg.webgui.plugin" then "Run As > Eclipse Application".

Another Eclipse workspace will be launched. 

In this workspace, in the top menu bar click on "Window > Show view > Other...", select ARG Web GUI. The browser will be launched.

## Package the plugin

Install MAVEN on your computer or add the Eclipse embedded MAVEN into an environment variable.

Go to the folder "<arg_folder>\rcp\src\io.arg.webgui"

Run the following command:

```
mvn clean install
```
