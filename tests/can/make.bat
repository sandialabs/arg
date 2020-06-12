REM #HEADER
REM                            arg/tests/can/make.bat
REM               Automatic Report Generator (ARG) v. 1.0
REM
REM Copyright 2020 National Technology & Engineering Solutions of Sandia, LLC
REM (NTESS). Under the terms of Contract DE-NA0003525 with NTESS, the U.S.
REM Government retains certain rights in this software.
REM
REM Redistribution and use in source and binary forms, with or without
REM modification, are permitted provided that the following conditions are met:
REM
REM * Redistributions of source code must retain the above copyright notice,
REM   this list of conditions and the following disclaimer.
REM
REM * Redistributions in binary form must reproduce the above copyright notice,
REM   this list of conditions and the following disclaimer in the documentation
REM   and/or other materials provided with the distribution.
REM
REM * Neither the name of the copyright holder nor the names of its
REM   contributors may be used to endorse or promote products derived from this
REM   software without specific prior written permission.
REM
REM THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
REM AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
REM IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
REM ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
REM LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
REM CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
REM SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
REM INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
REM CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
REM ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
REM POSSIBILITY OF SUCH DAMAGE.
REM
REM Questions? Visit gitlab.com/AutomaticReportGenerator/arg
REM
REM #HEADER

@echo off
SET DOC_NAME=Report-can

IF "%1" == "clean" (
  IF NOT "%2" == "noLog" (
    echo Cleaning can test case...
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
  IF EXIST "%DOC_NAME%" (
    for /d %%x in (%DOC_NAME%) do rd /s /q "%%x"
  )
  IF EXIST "artifacts" (
    for /d %%x in (artifacts) do rd /s /q "%%x"
  )
  IF NOT "%2" == "noLog" (
    echo All can files deleted. 
  )
) ELSE (
  echo Starting generation of %DOC_NAME%...
  python.exe ..\\..\\src\\Applications\\ARG.py -g
  robocopy %DOC_NAME% . %DOC_NAME%.pdf /MOV /njh /njs /ndl /nc /ns
  echo %DOC_NAME% report generated.
)
