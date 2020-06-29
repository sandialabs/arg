#HEADER
#                    arg/tests/build_tests/test.py
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

################################################################################
prefix = "build_tests"
app    = "ARG-{}".format(prefix)

################################################################################
# Import python packages
import getopt, os, shutil, subprocess, sys, time
from pathlib                    import Path

# Add home path
if not __package__:
    home_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
else:
    home_path = os.path.realpath("..")
home_path.lower() not in [path.lower() for path in sys.path] \
    and sys.path.append(home_path)

# Import ARG modules
from tests.tools import clean
from setEnv import *

# Define string constants
testCaseRegex = "{}-cases.txt".format(prefix)
argLogFile    = "ARG.log"
argErrFile    = "ARG.err"
argTmpFile    = "ARG.tmp"
parametersSep = "@"

# Retrieve variable environment
ARG_HOME      = os.environ["ARG_HOME"] if "ARG_HOME" in os.environ else home_path

############################################################################
def findTestCases():
    """Python wrapper of sed method
    """

    # Save current test case file and path
    testCaseFile = testCaseRegex
    testCasePath = os.path.realpath(testCaseFile)

    if not os.path.isfile("."):
        # List all test cases in test_cases.txt file
        f = open(testCasePath, "w")
        for testCase in Path(".").rglob(argFile):
            f.write(os.path.dirname(testCase))
            if "structure: %DOC_NAME%" in open(testCase, "r").read():
                f.write("{}-e".format(parametersSep))
            else:
                f.write("{}-g".format(parametersSep))
            f.write("\n")
        f.close()

############################################################################
def sed(fileName, str1, str2):
    """Python wrapper of sed method
    """

    # Open file in read mode
    f = open(fileName, "rt")
    # Read all file
    data = f.read()
    # Replace str1 by str2 in read data
    data = data.replace(str1, str2)
    # Close file
    f.close()

    # Open file in write mode
    f = open(fileName, "wt")
    # Dump modified data
    f.write(data)
    # Close file
    f.close()

############################################################################
def checkStructureFileExists(filePath):
    """Check in provided template parameters file if structure file already defined
    """

    # Open provided file
    file = yaml.safe_load(filePath)

    # Check if "data" key exists
    if "data" in file and "%DOC_NAME%.yml" in filePath:
        return False
    else:
        return True

############################################################################
def build_ind(machine, caseName, caseRunType, report, backend):
    """Individual building routine
    """

    # Indicate current test case
    print("... on {} {}".format(report, backend))

    # Create clean working folder
    workingDir = "{}-{}-{}-{}".format(prefix, caseName.strip(), report, backend)
    workingPath = os.path.realpath("{}/{}".format(caseName.strip(), workingDir))
    casePath =  os.path.dirname(workingPath)
    if not os.path.exists(workingPath):
        os.mkdir(workingPath)

    # Copy constants file template to test current working folder
    parametersFilePath = os.path.realpath("{}/{}".format(workingPath, parametersFile))
    shutil.copyfile(os.path.realpath("{}/{}".format(caseName.strip(), argFile)),
                    parametersFilePath)

    # Determine document extension
    if backend == "LaTeX":
        extension = ".pdf"
    elif backend == "Word":
       extension = ".docx"
    else:
       extension = ""

    # Substitute BACKEND_TYPE in copied constants file template
    sed(parametersFilePath, "%BACKEND_TYPE%", backend)

    # Substitute REPORT_TYPE in copied constants file template
    sed(parametersFilePath, "%REPORT_TYPE%", report)

    # Substitute DOC_NAME in copied parameters file template
    sed(parametersFilePath, "%DOC_NAME%", workingDir)

    # Substitute OUTPUT_DIR in copied parameters file template
    sed(parametersFilePath, "%OUTPUT_DIR%", workingPath)

    # Substitute OUTPUT_DIR in copied parameters file template
    sed(parametersFilePath, "%WORKING_DIR%", os.path.join(casePath, "data"))

    # Create output files
    out = open(os.path.realpath("{}/{}".format(workingPath, argLogFile)), "a")
    err = open(os.path.realpath("{}/{}".format(workingPath, argErrFile)), "a")

    # Call ApreproSubstitutor if template exists
    templateFilePath = os.path.realpath("{}/Results.template.yml".format(casePath))
    dataFilePath = os.path.realpath("{}/params.dat".format(casePath))
    resultsFilePath = os.path.realpath("{}/Results.yml".format(casePath))
    if os.path.exists(templateFilePath) and os.path.isfile(templateFilePath):
        subprocess.Popen(["python",
                          os.path.realpath("{}/arg/Applications/ApreproSubstitutor.py".format(ARG_HOME)),
                          "-a",
                          dataFilePath,
                          "-t",
                          templateFilePath,
                          "-o",
                          resultsFilePath],
                          stdout=out, stderr=err)

    # Determine if structure file exists and save run type for ARG argument
    argRunType = "-g" if checkStructureFileExists(parametersFilePath) else "-e"

    # Execute runner
    proc = subprocess.Popen(["python",
                             os.path.realpath("{}/arg/Applications/ARG.py".format(ARG_HOME)),
                             caseRunType,
                             "-p",
                             parametersFilePath],
                             stdout=out, stderr=err)
    proc.wait()
    out.flush()

    # Copy generated report to case-level directory
    try:
        shutil.copyfile(os.path.realpath("{}/{}{}".format(workingPath, workingDir, extension)),
                    os.path.realpath("{}/{}{}".format(caseName.strip(), workingDir, extension)))
    except:
        print("Could not copy generated report to case-level directory.")

############################################################################
def build_all(machine, caseName, caseType, reportTypes, backendTypes):
    """Building routine over all report and backend type associations
    """

    # Iterate over all available report types
    for report in reportTypes:

        # Iterate over all available backend types
        for backend in backendTypes:

            # Build current case
            build_ind(machine, caseName, caseType, report, backend)

############################################################################
def main():
    """ARG build tests main method
    """

    # Generate test cases in dedicated file
    findTestCases()

    # Iterate over all found test cases
    for case in open(testCaseRegex.format(os.path.join("tests", "build_tests"))):
        [caseName, caseRunType] = case.strip().split(parametersSep)

        # Indicate current test case
        print("-------------------------------------------------------------------------")
        print("Running build test {}...".format(caseName))

        # Build all report and backend type associations
        build_all(machine, caseName, caseRunType, reportTypes, backendTypes)

################################################################################
if __name__ == '__main__':
    """ARG build tests main routine
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
        print("\n-------------------- [{}] Clean previous results --------------------\n".format(app))
        clean(prefix)
    # Otherwise, run main routine
    else:
        main()

    # End stopwatch
    dt = time.time() - t_start

    # If this point is reached everything went fine
    print("[{}] Process completed in {} seconds. ###".format(
    app,
    dt))

################################################################################
