@ECHO off

REM This script copy angular build to be hosted by the flask server

REM to build angular application first, please run the following command
REM ng build --prod --base-href /static/


SET ng_build_dir="%~dp0..\dist\ARG-GUI-angular"
SET api_dir="%d%..\..\api"

ECHO %d%

del /s /q "%api_dir%\templates\index.html"
del /s /q "%api_dir%\static\*"

XCOPY "%ng_build_dir%\index.html" "%api_dir%\templates\" /C /S /I /F /H /Y
XCOPY "%ng_build_dir%\*.*" "%api_dir%\static\" /C /S /I /F /H /Y
del /s /q "%api_dir%\static\index.html"
