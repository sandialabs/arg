@echo off
SET DOC_NAME=Report-crush

IF "%1" == "clean" (
  IF NOT "%2" == "noLog" (
    echo Cleaning crush test case...
  )
  IF EXIST "*.tmp" (
    del *.tmp
  )
  IF EXIST "%DOC_NAME%.pdf" (
    del %DOC_NAME%.pdf
  )
  IF EXIST "mutables.yml" (
    del mutables.yml
  )
  IF EXIST "%DOC_NAME%.yml" (
    del %DOC_NAME%.yml
  )
  IF EXIST "%DOC_NAME%" (
    for /d %%x in (%DOC_NAME%) do rd /s /q "%%x"
  )
  IF EXIST "crush_from_log.inp" (
    del crush_from_log.inp
  )
  IF NOT "%2" == "noLog" (
    echo All crush files deleted.
  )
) ELSE (
  echo Starting generation of %DOC_NAME%...
  python.exe ..\\..\\arg\\Applications\\ARG.py -e
  robocopy %DOC_NAME% . %DOC_NAME%.pdf /MOV /njh /njs /ndl /nc /ns
  echo %DOC_NAME% report generated. 
)
