#HEADER
#                           arg/tests/pylintScan.py
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
app = "pylintScan"

########################################################################
# Import python packages
import getopt, os, shutil, sys, time
from pylint import epylint as lint

# Add home path
if not __package__:
    home_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
else:
    home_path = os.path.realpath("..")
home_path.lower() not in [path.lower() for path in sys.path] \
    and sys.path.append(home_path)

########################################################################
# Set separators
newModuleSep = "************* Module "

####################################################################
def clean():
    """pylintScan clean method to remove all result files from previous runs
    """

    print(os.path.join(home_path, "tests", "log"))
    try:
        shutil.rmtree(os.path.join(home_path, "tests", "log"), ignore_errors=True)
    except Exception as e:
        pass

########################################################################
def main(app):
    """pylintScan main method
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

    # Parse commandline arguments to detect clean routine
    opts, args = getopt.getopt(sys.argv[1:], "c")
    if '-c' in [opt[0] for opt in opts] or 'c' in args:
        print("\n==================== CLEAN PREVIOUS RESULTS ====================\n")
        clean()
    # Otherwise
    else:
        # Run scan routine
        scan(os.path.join(home_path, "arg"), "log/pylint/", "pylintScan.log", "pylintScan.err")

        # Parse scan result
        parse_pylint_log("log/pylint/pylintScan.log", "log/pylint/parsed/")

    # End stopwatch
    dt = time.time() - t_start

    # If this point is reached everything went fine
    print("[{}] Process completed in {} seconds. ###".format(
        app,
        dt))

########################################################################
def scan(root_dir, log_dir, log_file_name, err_file_name):
    """Scan main method
    """

    # Retrieve scan output
    output = lint.py_run(root_dir,
        ["--msg-template", "{path}:{line}:{column}: {msg_id}: {msg} ({symbol})",
         "--reports", "y"])
    stdout = output[0]
    stderr = output[1]

    # Create log file if does not exist
    if not os.path.exists(log_dir):
        os.makedirs(os.path.join(os.getcwd(), os.path.realpath(log_dir)))

    # Write standard output to log file
    with open(os.path.join(log_dir, log_file_name), "w") as log_file:
        print(stdout.getvalue(),
             file=log_file)
        log_file.close()

    # Write error output to log file
    with open(os.path.join(log_dir, err_file_name), "w") as err_file:
        print(stdout.getvalue(),
            file=err_file)
        err_file.close()

########################################################################
def parse_pylint_log(file_name, res_folder):
    """Parse log file generated by pylint
    """

    # Define module elements
    moduleContent = ''
    moduleName = ''

    # Create result folder
    if not os.path.exists(res_folder):
        os.makedirs(os.path.join(os.getcwd(), os.path.realpath(res_folder)))

    # Open file
    with open(file_name, 'r') as file:
        for line in file:
            currLine = file.readline()

            # Detect new module
            if newModuleSep in currLine:

                # Save previous module to log file
                if moduleName:
                    print("[{}] Parsed module '{}'.".format(
                        app,
                        moduleName))
                    module = open("{}/{}.log".format(res_folder, moduleName), 'w')
                    module.write(moduleContent)
                    module.close()

                # Save current module name and initiate content
                moduleName = currLine.replace(newModuleSep, '').strip()
                moduleContent = ''

            # Save non-empty lines
            elif currLine.strip():
                moduleContent = "{}{}".format(moduleContent, currLine)

        # End closing file
        file.close()

########################################################################
if __name__ == '__main__':
    """Scan main routine
    """

    main(app)
########################################################################
