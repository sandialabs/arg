#HEADER
#                     arg/tests/GUI_tests/test_argParameterReader.py
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
from unittest import TestCase

from arg.GUI.Logic.argParameterReader import argParameterReader
from tests.tools import prepareParametersFile, unittest_application


class TestArgParameterReader(TestCase):

    def setUp(self):
        self.home_path = os.path.dirname(os.path.realpath(__file__))

        self.workingDir = os.path.join(self.home_path, "GUI_unittests")
        self.testName = "test_argParameterReader"

        """A GUI unit test class for argParameterReader
        """

        # Define parameters file
        self.inputFile = os.path.join(self.home_path, "input", "parameters.yml")
        self.parametersFilePath = prepareParametersFile(self.inputFile, self.workingDir, self.testName)

        self.expected = {"BackendType": "LaTeX",
                         "File Name": f"test_argParameterReader{datetime.datetime.now().strftime('%Y-%m-%d')}",
                         "ReportType": "Report",
                         "StructureFile": "../../../tests/GUI_tests/input/structure.yml",
                         "OutputDir": "{}".format(self.workingDir),
                         "Verbosity": 0,
                         "Final": False,
                         "Number": "-{}-{}".format(self.testName,
                                                   datetime.datetime.strftime(datetime.datetime.now(), "%Y-%m-%d"))}

        self.app = unittest_application.instance()
        if self.app is None:
            self.app = unittest_application()

    def test_verbosity_to_int(self):
        """Unit test all values on verbosity_to_int method
        """

        # Log total content in case of difference
        self.maxDiff = None

        reader = argParameterReader()
        self.assertEqual(reader.verbosity_to_int("verbose"), 1)
        self.assertEqual(reader.verbosity_to_int("default"), 0)
        self.assertEqual(reader.verbosity_to_int("terse"), -1)
        self.assertEqual(reader.verbosity_to_int("test"), 0)

    def test_read(self):
        """Unit test read method
        """

        # Log total content in case of difference
        self.maxDiff = None

        reader = argParameterReader()
        reader.read(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                 self.parametersFilePath))
        self.assertDictEqual(reader.ParameterData.Dict,
                             self.expected)
