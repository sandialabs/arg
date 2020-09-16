#HEADER
#          arg/tests/GUI_tests/test_argSettingsController.py
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
from unittest import TestCase

import yaml

from arg.GUI.Logic.argSettingsController import argSettingsController
from arg.GUI.Logic.argUserSettingsReader import argUserSettingsReader
from tests.tools import unittest_application


class TestArgSettingsController(TestCase):
    """A GUI unit test class for argSettingsController
    """

    def setUp(self):
        self.home_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        self.arg_path = os.path.join(self.home_path, "arg")

        self.prefix = "GUI_unittests"
        self.app = "ARG-{}".format(self.prefix)
        self.dir_path = os.path.dirname(os.path.realpath(__file__))
        self.workingDir = os.path.join(self.dir_path, self.prefix)
        self.testName = "test_argSettingsController"

        self.expected = {"python_executable": "/Users/myuser/python3.7",
                         "python_site_package": "/Users/myuser/Library/Frameworks/Python.framework/Versions/3.7/lib/python3.7/site-packages/",
                         "arg_script": "/Users/myuser/arg/arg/Applications/ARG.py",
                         "latex_processor": "/Users/myuser/Latex/bin"}
        self.expectedMissings = [["python_site_package",
                                  "arg_script",
                                  "latex_processor"],
                                 ["python_executable",
                                  "arg_script",
                                  "latex_processor"],
                                 ["latex_processor"],
                                 ["latex_processor"],
                                 ["latex_processor"],
                                 ["python_executable",
                                  "python_site_package",
                                  "arg_script"],
                                 ["python_executable",
                                  "python_site_package",
                                  "arg_script",
                                  "latex_processor"]]

        self.data = {"python_executable": "python",
                     "python_site_package": "python/site-packages",
                     "arg_script": "ARG.py",
                     "latex_processor": "latex"}
        self.expectedSettings = {"BackendType": ["Backend", True],
                                 "ReportType": ["Report Type", True],
                                 "Classification": ["Classification", True],
                                 "File Name": ["File Name", False],
                                 "Mutables": ["Mutables File", False],
                                 "StructureFile": ["Structure File", False],
                                 "StructureEnd": ["Analyst Authored Results Section", False],
                                 "ArtifactFile": ["Artifact File", False],
                                 "OutputDir": ["Output Folder", True],
                                 "Verbosity": ["Verbosity", False],
                                 "Title": ["Title", False],
                                 "Number": ["Number", False],
                                 "Issue": ["Issue", False],
                                 "Versions": ["Versions", False],
                                 "Authors": ["Authors", False],
                                 "Organizations": ["Organizations", False],
                                 "Location": ["Location", False],
                                 "Year": ["Year", False],
                                 "Month": ["Month", False],
                                 "AbstractFile": ["Abstract File", False],
                                 "Preface": ["Preface", False],
                                 "Thanks": ["Thanks", False],
                                 "ExecutiveSummary": ["Executive Summary", False],
                                 "Nomenclature": ["Nomenclature", False],
                                 "Final": ["Final", False],
                                 "KeySeparator": ["Key Separator", False],
                                 "DataDirectory": ["Model Directory", False],
                                 "DeckRoot": ["Input Deck", False],
                                 "GeometryRoot": ["Geometry Root", False],
                                 "ReportedCadMetaData": ["Reported CAD Metadata", False],
                                 "LogFile": ["Log File", False],
                                 "IgnoredBlockKeys": ["Ignored Blocks", False],
                                 "Mappings": ["Bijective Mapping", False],
                                 "CAD_to_FEM": ["CAD to FEM", False],
                                 "FEM_to_CAD": ["FEM to CAD", False]}
        self.app = unittest_application.instance()
        if self.app is None:
            self.app = unittest_application()

    def test_init(self):
        """Unit test __init__ contructor
        """

        # Log total content in case of difference
        self.maxDiff = None

        # Set APPDATA environment variable to specific path for test
        appData_path = os.path.join(self.home_path, "APPDATA")
        os.environ["APPDATA"] = appData_path

        # Create test parameterController
        controller1 = argSettingsController()

        # Check initialized values
        self.assertEqual(controller1.scriptDirectory.lower(),
                         os.path.join(self.arg_path, "GUI", "Logic").lower())
        self.assertEqual(controller1.scriptDirectoryConfigFilePath.lower(),
                         os.path.join(self.arg_path, "GUI", "Logic", "ARG-GUI-config.yml").lower())
        self.assertEqual(controller1.homePath.lower(),
                         appData_path.lower())
        self.assertEqual(controller1.userHomeConfigFilePath.lower(),
                         os.path.join(appData_path, "ARG", "ARG-GUI-config.yml").lower())

        # Delete APPDATA environment variable
        # and HOME environment vairable to self.home_path for test
        os.environ.pop("APPDATA", None)
        os.environ["HOME"] = self.home_path

        # Create new test parameterController
        controller2 = argSettingsController()

        # Check initialized values
        self.assertEqual(controller2.scriptDirectory.lower(),
                         os.path.join(self.arg_path, "GUI", "Logic").lower())
        self.assertEqual(controller2.scriptDirectoryConfigFilePath.lower(),
                         os.path.join(self.arg_path, "GUI", "Logic", "ARG-GUI-config.yml").lower())
        self.assertEqual(controller2.homePath.lower(),
                         self.home_path.lower())
        self.assertEqual(controller2.userHomeConfigFilePath.lower(),
                         os.path.join(self.home_path, "ARG", "ARG-GUI-config.yml").lower())

    def test_initialize(self):
        """Unit test initialize method
        """

        # Log total content in case of difference
        self.maxDiff = None

        # Set APPDATA environment variable to specific path for test
        os.environ["APPDATA"] = os.path.join(self.home_path, "GUI/GUI_tests/input")

        # Create test parameterController
        controllerEmpty = argSettingsController()
        controller = argSettingsController()
        controller0 = argSettingsController()

        # Apply test scenario

        # Test initialization on empty controller
        controllerEmpty.initialize()
        self.assertEqual(controllerEmpty.settings,
                         self.expectedSettings)

        # Tests initialization on set up controllers
        for i in range(len(self.expectedMissings)):
            # Change controller attributes to match test environment
            controller.scriptDirectoryConfigFilePath = os.path.join(self.home_path,
                                                                    "tests/GUI_tests/input/userSettingsAdmin{}.yml".format(
                                                                        i))
            controller.userHomeConfigFilePath = os.path.join(self.home_path,
                                                             "tests/GUI_tests/input/userSettingsUsr.yml")
            controller.userSettingsReader = \
                argUserSettingsReader(controller.scriptDirectoryConfigFilePath, controller.userHomeConfigFilePath)
            self.assertEqual(controller.initialize(), None)
            self.assertEqual(controller.argPythonExePath, self.expected["python_executable"])
            self.assertEqual(controller.argPythonSitePackagePath, self.expected["python_site_package"])
            self.assertEqual(controller.argScriptPath, self.expected["arg_script"])
            self.assertEqual(controller.argLatexProcessorPath, self.expected["latex_processor"])
            self.assertEqual(controller.settings, self.expectedSettings)

            # Change controller attributes to match test environment
            controller0.scriptDirectoryConfigFilePath = os.path.join(self.home_path,
                                                                     "tests/GUI_tests/input/userSettingsAdmin{}.yml".format(
                                                                         i))
            controller0.userHomeConfigFilePath = os.path.join(self.home_path,
                                                              "tests/GUI_tests/input/userSettingsUsr0.yml")
            controller0.userSettingsReader = \
                argUserSettingsReader(controller0.scriptDirectoryConfigFilePath, controller0.userHomeConfigFilePath)
            self.assertEqual(sorted(controller0.initialize()), sorted(self.expectedMissings[i]))
            self.assertEqual(controller0.argPythonExePath, None)
            self.assertEqual(controller0.argPythonSitePackagePath, None)
            self.assertEqual(controller0.argScriptPath, None)
            self.assertEqual(controller0.argLatexProcessorPath, None)
            self.assertDictEqual(controller0.settings,
                                 self.expectedSettings)

    def test_initializeUserSettings(self):
        """Unit test initializeUserSettings method
        """

        # Log total content in case of difference
        self.maxDiff = None

        # Set APPDATA environment variable to specific path for test
        os.environ["APPDATA"] = os.path.join(self.home_path, "GUI/GUI_tests/input")

        # Create test parameterController
        controller = argSettingsController()
        controller0 = argSettingsController()

        # Apply test scenario
        for i in range(len(self.expectedMissings)):
            # Change controller attributes to match test environment
            controller.scriptDirectoryConfigFilePath = os.path.join(self.home_path,
                                                                    "tests/GUI_tests/input/userSettingsAdmin{}.yml".format(
                                                                        i))
            controller.userHomeConfigFilePath = os.path.join(self.home_path,
                                                             "tests/GUI_tests/input/userSettingsUsr.yml")
            controller.userSettingsReader = \
                argUserSettingsReader(controller.scriptDirectoryConfigFilePath, controller.userHomeConfigFilePath)
            self.assertEqual(controller.initializeUserSettings(), None)
            self.assertEqual(controller.argPythonExePath, self.expected["python_executable"])
            self.assertEqual(controller.argPythonSitePackagePath, self.expected["python_site_package"])
            self.assertEqual(controller.argScriptPath, self.expected["arg_script"])
            self.assertEqual(controller.argLatexProcessorPath, self.expected["latex_processor"])

            # Change controller attributes to match test environment
            controller0.scriptDirectoryConfigFilePath = os.path.join(self.home_path,
                                                                     "tests/GUI_tests/input/userSettingsAdmin{}.yml".format(
                                                                         i))
            controller0.userHomeConfigFilePath = os.path.join(self.home_path,
                                                              "tests/GUI_tests/input/userSettingsUsr0.yml")
            controller0.userSettingsReader = \
                argUserSettingsReader(controller0.scriptDirectoryConfigFilePath, controller0.userHomeConfigFilePath)
            self.assertEqual(sorted(controller0.initializeUserSettings()), sorted(self.expectedMissings[i]))
            self.assertEqual(controller0.argPythonExePath, None)
            self.assertEqual(controller0.argPythonSitePackagePath, None)
            self.assertEqual(controller0.argScriptPath, None)
            self.assertEqual(controller0.argLatexProcessorPath, None)

    def test_saveSettings(self):
        """Unit test saveSettings method
        """

        # Log total content in case of difference
        self.maxDiff = None

        # Set APPDATA environment variable to specific path for test
        os.environ["APPDATA"] = os.path.join(self.home_path, "GUI/GUI_tests/input")

        # Create test parameterController
        controller = argSettingsController()
        controller.userHomeConfigFilePath = os.path.join(self.workingDir, "userSettingsController.yml")

        controller.argPythonExePath = "python"
        controller.argPythonSitePackagePath = "python/site-packages"
        controller.argScriptPath = "ARG.py"
        controller.argLatexProcessorPath = "latex"

        # Apply tests scenario
        controller.saveSettings(self.data)
        self.assertEqual(controller.argPythonExePath,
                         self.data.get("python_executable", None))
        self.assertEqual(controller.argPythonSitePackagePath,
                         self.data.get("python_site_package", None))
        self.assertEqual(controller.argScriptPath,
                         self.data.get("arg_script", None))
        self.assertEqual(controller.argLatexProcessorPath,
                         self.data.get("latex_processor", None))
        with open("{}/userSettingsController.yml".format(self.workingDir), 'r') as f:
            self.assertDictEqual(yaml.safe_load(f), self.data)
            f.close()
