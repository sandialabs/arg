#HEADER
#                     arg/tests/GUI_tests/all_gui_tests.py
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
import subprocess
import sys
import time

from tests.GUI_tests.integrationtests import integration
from tests.tools import unittest_application

prefix = "GUI_tests"
app = "ARG-{}".format(prefix)


def main():
    """ARG GUI tests main method
    """

    # Run integration tests
    integration.main()

    # Run unit tests
    dir_path = os.path.dirname(os.path.realpath(__file__))
    subprocess.run(["python", "-m", "unittest", "discover", "-s", dir_path, "-p", "test_arg*.py"])


if __name__ == '__main__':
    """ARG GUI tests main routine
    """
    # Start stopwatch
    t_start = time.time()

    # Print startup information
    sys_version = sys.version_info
    print("[{}] ### Started with Python {}.{}.{}".format(
        app,
        sys_version.major,
        sys_version.minor,
        sys_version.micro))

    unittest_application()
    main()

    # End stopwatch
    dt = time.time() - t_start

    # If this point is reached everything went fine
    print("[{}] Process completed in {} seconds. ###".format(
        app,
        dt))
