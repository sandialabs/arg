#HEADER
#                     arg/tests/GUI_tests/test_argParameterController.py
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

import datetime
import os
import random
from unittest import TestCase

import yaml

from arg.GUI.Logic.argParameterController import argParameterController
from tests.tools import prepareParametersFile, unittest_application, unittest_signal


class TestArgParameterController(TestCase):

    def setUp(self):
        self.home_path = os.path.dirname(os.path.realpath(__file__))

        self.workingDir = os.path.join(self.home_path, "GUI_unittests")

        self.testName = "test_argParameterController"

        # Define parameters file
        self.inputFile = os.path.join(self.home_path, "input", "parameters.yml")
        self.parametersFilePath = prepareParametersFile(self.inputFile, self.workingDir, self.testName)

        self.expectedRead = {"BackendType": "LaTeX",
                             "ReportType": "Report",
                             "StructureFile": "../../../tests/GUI_tests/input/structure.yml",
                             "OutputDir": "{}".format(self.workingDir),
                             "Verbosity": 0,
                             "File Name": f"test_argParameterController{datetime.datetime.now().strftime('%Y-%m-%d')}",
                             "Final": False,
                             "Number": "-{}-{}".format(self.testName,
                                                       datetime.datetime.strftime(datetime.datetime.now(), "%Y-%m-%d"))}

        self.dataWrite = [{"a": "A", "b": "B", "c": "C", "d": "D"},
                          {"backend_type": "A", "report_type": "B", "structure": "C", "output": "D"},
                          {"backend_type": "LaTeX", "report_type": "Report", "structure": "structure.yml",
                           "output": "output"},
                          {"BackendType": "A", "ReportType": "B", "StructureFile": "C", "OutputDir": "D"},
                          {"BackendType": "LaTeX", "ReportType": "Report", "StructureFile": "structure.yml",
                           "OutputDir": "output"}]
        self.expectedWrite = [{},
                              {},
                              {},
                              {"backend_type": "A", "report_type": "B", "structure": "C.yml", "output": "D"},
                              {"backend_type": "LaTeX", "report_type": "Report", "structure": "structure.yml",
                               "output": "output"}]

        self.data = {"BackendType": "LaTeX", "ReportType": "Report", "StructureFile": "structure.yml",
                     "OutputDir": "output"}

        self.app = unittest_application.instance()
        if self.app is None:
            self.app = unittest_application()

    def test_read(self):
        """Unit test read method
        """
        # Log total content in case of difference
        self.maxDiff = None

        # Create test parameterController
        controller = argParameterController()
        controller.setSettingsController(self.app.settingsController)

        # Apply test scenario
        self.assertEqual(controller.read(self.parametersFilePath),
                         True)
        self.assertEqual(self.app.settingsController.getCurrentParameterFile(),
                         self.parametersFilePath)

    def test_write(self):
        """Unit test write method
        """

        # Log total content in case of difference
        self.maxDiff = None

        # Create test parameterController
        controller = argParameterController()
        controller.setSettingsController(self.app.settingsController)

        # Apply test scenario
        for i in range(len(self.dataWrite)):
            controller.write("{}/{}{}.yml".format(self.workingDir, self.testName, i),
                             self.dataWrite[i])
            if i == 3 or i == 4:
                with open("{}/{}{}.yml".format(self.workingDir, self.testName, i), 'r') as f:
                    self.assertDictEqual(yaml.safe_load(f),
                                         self.expectedWrite[i])
                    self.assertEqual(self.app.settingsController.getCurrentParameterFile(),
                                     "{}/{}{}.yml".format(self.workingDir, self.testName, i))
                    f.close()
            else:
                self.assertFalse(os.stat("{}/{}{}.yml".format(self.workingDir, self.testName, i)).st_size)

    def test_reload_data(self):
        """Unit test reloadData method
        """

        # Log total content in case of difference
        self.maxDiff = None

        # Create test parameterController
        controller = argParameterController()
        controller.setSettingsController(self.app.settingsController)

        # Apply test scenario

        # Check backupData is initialized empty by default
        self.assertDictEqual(controller.backupData, {})

        # Check backupData is still empty after a realoadData BEFORE any read
        controller.reloadData()
        self.assertDictEqual(controller.backupData, {})

        # Check backupData is updated after a read
        controller.read(self.parametersFilePath)
        self.assertDictEqual(controller.backupData,
                             self.expectedRead)

        # Check empty backupData is NOT updated after a write
        i = random.randint(0, len(self.dataWrite) - 1)
        controller.write("{}/unitTestParametersControllerReload.yml".format(self.workingDir),
                         self.dataWrite[i])
        self.assertNotEqual(controller.backupData,
                            self.dataWrite[i])
        self.assertDictEqual(controller.backupData,
                             self.expectedRead)

        # Clean backupData
        controller.backupData = {}
        self.assertDictEqual(controller.backupData, {})

        # Check backupData is restored after a realoadData AFTER a read
        controller.reloadData()
        self.assertDictEqual(controller.backupData, {})

    def test_on_data_created(self):
        """Unit test onDataCreated method
        """

        # Log total content in case of difference
        self.maxDiff = None

        # Create test parameterController
        controller = argParameterController()
        controller.setSettingsController(self.app.settingsController)
        handler = unittest_signal()

        # Apply test scenario
        controller.dataCreated.connect(handler.onDataReceived)
        controller.onDataCreated(self.dataWrite[4])
        self.assertEqual(handler.callCount, 1)
        self.assertDictEqual(handler.dataReceived,
                             self.data)
