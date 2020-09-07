#HEADER
#                  arg/tests/GUI_tests/integration.py
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


import getopt
import os
import shutil
import sys
import time

from tests.GUI_tests.integrationtests import testParametersController, testUserSettingsReaderWriter, \
    testSettingsController, testParametersReaderWriter
from tests.tools import clean, unittest_application

prefix = "GUI_integrationtests"
app = "ARG-{}".format(prefix)


def main():
    """ARG GUI integration tests main method
    """

    # Create output directory if does not exist
    if not os.path.exists("output") or not os.path.isdir("output"):
        os.mkdir("output")

    print("\n-------------------- [{}] testParametersController --------------------".format(app))
    testParametersController.main()
    print("\n-------------------- [{}] testParametersReaderWriter --------------------".format(app))
    testParametersReaderWriter.main()
    print("\n-------------------- [{}] testSettingsController --------------------".format(app))
    testSettingsController.main()
    print("\n-------------------- [{}] testUserSettingsReaderWriter --------------------".format(app))
    testUserSettingsReaderWriter.main()


if __name__ == '__main__':
    """ARG GUI integration tests main routine
    """
    t_start = time.time()
    sys_version = sys.version_info
    print("[{}] ### Started with Python {}.{}.{}".format(
        app,
        sys_version.major,
        sys_version.minor,
        sys_version.micro))

    # Parse commandline arguments to detect clean routine
    opts, args = getopt.getopt(sys.argv[1:], "c")
    if '-c' in [opt[0] for opt in opts] or 'c' in args:
        print("\n-------------------- [{}] Clean previous results --------------------\n".format(app))
        clean(prefix)
        try:
            shutil.rmtree(prefix)
        except:
            pass
    else:
        unittest_application()
        main()

    dt = time.time() - t_start

    print("[{}] Process completed in {} seconds. ###".format(
        app,
        dt))
