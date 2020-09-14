# Flask-based web api providing arg operations remotely

## Install requirements
pip install -r requirements.txt

## Configure
Please edit the settings.yml file to configure the server environment

## Run
set FLASK_APP=<api_folder> && set FLASK_ENV=development && set FLASK_RUN_PORT=5000 && python -m flask run
where FLASK_APP is the path to the api folder, FLASK_ENV is either development or production, FLASK_RUN_PORT is a custom port to serve the api

## Execute the tests
Tests are currently based on the python integrated unit testing framework named **unittest**
The web Api tests are located in tests/web_api_tests
To execute the tests go to the Web Api Tests directory then run the following command `python -m unittest`.

# Make angular front end available from the flask api
Go to the arg/web/angular folder then run the following command :
ng build --prod --base-href /static/
Then copy generated files (from arg/web/angular/dist/ARG-GUI-angular) to the flask api
    index.html to arg/web/api/templates 
    other files to arg/web/api/static

## VS Code Debugging

This section is useful for debugging using Visual Studio Code.
You will need to install the Python extension for VS Code first.

### VS Code run configuration

From a Visual Studio Code launch configuration file (`launch.json`) you can define the environment variables in the "env" part of the configuration. The following is an example of a `launch.json` file specifyinf 5 Flask environment variables :
```json
 {
            "version": "0.2.0",
            "configurations": [
                {
                    "name": "Python : Flask",
                    "type": "python",
                    "request": "launch",
                    "module": "flask",
                    "env": {
                        "FLASK_APP": "web/api",
                        "FLASK_ENV": "development",
                        "FLASK_DEBUG": "1",
                        "FLASK_RUN_HOST": "localhost",
                        "FLASK_RUN_PORT": "8050"
                    },
                    "args": [
                        "run",
                        "--no-debugger",
                        "--no-reload"
                    ],
                    "jinja": false
                }
            ]
        }

```

# Eclipse RCP plugin

## Install requirements
In Eclipse, install the following features by going under "Help > Install New Software"
- Install chromium feature from http://dl.maketechnology.io/chromium-swt/rls/repository
- Install cef feature from http://dl.maketechnology.io/chromium-cef/rls/repository

## Import io.arg.webgui project
Import io.arg.webgui as a new Java Project
