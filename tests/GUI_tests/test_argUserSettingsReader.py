#HEADER
#                      arg/tests/GUI_tests/test_argUserSettingsReader.py
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

from arg.GUI.Logic.argUserSettingsReader import argUserSettingsReader


class ArgUserSettingsReader(TestCase):
    """A GUI unit test class for argUserSettingsReader
    """

    def setUp(self):

        self.dir_path = os.path.dirname(os.path.realpath(__file__))

        self.keys = ["python_executable",
                     "python_site_package",
                     "arg_script",
                     "latex_processor"]
        self.expected = [["python_site_package",
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
        self.expectedAdmin = {"python_executable": "/opt/local/bin/python3.7",
                              "python_site_package": "/opt/local/Library/Frameworks/Python.framework/Versions/3.7/lib/python3.7/site-packages/",
                              "arg_script": "/opt/local/arg/arg/Applications/ARG.py",
                              "latex_processor": "/opt/local/Latex/bin"}
        self.expectedUsr = {"python_executable": "/Users/myuser/python3.7",
                            "python_site_package": "/Users/myuser/Library/Frameworks/Python.framework/Versions/3.7/lib/python3.7/site-packages/",
                            "arg_script": "/Users/myuser/arg/arg/Applications/ARG.py",
                            "latex_processor": "/Users/myuser/Latex/bin"}

        self.adminLvl = os.path.join(self.dir_path, "input/userSettingsAdmin.yml")
        self.adminLvls = [os.path.join(self.dir_path, "input/userSettingsAdmin{}.yml").format(i) for i in range(7)]
        self.usrLvl = os.path.join(self.dir_path, "input/userSettingsUsr.yml")

        self.keyValues = {"python_executable": "python",
                          "python_site_package": "python/site-packages",
                          "arg_script": "ARG.py",
                          "latex_processor": "latex",
                          "key": ""}

    def test_read(self):
        """Unit test read method
        """

        # Log total content in case of difference
        self.maxDiff = None

        # Specify admin lvl then usr lvl in constructor
        reader1 = argUserSettingsReader(self.adminLvl, self.usrLvl)
        reader1.read()

        # Expect second specified lvl by default -- usr lvl expected
        self.assertDictEqual(reader1.settings, self.expectedUsr)
        self.assertNotEqual(reader1.settings, self.expectedAdmin)

        # Specify usr lvl then admin lvl in constructor
        reader2 = argUserSettingsReader(self.usrLvl, self.adminLvl)
        reader2.read()

        # Expect second specified lvl by default -- admin lvl here
        self.assertDictEqual(reader2.settings, self.expectedAdmin)
        self.assertNotEqual(reader2.settings, self.expectedUsr)

    def test_readSettingsFile(self):
        """Unit test readSettingsFile method
        """

        # Log total content in case of difference
        self.maxDiff = None

        # Test admin lvl
        readerAdmin = argUserSettingsReader(self.adminLvl,
                                            self.usrLvl)
        self.assertDictEqual(readerAdmin.readSettingsFile(self.adminLvl),
                             self.expectedAdmin)

        # Test usr lvl
        readerUsr = argUserSettingsReader(self.adminLvl,
                                          self.usrLvl)
        self.assertDictEqual(readerUsr.readSettingsFile(self.usrLvl),
                             self.expectedUsr)

    def test_readPythonExecutable(self):
        """Unit test readPythonExecutable method
        """

        # Log total content in case of difference
        self.maxDiff = None

        # Test admin lvl
        reader = argUserSettingsReader(self.adminLvl, self.usrLvl)
        self.assertEqual(reader.readPythonExecutable(self.adminLvl),
                         self.expectedAdmin["python_executable"])

        # Test usr lvl
        reader = argUserSettingsReader(self.adminLvl, self.usrLvl)
        self.assertEqual(reader.readPythonExecutable(self.usrLvl),
                         self.expectedUsr["python_executable"])

    def test_readPythonSitePackage(self):
        """Unit test readPythonSitePackage method
        """

        # Log total content in case of difference
        self.maxDiff = None

        # Test admin lvl
        reader = argUserSettingsReader(self.adminLvl, self.usrLvl)
        self.assertEqual(reader.readPythonSitePackage(self.adminLvl),
                         self.expectedAdmin["python_site_package"])

        # Test usr lvl
        reader = argUserSettingsReader(self.adminLvl, self.usrLvl)
        self.assertEqual(reader.readPythonSitePackage(self.usrLvl),
                         self.expectedUsr["python_site_package"])

    def test_readArgScript(self):
        """Unit test readArgScript method
        """

        # Log total content in case of difference
        self.maxDiff = None

        # Test admin lvl
        reader = argUserSettingsReader(self.adminLvl, self.usrLvl)
        self.assertEqual(reader.readArgScript(self.adminLvl),
                         self.expectedAdmin["arg_script"])

        # Test usr lvl
        reader = argUserSettingsReader(self.adminLvl, self.usrLvl)
        self.assertEqual(reader.readArgScript(self.usrLvl),
                         self.expectedUsr["arg_script"])

    def test_readLatexProcessor(self):
        """Unit test readLatexProcessor method
        """

        # Log total content in case of difference
        self.maxDiff = None

        # Test admin lvl
        reader = argUserSettingsReader(self.adminLvl, self.usrLvl)
        self.assertEqual(reader.readLatexProcessor(self.adminLvl),
                         self.expectedAdmin["latex_processor"])

        # Test usr lvl
        reader = argUserSettingsReader(self.adminLvl, self.usrLvl)
        self.assertEqual(reader.readLatexProcessor(self.usrLvl),
                         self.expectedUsr["latex_processor"])

    def test_checkAllSettings(self):
        """Unit test checkAllSettings method
        """

        # Log total content in case of difference
        self.maxDiff = None

        for i in range(1):
            reader = argUserSettingsReader("{}{}".format(self.adminLvl, i),
                                           self.usrLvl)
            reader.setSetting("python_executable",
                              reader.readPythonExecutable(self.adminLvls[i]))
            reader.setSetting("python_site_package",
                              reader.readPythonSitePackage(self.adminLvls[i]))
            reader.setSetting("arg_script", reader.readArgScript(self.adminLvls[i]))
            reader.setSetting("latex_processor", reader.readLatexProcessor(self.adminLvls[i]))
            self.assertListEqual(sorted(reader.checkAllSettings()),
                                 sorted(self.expected[i]))

    def test_setSetting(self):
        """Unit test setSetting method
        """

        # Log total content in case of difference
        self.maxDiff = None

        reader = argUserSettingsReader(self.adminLvl, self.usrLvl)
        for key in self.keyValues:
            value = self.keyValues[key]
            reader.setSetting(key, value)
            if not key in self.keys:
                self.assertEqual(key in reader.settings, False)
            else:
                self.assertEqual(reader.settings[key], value)

    def test_getPythonExecutable(self):
        """Unit test getPythonExecutable method
        """

        # Log total content in case of difference
        self.maxDiff = None

        reader = argUserSettingsReader(self.adminLvl, self.usrLvl)
        reader.read()
        self.assertEqual(reader.getPythonExecutable(),
                         self.expectedUsr.get("python_executable"))

    def test_getPythonSitePackage(self):
        """Unit test getPythonSitePackage method
        """

        # Log total content in case of difference
        self.maxDiff = None

        reader = argUserSettingsReader(self.adminLvl, self.usrLvl)
        reader.read()
        self.assertEqual(reader.getPythonSitePackage(),
                         self.expectedUsr.get("python_site_package"))

    def test_getArgScript(self):
        """Unit test getArgScript method
        """

        # Log total content in case of difference
        self.maxDiff = None

        reader = argUserSettingsReader(self.adminLvl, self.usrLvl)
        reader.read()
        self.assertEqual(reader.getArgScript(),
                         self.expectedUsr.get("arg_script"))

    def test_getLatexProcessor(self):
        """Unit test getLatexProcessor method
        """

        # Log total content in case of difference
        self.maxDiff = None

        reader = argUserSettingsReader(self.adminLvl, self.usrLvl)
        reader.read()
        self.assertEqual(reader.getLatexProcessor(),
                         self.expectedUsr.get("latex_processor"))
