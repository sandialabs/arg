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
app      = "ARG-GUI_unittests"

############################################################################
# Import python packages
import os
import sys
import unittest
import yaml

# Import ARG-GUI modules
if not __package__:
    home_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    src_path = os.path.join(home_path, "src")
    sys.path.append(home_path)
    sys.path.append(src_path)
    from src.GUI.argParameterReader         import *
    from src.GUI.argParameterWriter         import *
else:
    from ..src.GUI.argParameterReader       import *
    from ..src.GUI.argParameterWriter       import *

############################################################################
class argParameterReader_unittest(unittest.TestCase):
    """A GUI unit test class for argParameterReader
    """

    expected = {"BackendType":"LaTeX",
                "ReportType":"Report",
                "StructureFile":"../../../tests/GUI_tests/input/structure.yml",
                "OutputDir":"output",
                "Verbosity":0,
                "Final":False,
                "Number":"-%TEST_NAME%-%DATE%"}

    ########################################################################
    def test_verbosity_to_int(self):
        """Unit test all values on verbosity_to_int method
        """

        reader = argParameterReader()
        self.assertEqual(reader.verbosity_to_int("verbose"), 1)
        self.assertEqual(reader.verbosity_to_int("default"), 0)
        self.assertEqual(reader.verbosity_to_int("terse"), -1)
        self.assertEqual(reader.verbosity_to_int("test"), 0)

    ########################################################################
    def test_read(self):
        """Unit test read method
        """

        reader = argParameterReader()
        reader.read(os.path.join(os.path.dirname(os.path.abspath(__file__)), "input/parameters.yml"))
        self.assertDictEqual(reader.ParameterData.Dict, argParameterReader_unittest.expected)

############################################################################
class argParameterWriter_unittest(unittest.TestCase):
    """A GUI unit test class for argParameterWriter
    """

    data     =  [{"a":"A", "b":"B", "c":"C", "d":"D"},
                 {"backend_type":"A", "report_type":"B", "structure":"C", "output":"D"},
                 {"backend_type":"LaTeX", "report_type":"Report", "structure":"structure.yml", "output":"output"},
                 {"BackendType":"A", "ReportType":"B", "StructureFile":"C", "OutputDir":"D"},
                 {"BackendType":"LaTeX", "ReportType":"Report", "StructureFile":"structure.yml", "OutputDir":"output"}]

    expected = [{},
                {},
                {},
                {"backend_type":"A", "report_type":"B", "structure":"C.yml", "output":"D"},
                {"backend_type":"LaTeX", "report_type":"Report", "structure":"structure.yml", "output":"output"}]

    ########################################################################
    def test_setData(self):
        """Unit test setData method
        """

        writer = argParameterWriter()
        for i in range(len(argParameterWriter_unittest.data)):
            writer.setData(argParameterWriter_unittest.data[i])
            self.assertDictEqual(writer.ParameterData.Dict, argParameterWriter_unittest.data[i])

    ########################################################################
    def test_write(self):
        """Unit test write method
        """

        writer = argParameterWriter()
        for i in range(len(argParameterWriter_unittest.data)):
            writer.setData(argParameterWriter_unittest.data[i])
            writer.write("output/unitTestParametersReaderWriter{}.yml".format(i))
            if i == 3 or i == 4:
                with open("output/unitTestParametersReaderWriter{}.yml".format(i),'r') as f:
                    self.assertDictEqual(yaml.safe_load(f), argParameterWriter_unittest.expected[i])
                    f.close()
            else:
                self.assertFalse(os.stat("output/unitTestParametersReaderWriter{}.yml".format(i)).st_size)

############################################################################
if __name__ == '__main__':
    unittest.main()

############################################################################
