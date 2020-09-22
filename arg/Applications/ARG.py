#HEADER
#                         arg/Applications/ARG.py
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

import distutils.spawn
import getopt
import os
import shutil
import sys
import time
import yaml

from arg import __version__
from arg.Applications import Explorator, Generator, Assembler
from arg.Common.argReportParameters import argReportParameters

ARG_VERSION = __version__

app = "ARG"

# Import ARG modules
if not __package__:
    sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
else:
    sys.path.append("..")

# Load supported types
common_dir = os.path.dirname(os.path.realpath(__file__))
with open(os.path.join(common_dir, "../Common/argTypes.yml"),
          'r',
          encoding="utf-8") as t_file:
    Types = yaml.safe_load(t_file)


class Runner:
    """A class to describe ARG runner parameters
    """

    def __init__(self, version=None):
        """Class constructor
        """

        # Default values of variables that must exist
        self.Explore = False
        self.Generate = False
        self.Assemble = False
        self.ParametersFile = None
        self.Parameters = None
        self.Version = version
        self.LatexProcessor = None
        self.TexFile = None

    @staticmethod
    def usage():
        """Provide online help
        """

        print("Usage:")
        print("\t [-h]                      Help: print this message and exit")
        print("\t [-e]                      run Explorator then Assembler")
        print("\t [-g]                      run Generator then Assembler")
        print("\t [-E]                      run Explorator")
        print("\t [-G]                      run Generator")
        print("\t [-A]                      run Assembler")
        print("\t [-p <parameters file>]    name of parameters file")
        print("\t [-l <LaTeX processor>]    name of LaTeX processor")
        print("\t [-t]                      generate just .tex file")
        sys.exit(0)

    def parse_line(self, app, default_parameters_filename, types=None):
        """Parse command line and fill artifact parameters
        """

        # Initiate caller as empty string by default
        caller = ""

        # Try to hash command line with respect to allowable flags
        try:
            opts, args = getopt.getopt(sys.argv[1:], "egEGAp:l:t")
        except getopt.GetoptError:
            self.usage()
            sys.exit(1)

        # Parse arguments and assign corresponding variables
        for o, a in opts:
            if o == "-h":
                self.usage()
                sys.exit(0)
            elif o == "-e":
                self.Assemble = True
                self.Explore = True
                caller = "Explorator"
            elif o == "-g":
                self.Assemble = True
                self.Generate = True
                caller = "Generator"
            elif o == "-E":
                self.Explore = True
                caller = "Explorator"
            elif o == "-G":
                self.Generate = True
                caller = "Generator"
            elif o == "-A":
                self.Assemble = True
                caller = "Assembler"
            elif o == "-p":
                self.ParametersFile = a
            elif o == "-l":
                self.LatexProcessor = a
            elif o == "-t":
                self.TexFile = True

        # Inform user if missing argument
        if not self.ParametersFile:
            print("*  WARNING: no parameters file name provided; "
                  "using '{}' by default.".format(default_parameters_filename))
            self.ParametersFile = default_parameters_filename

        # Create parameters
        self.Parameters = argReportParameters(app,
                                              self.ParametersFile,
                                              self.Version,
                                              types,
                                              self.LatexProcessor)
        self.Parameters.TexFile = self.TexFile

        # Populate attributes based on parameters file content
        return (self.Parameters.check_parameters_file()
                and self.Parameters.parse_parameters_file()
                and self.Parameters.check_parameters(caller))

    def run(self):
        """Run ARG applications based on parsed values
        """

        # Copy Explorator output file if exists
        concatenateStructureFile = False
        if self.Explore and os.path.isfile("{}.yml".format(self.Parameters.StructureFile)):
            concatenateStructureFile = True
            shutil.copyfile(os.path.realpath("{}.yml".format(self.Parameters.StructureFile)),
                            os.path.realpath("{}_tmp.yml".format(self.Parameters.StructureFile)))

        # Explore when required
        if self.Explore:
            Explorator.execute("Explorator", self.Parameters)

        # Generate when required
        if self.Generate:
            Generator.execute("Generator", self.Parameters)

        # Concatenate existing structure file content with generated content
        if concatenateStructureFile:
            with open(self.Parameters.StructureFile, 'w') as newFile:
                with open(self.Parameters.StructureFile, 'r') as existingFile:
                    newFile.write(existingFile.read())

        # Assemble when required
        if self.Assemble:
            Assembler.execute("Assembler", self.Parameters)


def main(app, types, version=None):
    """ ARG main method
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

    # Retrieve default parameters filename from provided types dict
    default_parameters_filename = types.get("DefaultParametersFile")

    runner = Runner(version)
    runner.parse_line(app, default_parameters_filename, types)

    # Run
    runner.run()

    # End stopwatch
    dt = time.time() - t_start

    # If this point is reached everything went fine
    success_apps = runner.Parameters.get_successful_apps(app)
    print("[{}] Ran {} successfully.".format(
        app,
        success_apps))
    print("[{}] Process completed in {} seconds. ###".format(
        app,
        dt))


def print_debug(app, python_debug=False, latex_debug=False, latex_proc=None):
    """ Print debug information when requested
    """

    # Print full Python interpreter path
    if python_debug:
        return_python = distutils.spawn.find_executable("python")
        if return_python:
            print("[{}] Python interpreter: {}".format(
                app,
                return_python.strip()))
        else:
            print("** ERROR: could not find a Python interpreter. Exiting.")
            sys.exit(1)
        # Print relevant environment variables
        env_dict = os.environ
        for k in ("PYTHONPATH", "LD_LIBRARY_PATH"):
            try:
                v = env_dict[k]
            except:
                v = ''
            print("[{}] {}: {}".format(app, k, v))

    # Print LaTeX processor information
    if latex_debug:

        # Retrieve specified processor if exists
        if latex_proc:
            print("[{}] LaTeX to PDF processor: {}".format(
                app,
                latex_proc.strip()))

        # Look for predefined list of possible processors otherwise
        else:
            # Start to look for full latexmk path
            return_latex = distutils.spawn.find_executable("latexmk")
            if return_latex:
                print("[{}] LaTeX to PDF processor: {}".format(
                    app,
                    return_latex.strip()))
            else:
                # If no latexmk was found, then look for full pdflatex path
                return_latex = distutils.spawn.find_executable("pdflatex")
                if return_latex:
                    print("[{}] LaTeX to PDF processor: {}".format(
                        app,
                        return_latex.strip()))
                else:
                    print("** WARNING: could not find a LaTeX to PDF processor. Generate a tex file only. ")


if __name__ == '__main__':
    """Main ARG routine
    """

    main(app, Types, ARG_VERSION)
