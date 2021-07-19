#HEADER
#                           arg/tests/tools.py
#               Automatic Report Generator (ARG) v. 1.0
#
# Copyright 2020 National Technology & Engineering Solutions of Sandia, LLC
# (NTESS). Under the terms of Contract DE-NA0003525 with NTESS, the U.S.
# Government retains certain rights in this software.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# * Redistributions of source code must retain the above copyright notice,
#   this list of conditions and the following disclaimer.
#
# * Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.
#
# * Neither the name of the copyright holder nor the names of its
#   contributors may be used to endorse or promote products derived from this
#   software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
#
# Questions? Visit gitlab.com/AutomaticReportGenerator/arg
#
#HEADER

############################################################################
app = "ARG-GUI_unittests"

############################################################################
# Import python packages
import datetime
import os
import pathlib
import shutil

# Import GUI packages
from PySide2.QtCore import Slot
from PySide2.QtWidgets import QApplication

# Add home and tests paths
if not __package__:
    home_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
else:
    home_path = os.path.realpath(".")
# arg_path = os.path.join(home_path, "arg")
# sys.path.append(home_path)
# sys.path.append(arg_path)

# Import ARG-GUI modules
from arg.GUI.Logic.argSettingsController import argSettingsController
from arg.GUI.Logic.argParameterController import argParameterController


############################################################################
class unittest_application(QApplication):
    """A GUI application test tool class
    """

    def __init__(self):
        super(unittest_application, self).__init__()
        self.settingsController = argSettingsController()
        self.settingsController.initialize()

    ########################################################################
    # def __init__(self, workingDir, testName):
    #     super(unittest_application, self).__init__()
    #     self.settingsController = argSettingsController()
    #
    #     # Create output directory and copy input parameters file template
    #     os.mkdir(workingDir) if not os.path.isdir(workingDir) else False
    #     inputFile = os.path.join(home_path, "tests", "GUI_tests", "input", "parameters.yml")
    #     self.parametersFilePath = prepareParametersFile(inputFile, workingDir, testName)


############################################################################
class unittest_signal(object):
    """A GUI signal test tool class
    """

    ########################################################################
    def __init__(self):
        self.callCount = 0

    ########################################################################
    @Slot(dict)
    def onDataReceived(self, data):
        self.callCount += 1
        self.dataReceived = data


############################################################################
def sed(fileName, str1, str2):
    """Python wrapper of sed method
    """

    # Open file in read mode
    f = open(fileName, "rt")

    # Read all file
    data = f.read()

    # Replace str1 by str2 in read data
    data = data.replace(str1, str2)

    # Close file
    f.close()

    # Open file in write mode
    f = open(fileName, "wt")

    # Dump modified data
    f.write(data)

    # Close file
    f.close()


############################################################################
def replaceInTemplate(filePath, testName):
    """Replace date and test name in templated parameters file
    """

    # Get timestamp
    date = datetime.datetime.strftime(datetime.datetime.now(), "%Y-%m-%d")

    # Substitute template DATE and TEST_NAME values in parameters file
    sed(filePath, "%DATE%", date)
    sed(filePath, "%TEST_NAME%", testName)

    return date


############################################################################
def prepareParametersFile(fromFile, workingDir, testName):
    """Prepare parameters file based on provided template and return path
    """

    # Create working folder
    if not os.path.exists(workingDir):
        os.mkdir(workingDir)

    # Define parametersFilePath based on provided workingDir and testName
    parametersFilePath = os.path.join(workingDir,
                                      "parameters{}.yml".format(testName[0].upper() + testName[1:]))
    shutil.copyfile(fromFile, parametersFilePath)

    # Subtitute templated values to current ones in parameters file
    date = replaceInTemplate(parametersFilePath, testName)

    # Substitute WORKING_DIR in copied parameters file template
    sed(parametersFilePath, "%WORKING_DIR%", workingDir)

    # Substitute DOC_NAME in copied parameters file template
    sed(parametersFilePath, "%DOC_NAME%", testName + date)

    # Return parametersFilePath
    return parametersFilePath


############################################################################
def clean(prefix):
    """ARG GUI unit tests cleaning routine
    """
    files_to_remove = list(pathlib.Path(".").rglob("{}-*".format(prefix)))
    not_remove_expected = [str(file) for file in files_to_remove if 'expected' not in str(file)]
    # Delete former results
    for p in not_remove_expected:
        print(p)
        if os.path.isdir(p):
            try:
                shutil.rmtree(p, ignore_errors=True)
            except:
                pass
        elif os.path.isfile(p):
            os.remove(p)

    # Delete any existing .tmp file
    for p in pathlib.Path(".").rglob("*.tmp"):
        print(p)
        if os.path.isdir(p):
            try:
                shutil.rmtree(p, ignore_errors=True)
            except:
                pass
        elif os.path.isfile(p):
            os.remove(p)
