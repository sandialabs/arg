#HEADER
#                     arg/tests/GUI_tests/test_argParameterWriter.py
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
import unittest
from unittest import TestCase

import yaml

from arg.GUI.Logic.argParameterWriter import argParameterWriter
from tests.tools import unittest_application


class TestArgParameterWriter(TestCase):

    def setUp(self):
        self.home_path = os.path.dirname(os.path.realpath(__file__))

        self.workingDir = os.path.join(self.home_path, "GUI_unittests")
        self.testName = "test_argParameterWriter"

        """A GUI unit test class for argParameterWriter
        """

        self.data = [{"a": "A", "b": "B", "c": "C", "d": "D"},
                     {"backend_type": "A", "report_type": "B", "structure": "C", "output": "D"},
                     {"backend_type": "LaTeX", "report_type": "Report", "structure": "structure.yml",
                      "output": "output"},
                     {"BackendType": "A", "ReportType": "B", "StructureFile": "C", "OutputDir": "D"},
                     {"BackendType": "LaTeX", "ReportType": "Report", "StructureFile": "structure.yml",
                      "OutputDir": "output"}]

        self.expected = [{},
                         {},
                         {},
                         {"backend_type": "A", "report_type": "B", "structure": "C.yml", "output": "D"},
                         {"backend_type": "LaTeX", "report_type": "Report", "structure": "structure.yml",
                          "output": "output"}]

        self.app = unittest_application.instance()
        if self.app is None:
            self.app = unittest_application()

    def test_setData(self):
        """Unit test setData method
        """

        # Log total content in case of difference
        self.maxDiff = None

        writer = argParameterWriter()
        for i in range(len(self.data)):
            writer.setData(self.data[i])
            self.assertDictEqual(writer.ParameterData.Dict, self.data[i])

    def test_write(self):
        """Unit test write method
        """

        # Log total content in case of difference
        self.maxDiff = None

        if not os.path.exists(self.workingDir):
            os.mkdir(self.workingDir)

        writer = argParameterWriter()
        for i in range(len(self.data)):
            writer.setData(self.data[i])
            writer.write("{}/{}{}.yml".format(self.workingDir, self.testName, i))
            if i == 3 or i == 4:
                with open("{}/{}{}.yml".format(self.workingDir, self.testName, i), 'r') as f:
                    self.assertDictEqual(yaml.safe_load(f), self.expected[i])
                    f.close()
            else:
                self.assertFalse(os.stat("{}/{}{}.yml".format(self.workingDir, self.testName, i)).st_size)


if __name__ == '__main__':
    unittest.main()
