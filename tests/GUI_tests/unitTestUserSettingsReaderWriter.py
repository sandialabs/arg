#HEADER
#                      arg/tests/GUI_tests.py
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
prefix     = "GUI_unittests"
app        = "ARG-{}".format(prefix)
workingDir = prefix
testName   = "unitTestUserSettingsReaderWriter"

############################################################################
# Import python packages
import os, sys, unittest, yaml

# Add home path
if not __package__:
    home_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
else:
    home_path = os.path.realpath("../..")
home_path.lower() not in [path.lower() for path in sys.path] \
    and sys.path.append(home_path)

# Import ARG modules
from arg.GUI.argUserSettingsReader      import argUserSettingsReader
from arg.GUI.argUserSettingsWriter      import argUserSettingsWriter

############################################################################
class argUserSettingsReader_unittest(unittest.TestCase):
    """A GUI unit test class for argUserSettingsReader
    """

    keys          = ["python_executable",
                     "python_site_package",
                     "arg_script",
                     "paraview_site_package",
                     "paraview_libs",
                     "latex_processor"]
    expected      = [["python_site_package",
                      "arg_script",
                      "paraview_site_package",
                      "paraview_libs",
                      "latex_processor"],
                     ["python_executable",
                      "arg_script",
                      "paraview_site_package",
                      "paraview_libs",
                      "latex_processor"],
                     ["paraview_site_package",
                      "paraview_libs",
                      "latex_processor"],
                     ["paraview_libs",
                      "latex_processor"],
                     ["latex_processor"],
                     ["python_executable",
                      "python_site_package",
                      "arg_script",
                      "paraview_site_package",
                      "paraview_libs"],
                     ["python_executable",
                      "python_site_package",
                      "arg_script",
                      "paraview_site_package",
                      "paraview_libs",
                      "latex_processor"]]
    expectedAdmin = {"python_executable":"/opt/local/bin/python3.7",
                     "python_site_package":"/opt/local/Library/Frameworks/Python.framework/Versions/3.7/lib/python3.7/site-packages/",
                     "arg_script":"/opt/local/arg/arg/Applications/ARG.py",
                     "paraview_site_package":"/opt/local/paraview-install/lib/python3.7/site-packages/",
                     "paraview_libs":"/opt/local/paraview-install/lib",
                     "latex_processor":"/opt/local/Latex/bin"}
    expectedUsr   = {"python_executable":"/Users/myuser/python3.7",
                     "python_site_package":"/Users/myuser/Library/Frameworks/Python.framework/Versions/3.7/lib/python3.7/site-packages/",
                     "arg_script":"/Users/myuser/arg/arg/Applications/ARG.py",
                     "paraview_site_package":"/Users/myuser/paraview-install/lib/python3.7/site-packages/",
                     "paraview_libs":"/Users/myuser/paraview-install/lib",
                     "latex_processor":"/Users/myuser/Latex/bin"}
    adminLvl      = "input/userSettingsAdmin.yml"
    adminLvls     = ["input/userSettingsAdmin{}.yml".format(i) for i in range(7)]
    usrLvl        = "input/userSettingsUsr.yml"

    keyValues     = {"python_executable":"python",
                     "python_site_package":"python/site-packages",
                     "arg_script":"ARG.py",
                     "paraview_site_package":"paraview",
                     "paraview_libs":"paraview/lib",
                     "latex_processor":"latex",
                     "key":""}

    ########################################################################
    def test_read(self):
        """Unit test read method
        """

        # Log total content in case of difference
        self.maxDiff = None

        # Specify admin lvl then usr lvl in constructor
        reader1 = argUserSettingsReader(argUserSettingsReader_unittest.adminLvl, argUserSettingsReader_unittest.usrLvl)
        reader1.read()
        # Expect second specified lvl by default -- usr lvl expected
        self.assertDictEqual(reader1.settings, argUserSettingsReader_unittest.expectedUsr)
        self.assertNotEqual(reader1.settings, argUserSettingsReader_unittest.expectedAdmin)

        # Specify usr lvl then admin lvl in constructor
        reader2 = argUserSettingsReader(argUserSettingsReader_unittest.usrLvl, argUserSettingsReader_unittest.adminLvl)
        reader2.read()
        # Expect second specified lvl by default -- admin lvl here
        self.assertDictEqual(reader2.settings, argUserSettingsReader_unittest.expectedAdmin)
        self.assertNotEqual(reader2.settings, argUserSettingsReader_unittest.expectedUsr)

    ########################################################################
    def test_readSettingsFile(self):
        """Unit test readSettingsFile method
        """

        # Log total content in case of difference
        self.maxDiff = None

        # Test admin lvl
        readerAdmin = argUserSettingsReader(argUserSettingsReader_unittest.adminLvl, argUserSettingsReader_unittest.usrLvl)
        self.assertDictEqual(readerAdmin.readSettingsFile(argUserSettingsReader_unittest.adminLvl),
                            argUserSettingsReader_unittest.expectedAdmin)

        # Test usr lvl
        readerUsr = argUserSettingsReader(argUserSettingsReader_unittest.adminLvl, argUserSettingsReader_unittest.usrLvl)
        self.assertDictEqual(readerUsr.readSettingsFile(argUserSettingsReader_unittest.usrLvl),
                            argUserSettingsReader_unittest.expectedUsr)

    ########################################################################
    def test_readPythonExecutable(self):
        """Unit test readPythonExecutable method
        """

        # Log total content in case of difference
        self.maxDiff = None

        # Test admin lvl
        reader = argUserSettingsReader(argUserSettingsReader_unittest.adminLvl, argUserSettingsReader_unittest.usrLvl)
        self.assertEqual(reader.readPythonExecutable(argUserSettingsReader_unittest.adminLvl),
                         argUserSettingsReader_unittest.expectedAdmin["python_executable"])

        # Test usr lvl
        reader = argUserSettingsReader(argUserSettingsReader_unittest.adminLvl, argUserSettingsReader_unittest.usrLvl)
        self.assertEqual(reader.readPythonExecutable(argUserSettingsReader_unittest.usrLvl),
                         argUserSettingsReader_unittest.expectedUsr["python_executable"])

    ########################################################################
    def test_readPythonSitePackage(self):
        """Unit test readPythonSitePackage method
        """

        # Log total content in case of difference
        self.maxDiff = None

        # Test admin lvl
        reader = argUserSettingsReader(argUserSettingsReader_unittest.adminLvl, argUserSettingsReader_unittest.usrLvl)
        self.assertEqual(reader.readPythonSitePackage(argUserSettingsReader_unittest.adminLvl),
                         argUserSettingsReader_unittest.expectedAdmin["python_site_package"])

        # Test usr lvl
        reader = argUserSettingsReader(argUserSettingsReader_unittest.adminLvl, argUserSettingsReader_unittest.usrLvl)
        self.assertEqual(reader.readPythonSitePackage(argUserSettingsReader_unittest.usrLvl),
                         argUserSettingsReader_unittest.expectedUsr["python_site_package"])

    ########################################################################
    def test_readArgScript(self):
        """Unit test readArgScript method
        """

        # Log total content in case of difference
        self.maxDiff = None

        # Test admin lvl
        reader = argUserSettingsReader(argUserSettingsReader_unittest.adminLvl, argUserSettingsReader_unittest.usrLvl)
        self.assertEqual(reader.readArgScript(argUserSettingsReader_unittest.adminLvl),
                         argUserSettingsReader_unittest.expectedAdmin["arg_script"])

        # Test usr lvl
        reader = argUserSettingsReader(argUserSettingsReader_unittest.adminLvl, argUserSettingsReader_unittest.usrLvl)
        self.assertEqual(reader.readArgScript(argUserSettingsReader_unittest.usrLvl),
                         argUserSettingsReader_unittest.expectedUsr["arg_script"])

    ########################################################################
    def test_readParaviewSitePackage(self):
        """Unit test readParaviewSitePackage method
        """

        # Log total content in case of difference
        self.maxDiff = None

        # Test admin lvl
        reader = argUserSettingsReader(argUserSettingsReader_unittest.adminLvl, argUserSettingsReader_unittest.usrLvl)
        self.assertEqual(reader.readParaviewSitePackage(argUserSettingsReader_unittest.adminLvl),
                         argUserSettingsReader_unittest.expectedAdmin["paraview_site_package"])

        # Test usr lvl
        reader = argUserSettingsReader(argUserSettingsReader_unittest.adminLvl, argUserSettingsReader_unittest.usrLvl)
        self.assertEqual(reader.readParaviewSitePackage(argUserSettingsReader_unittest.usrLvl),
                         argUserSettingsReader_unittest.expectedUsr["paraview_site_package"])

    ########################################################################
    def test_readParaviewLibraries(self):
        """Unit test readParaviewLibraries method
        """

        # Log total content in case of difference
        self.maxDiff = None

        # Test admin lvl
        reader = argUserSettingsReader(argUserSettingsReader_unittest.adminLvl, argUserSettingsReader_unittest.usrLvl)
        self.assertEqual(reader.readParaviewLibraries(argUserSettingsReader_unittest.adminLvl),
                         argUserSettingsReader_unittest.expectedAdmin["paraview_libs"])

        # Test usr lvl
        reader = argUserSettingsReader(argUserSettingsReader_unittest.adminLvl, argUserSettingsReader_unittest.usrLvl)
        self.assertEqual(reader.readParaviewLibraries(argUserSettingsReader_unittest.usrLvl),
                         argUserSettingsReader_unittest.expectedUsr["paraview_libs"])

    ########################################################################
    def test_readLatexProcessor(self):
        """Unit test readLatexProcessor method
        """

        # Log total content in case of difference
        self.maxDiff = None

        # Test admin lvl
        reader = argUserSettingsReader(argUserSettingsReader_unittest.adminLvl, argUserSettingsReader_unittest.usrLvl)
        self.assertEqual(reader.readLatexProcessor(argUserSettingsReader_unittest.adminLvl),
                         argUserSettingsReader_unittest.expectedAdmin["latex_processor"])

        # Test usr lvl
        reader = argUserSettingsReader(argUserSettingsReader_unittest.adminLvl, argUserSettingsReader_unittest.usrLvl)
        self.assertEqual(reader.readLatexProcessor(argUserSettingsReader_unittest.usrLvl),
                         argUserSettingsReader_unittest.expectedUsr["latex_processor"])

    ########################################################################
    def test_checkAllSettings(self):
        """Unit test checkAllSettings method
        """

        # Log total content in case of difference
        self.maxDiff = None

        for i in range(1):
            reader = argUserSettingsReader("{}{}".format(argUserSettingsReader_unittest.adminLvl, i),
                                           argUserSettingsReader_unittest.usrLvl)
            reader.setSetting("python_executable", reader.readPythonExecutable(argUserSettingsReader_unittest.adminLvls[i]))
            reader.setSetting("python_site_package", reader.readPythonSitePackage(argUserSettingsReader_unittest.adminLvls[i]))
            reader.setSetting("arg_script", reader.readArgScript(argUserSettingsReader_unittest.adminLvls[i]))
            reader.setSetting("paraview_site_package", reader.readParaviewSitePackage(argUserSettingsReader_unittest.adminLvls[i]))
            reader.setSetting("paraview_libs", reader.readParaviewLibraries(argUserSettingsReader_unittest.adminLvls[i]))
            reader.setSetting("latex_processor", reader.readLatexProcessor(argUserSettingsReader_unittest.adminLvls[i]))
            self.assertListEqual(sorted(reader.checkAllSettings()),
                                 sorted(argUserSettingsReader_unittest.expected[i]))

    ########################################################################
    def test_setSetting(self):
        """Unit test setSetting method
        """

        # Log total content in case of difference
        self.maxDiff = None

        reader = argUserSettingsReader(argUserSettingsReader_unittest.adminLvl,
                                       argUserSettingsReader_unittest.usrLvl)
        for key in argUserSettingsReader_unittest.keyValues:
            value = argUserSettingsReader_unittest.keyValues[key]
            reader.setSetting(key, value)
            if not key in argUserSettingsReader_unittest.keys:
                self.assertEqual(key in reader.settings, False)
            else:
                self.assertEqual(reader.settings[key], value)


    ########################################################################
    def test_getPythonExecutable(self):
        """Unit test getPythonExecutable method
        """

        # Log total content in case of difference
        self.maxDiff = None

        reader = argUserSettingsReader(argUserSettingsReader_unittest.adminLvl,
                                       argUserSettingsReader_unittest.usrLvl)
        reader.read()
        self.assertEqual(reader.getPythonExecutable(),
                         argUserSettingsReader_unittest.expectedUsr.get("python_executable"))

    ########################################################################
    def test_getPythonSitePackage(self):
        """Unit test getPythonSitePackage method
        """

        # Log total content in case of difference
        self.maxDiff = None

        reader = argUserSettingsReader(argUserSettingsReader_unittest.adminLvl,
                                       argUserSettingsReader_unittest.usrLvl)
        reader.read()
        self.assertEqual(reader.getPythonSitePackage(),
                         argUserSettingsReader_unittest.expectedUsr.get("python_site_package"))

    ########################################################################
    def test_getArgScript(self):
        """Unit test getArgScript method
        """

        # Log total content in case of difference
        self.maxDiff = None

        reader = argUserSettingsReader(argUserSettingsReader_unittest.adminLvl,
                                       argUserSettingsReader_unittest.usrLvl)
        reader.read()
        self.assertEqual(reader.getArgScript(),
                         argUserSettingsReader_unittest.expectedUsr.get("arg_script"))

    ########################################################################
    def test_getParaviewSitePackage(self):
        """Unit test getParaviewSitePackage method
        """

        # Log total content in case of difference
        self.maxDiff = None

        reader = argUserSettingsReader(argUserSettingsReader_unittest.adminLvl,
                                       argUserSettingsReader_unittest.usrLvl)
        reader.read()
        self.assertEqual(reader.getParaviewSitePackage(),
                         argUserSettingsReader_unittest.expectedUsr.get("paraview_site_package"))

    ########################################################################
    def test_getParaviewLibraries(self):
        """Unit test getParaviewLibraries method
        """

        # Log total content in case of difference
        self.maxDiff = None

        reader = argUserSettingsReader(argUserSettingsReader_unittest.adminLvl,
                                       argUserSettingsReader_unittest.usrLvl)
        reader.read()
        self.assertEqual(reader.getParaviewLibraries(),
                         argUserSettingsReader_unittest.expectedUsr.get("paraview_libs"))

    ########################################################################
    def test_getLatexProcessor(self):
        """Unit test getLatexProcessor method
        """

        # Log total content in case of difference
        self.maxDiff = None

        reader = argUserSettingsReader(argUserSettingsReader_unittest.adminLvl,
                                       argUserSettingsReader_unittest.usrLvl)
        reader.read()
        self.assertEqual(reader.getLatexProcessor(),
                         argUserSettingsReader_unittest.expectedUsr.get("latex_processor"))

