#HEADER
#           arg/tests/GUI_tests/integrationtests/testSettingsController.py
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

import os
import shutil

import yaml

from arg.GUI.Logic.argSettingsController import argSettingsController
from arg.GUI.Logic.argUserSettingsReader import argUserSettingsReader
from tests.tools import sed, replaceInTemplate, unittest_application

home_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
arg_path = os.path.join(home_path, "arg")
dir_path = os.path.dirname(os.path.realpath(__file__))

prefix = "GUI_integrationtests"
app = "ARG-{}".format(prefix)
data = {"a": "A", "b": "B", "c": "C"}
testName = "testSettingsController"
workingDir = os.path.join(dir_path, prefix)

# Load supported types
with open(os.path.join(arg_path, "Common", "argTypes.yml"),
          'r',
          encoding="utf-8") as t_file:
    Types = yaml.safe_load(t_file)

# Define constants
adminLvl = os.path.join(dir_path, "input", "userSettingsAdmin.yml")
usrLvl = os.path.join(dir_path, "input", "userSettingsUsr.yml")


def main():
    """ARG GUI settingsController test main method
    """

    # Create output directory and copy input parameters file template
    os.mkdir(workingDir) if not os.path.isdir(workingDir) else False
    parametersFilePath = os.path.join(workingDir,
                                      "parameters{}.yml".format(testName[0].upper() + testName[1:]))
    shutil.copyfile(os.path.join(dir_path, "input", "parameters.yml"), parametersFilePath)

    # Substitute WORKING_DIR in copied parameters file template
    sed(parametersFilePath, "%WORKING_DIR%", workingDir)

    # Substitute DOC_NAME in copied parameters file template
    sed(parametersFilePath, "%DOC_NAME%", testName)

    # Subtitute templated values to current ones in parameters file
    date = replaceInTemplate(parametersFilePath, testName)

    # Initiate controller
    controller = argSettingsController()

    # Change controller attributes to match test environment
    controller.scriptDirectoryConfigFilePath = adminLvl
    controller.userHomeConfigFilePath = usrLvl
    controller.userSettingsReader = \
        argUserSettingsReader(controller.scriptDirectoryConfigFilePath,
                              controller.userHomeConfigFilePath)

    # Set config file path to output, initialize controller and save settings as initialized
    controller.userHomeConfigFilePath = os.path.join(workingDir, "userSettingsController.yml")
    controller.initialize()
    controller.saveSettings({"python_executable": controller.argPythonExePath,
                             "python_site_package": controller.argPythonSitePackagePath,
                             "arg_script": controller.argScriptPath,
                             "latex_processor": controller.argLatexProcessorPath})

    # Check saved content is correct
    input = yaml.safe_load(open(usrLvl, 'r'))
    output = yaml.safe_load(open(controller.userHomeConfigFilePath, 'r'))
    return input == output


if __name__ == '__main__':
    """ARG GUI settingsController test main routine
    """
    # Create test application
    app = unittest_application()
    main()
