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
app     = "ARG-GUI_tests"
data    = {"a":"A", "b":"B", "c":"C"}

############################################################################
# Import python packages
import os
import subprocess
import sys
import unittest

# Import ARG modules
if not __package__:
    home_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    root_path = os.path.join(home_path, "arg")
    sys.path.append(home_path)
    sys.path.append(root_path)
else:
    sys.path.append("..")
from arg.Applications                import ARG
from arg.GUI.argUserSettingsReader   import *
from arg.GUI.argUserSettingsWriter   import *

########################################################################
# Load supported types
with open(os.path.join(root_path, "Common/argTypes.yml"),
    'r',
    encoding="utf-8") as t_file:
    Types = yaml.safe_load(t_file)

# Define constants
adminLvl = "input/userSettingsAdmin.yml"
usrLvl   = "input/userSettingsUsr.yml"

############################################################################
def main():

    # Initiate reader and writer
    reader = argUserSettingsReader(adminLvl, usrLvl)
    writer = argUserSettingsWriter()

    # Read and write
    missingAdmin, missingSettings = reader.read()
    data = {"python_executable":reader.getPythonExecutable(),
            "python_site_package":reader.getPythonSitePackage(),
            "arg_script":reader.getArgScript(),
            "paraview_site_package":reader.getParaviewSitePackage(),
            "paraview_libs":reader.getParaviewLibraries(),
            "latex_processor":reader.getLatexProcessor()}
    writer.write("output/testUserSettingsReaderWriter.yml", data)

    # Check saved content is correct
    input = yaml.safe_load(open(usrLvl, 'r'))
    output = yaml.safe_load(open("output/testUserSettingsReaderWriter.yml", 'r'))
    return not missingAdmin and not missingSettings and input == output

########################################################################
if __name__ == '__main__':
    """Main readerWriter test routine
    """

    main()

########################################################################