############################################################################
class argUserSettingsWriter_unittest(unittest.TestCase):
    """A GUI unit test class for argUserSettingsWriter
    """

    data     = [{"python_executable":"python3.7"},
                {"python_site_package":"python3.7/site-packages/"},
                {"arg_script":"ARG.py"},
                {"paraview_site_package":"paraview/python3.7/site-packages/"},
                {"paraview_libs":"paraview/lib/"},
                {"latex_processor":"latex/bin/"},
                {"python_executable":"python3.7",
                 "python_site_package":"python3.7/site-packages/",
                 "arg_script":"ARG.py",
                 "paraview_site_package":"paraview/python3.7/site-packages/",
                 "paraview_libs":"paraview/lib/",
                 "latex_processor":"latex/bin/"}]
    expected = data

    ########################################################################
    def test_write(self):
        """Unit test write method
        """

        # Log total content in case of difference
        self.maxDiff = None

        writer = argUserSettingsWriter()
        for i in range(len(argUserSettingsWriter_unittest.data)):
            writer.write("{}/{}{}.yml".format(workingDir, testName, i), argUserSettingsWriter_unittest.data[i])
            with open("{}/{}{}.yml".format(workingDir, testName, i),'r') as f:
                self.assertDictEqual(yaml.safe_load(f), argUserSettingsWriter_unittest.expected[i])
                f.close()

############################################################################
if __name__ == '__main__':
    unittest.main()

############################################################################
