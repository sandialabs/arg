#HEADER
#                        arg/tests/all_tests.py
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

########################################################################
app                 = "ARG all_tests"
prefix              = "all_tests"

############################################################################
# Import python packages
import getopt, os, shutil, subprocess, sys, time
from pathlib                    import Path

# Add home path
if not __package__:
    home_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
else:
    home_path = os.path.realpath("..")
home_path.lower() not in [path.lower() for path in sys.path] \
    and sys.path.append(home_path)

####################################################################
def clean():
    """ARG tests overall clean method to remove all result files from previous runs
    """

    # Run build tests
    print("\n==================== ARG build tests ====================\n")
    os.chdir("build_tests")
    proc = subprocess.Popen(["python",
                             "test.py",
                             "-c"])
    proc.wait()
    os.chdir("..")

    # Run GUI tests
    print("\n==================== ARG GUI tests ====================\n")
    os.chdir("GUI_tests")
    proc = subprocess.Popen(["python",
                             "test.py",
                             "-c"])
    proc.wait()
    os.chdir("..")

    # Run pylint scan
    print("\n==================== ARG pylint scan ====================\n")
    proc = subprocess.Popen(["python",
                             "pylintScan.py",
                             "-c"])
    proc.wait()

############################################################################
def main():
    """ARG test main method
    """

    # Run build tests
    print("\n==================== ARG build tests ====================\n")
    os.chdir("build_tests")
    proc = subprocess.Popen(["python",
                             "test.py"])
    proc.wait()
    os.chdir("..")

    # Run GUI tests
    print("\n==================== ARG GUI tests ====================\n")
    os.chdir("GUI_tests")
    proc = subprocess.Popen(["python",
                             "test.py"])
    proc.wait()
    os.chdir("..")

    # Run pylint scan
    print("\n==================== ARG pylint scan ====================\n")
    proc = subprocess.Popen(["python",
                             "pylintScan.py"])
    proc.wait()

########################################################################
if __name__ == '__main__':
    """ARG test main routine
    """

    # Start stopwatch
    t_start = time.time()

    # Print startup information
    sys_version = sys.version_info
    print("*************************************************************************")
    print("[{}] ### Started with Python {}.{}.{}".format(
        app,
        sys_version.major,
        sys_version.minor,
        sys_version.micro))

    # Create boolean to run tests
    runTests = True
    # Create boolean to clean repository
    cleanRepo = False

    # Parse commandline arguments to detect clean routine
    opts, args = getopt.getopt(sys.argv[1:], "c")
    if '-c' in [opt[0] for opt in opts] or 'c' in args:
        print("\n==================== CLEAN PREVIOUS RESULTS ====================\n")
        clean()
    # Otherwise, run main routine
    else:
        main()

    # End stopwatch
    dt = time.time() - t_start

    # If this point is reached everything went fine
    print("*************************************************************************")
    print("[{}] Process completed in {} seconds. ###".format(
    app,
    dt))

########################################################################
