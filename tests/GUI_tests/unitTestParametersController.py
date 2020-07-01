#HEADER
#          arg/tests/GUI_tests/unitTestParametersController.py
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
testName   = "unitTestParametersController"

############################################################################
# Import python packages
import datetime, os, random, sys, unittest, yaml

# Import GUI packages
from PySide2.QtCore             import QCoreApplication, \
                                       QObject, \
                                       Signal, \
                                       Slot
# Add home path
if not __package__:
    home_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
else:
    home_path = os.path.realpath("../..")
home_path.lower() not in [path.lower() for path in sys.path] \
    and sys.path.append(home_path)

# Import ARG modules
from arg.GUI.argApplication            import argApplication
from arg.GUI.argParameterController    import argParameterController
from arg.GUI.argSettingsController     import argSettingsController
from tests.tools                       import prepareParametersFile, unittest_application, unittest_signal

############################################################################
class argParameterController_unittest(unittest.TestCase):
    """A GUI unit test class for argParameterController
    """

    # Define parameters file
    inputFile = os.path.join(home_path, "tests", "GUI_tests", "input", "parameters.yml")
    parametersFilePath = prepareParametersFile(inputFile, workingDir, testName)


    expectedRead = {"BackendType":"LaTeX",
                    "ReportType":"Report",
                    "StructureFile":"../../../tests/GUI_tests/input/structure.yml",
                    "OutputDir":"{}".format(prefix),
                    "Verbosity":0,
                    "Final":False,
                    "Number":"-{}-{}".format(testName,
                                             datetime.datetime.strftime(datetime.datetime.now(), "%Y-%m-%d"))}

    dataWrite     =  [{"a":"A", "b":"B", "c":"C", "d":"D"},
                      {"backend_type":"A", "report_type":"B", "structure":"C", "output":"D"},
                      {"backend_type":"LaTeX", "report_type":"Report", "structure":"structure.yml", "output":"output"},
                      {"BackendType":"A", "ReportType":"B", "StructureFile":"C", "OutputDir":"D"},
                      {"BackendType":"LaTeX", "ReportType":"Report", "StructureFile":"structure.yml", "OutputDir":"output"}]
    expectedWrite = [{},
                     {},
                     {},
                     {"backend_type":"A", "report_type":"B", "structure":"C.yml", "output":"D"},
                     {"backend_type":"LaTeX", "report_type":"Report", "structure":"structure.yml", "output":"output"}]

    data          = {"BackendType":"LaTeX", "ReportType":"Report", "StructureFile":"structure.yml", "OutputDir":"output"}

    ########################################################################
    def test_read(self):
        """Unit test read method
        """
        # Log total content in case of difference
        self.maxDiff = None

        # Create test parameterController
        controller = argParameterController()

        # Apply test scenario
        self.assertEqual(controller.read(argParameterController_unittest.parametersFilePath),
                         True)
        self.assertEqual(app.settingsController.getCurrentParameterFile(),
                         argParameterController_unittest.parametersFilePath)

    ########################################################################
    def test_write(self):
        """Unit test write method
        """

        # Log total content in case of difference
        self.maxDiff = None

        # Create test parameterController
        controller = argParameterController()

        # Apply test scenario
        for i in range(len(argParameterController_unittest.dataWrite)):
            controller.write("{}/{}{}.yml".format(workingDir, testName, i),
                             argParameterController_unittest.dataWrite[i])
            if i == 3 or i == 4:
                with open("{}/{}{}.yml".format(workingDir, testName, i),'r') as f:
                    self.assertDictEqual(yaml.safe_load(f),
                                         argParameterController_unittest.expectedWrite[i])
                    self.assertEqual(app.settingsController.getCurrentParameterFile(),
                                     "{}/{}{}.yml".format(workingDir, testName, i))
                    f.close()
            else:
                self.assertFalse(os.stat("{}/{}{}.yml".format(workingDir, testName, i)).st_size)

    ########################################################################
    def test_reloadData(self):
        """Unit test reloadData method
        """

        # Log total content in case of difference
        self.maxDiff = None

        # Create test parameterController
        controller = argParameterController()

        # Apply test scenario

        # Check backupData is initialized empty by default
        self.assertDictEqual(controller.backupData, {})

        # Check backupData is still empty after a realoadData BEFORE any read
        controller.reloadData()
        self.assertDictEqual(controller.backupData, {})

        # Check backupData is updated after a read
        controller.read(argParameterController_unittest.parametersFilePath)
        self.assertDictEqual(controller.backupData,
                             argParameterController_unittest.expectedRead)

        # Check empty backupData is NOT updated after a write
        i = random.randint(0, len(argParameterController_unittest.dataWrite) - 1)
        controller.write("{}/unitTestParametersControllerReload.yml".format(workingDir),
                         argParameterController_unittest.dataWrite[i])
        self.assertNotEqual(controller.backupData,
                             argParameterController_unittest.dataWrite[i])
        self.assertDictEqual(controller.backupData,
                             argParameterController_unittest.expectedRead)

        # Clean backupData
        controller.backupData = {}
        self.assertDictEqual(controller.backupData, {})

        # Check backupData is restored after a realoadData AFTER a read
        controller.reloadData()
        self.assertDictEqual(controller.backupData, {})

    ########################################################################
    def test_onDataCreated(self):
        """Unit test onDataCreated method
        """

        # Log total content in case of difference
        self.maxDiff = None

        # Create test parameterController
        controller = argParameterController()
        handler = unittest_signal()

        # Apply test scenario
        controller.dataCreated.connect(handler.onDataReceived)
        controller.onDataCreated(argParameterController_unittest.dataWrite[4])
        self.assertEqual(handler.callCount, 1)
        self.assertDictEqual(handler.dataReceived,
                             argParameterController_unittest.data)

############################################################################
if __name__ == '__main__':

    # Create test application
    app = unittest_application(workingDir, testName)

    # Run test main routine
    unittest.main()

    # Quit test application
    app.quit()

############################################################################
