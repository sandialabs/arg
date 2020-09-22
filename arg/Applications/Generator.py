# HEADER
#                      arg/Applications/Generator.py
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
# HEADER

import os
import sys
import time

import yaml

from arg import __version__
from arg.Common.argReportParameters import argReportParameters
from arg.Generation import argPlot, argVTK
from arg.Tools import Utilities

ARG_VERSION = __version__

app = "Generator"

# Import ARG modules
if not __package__:
    sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
else:
    sys.path.append("..")

# Load supported types
common_dir = os.path.dirname(os.path.realpath(__file__))
with open(os.path.join(common_dir, "../Common/argTypes.yml"), 'r', encoding="utf-8") as t_file:
    Types = yaml.safe_load(t_file)


def main(app, types, version=None):
    """ Generator main method
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

    # Instantiate parameters object from command line arguments
    parameters = argReportParameters(app, version=version, types=types)

    # Parse command line arguments to get parameters file value
    if parameters.parse_line():
        # Execute
        execute(app, parameters)

    # Print error message if something went wrong
    else:
        print("*  ERROR: cannot parse parameters. Exiting.")

    # End stopwatch
    dt = time.time() - t_start

    # If this point is reached everything went fine
    success_apps = parameters.get_successful_apps(app)
    print("[{}] Ran {} successfully.".format(app, success_apps))
    print("[{}] Process completed in {} seconds. ###".format(app, dt))


def execute(app, parameters):
    """ Generator execute method
    """

    # Parse parameters file
    print("[{}] Parsing parameters file".format(app))

    # Generate document structure from discovered data
    generate_artefacts(parameters)

    # Log execution status
    parameters.log_execution_status(app, "{}/".format(os.path.dirname(parameters.OutputDir)))


def generate_artefacts(parameters):
    """ Generate artefacts from provided data
    """

    # Open provided structure file
    artifact_map = Utilities.read_yml_file(parameters.ArtifactFile, parameters.Application)

    if isinstance(artifact_map, str):
        print("*  WARNING: {} {}".format(parameters.Application, artifact_map))
        return False

    # Iterate over requested artifacts
    n_missing = 0
    for request_params in artifact_map:
        # Retrieve artifact type
        item_type = request_params.get('n')

        # VTK artifact
        if item_type == "vtk":
            # Find or create VTK figure artifact
            base_name, caption = argVTK.execute_request(parameters, request_params)
            if not base_name:
                print("*  WARNING: could neither find nor create visualization. Skipping it.")
                n_missing += 1
                continue

        # MatPlotLib artifact
        elif item_type == "plot":
            # Find or create MatPlotLib figure artifact
            base_name, caption = argPlot.execute_request(parameters, request_params)
            if not base_name:
                print("*  WARNING: could neither find nor create plot. Skipping it.")
                n_missing += 1
                continue

        # Save caption as file
        caption.write(parameters.Backend,
                      parameters.OutputDir,
                      base_name)
        print("[{}] Created {} artifact/caption pair".format(app, base_name))

    # Report on missing items and terminate
    if n_missing:
        print("[{}] Process incomplete with {} missing artifact/caption pair(s)".format(
            app,
            n_missing))
    else:
        print("[{}] Process complete with no missing artifacts".format(
            app))


if __name__ == '__main__':
    """Main artifact generator routine
    """

    main(app, Types, ARG_VERSION)
