#HEADER
#                         tests/build_tests/setEnv.py
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
debug = False

########################################################################
# Import ARG modules
import os, platform, sys, yaml

# Add home path
if not __package__:
    home_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
else:
    home_path = os.path.realpath("..")
home_path.lower() not in [path.lower() for path in sys.path] \
    and sys.path.append(home_path)

########################################################################
# Define default config file name
configFile = "config.yml"

# Define expected config file keys
backendTypesKey = "backendTypes"
reportTypesKey = "reportTypes"
hostKey = "host"
machineKey = "machine"
argFileKey = "argFile"
parametersFileKey = "parametersFile"
argHomeKey = "ARG_HOME"
argVarKey = "ARG_HOME"
pythonVarKey = "PYTHONPATH"

# Define default values
backendTypes = ["LaTeX", "Word"]
reportTypes = ["Report"]
host = platform.system()
machine = "NotDefined"
argFile = ".arg"
parametersFile = "parameters.yml"
argHome = home_path

########################################################################
# Retrieve config file content
config = yaml.safe_load(open(configFile))
config = {key: value for item in config if isinstance(item, dict) for key, value in item.items()}
if debug:
    print("Config file is {}".format(configFile))
    print("It contains: ")
    print(config)

########################################################################
# Retrieve backend types
if backendTypesKey in config.keys() and config.get(backendTypesKey):
    backendTypes = config.get(backendTypesKey)
else:
    print("*  Warning: No ackend type is defined in provided config file. Using default values.")

# Retrieve report types
if reportTypesKey in config.keys() and config.get(reportTypesKey):
    reportTypes = config.get(reportTypesKey)
else:
    print("*  Warning: No backend type is defined in provided config file. Using default values.")

# Retrieve host
if hostKey in config.keys() and config.get(hostKey):
    host = config.get(hostKey)
else:
    print("*  Warning: No host is defined in provided config file. Using default value.")

# Retrieve machine
if machineKey in config.keys() and config.get(machineKey):
    machine = config.get(machineKey)
else:
    print("*  Warning: No machine is defined in provided config file. Using default value.")

# Retrieve report types
if argFileKey in config.keys() and config.get(argFileKey):
    argFile = config.get(argFileKey)
else:
    print("*  Warning: No test case regex is defined in provided config file. Using default value.")

# Retrieve parameters file name
if parametersFileKey in config.keys() and config.get(parametersFileKey):
    parametersFile = config.get(parametersFileKey)
else:
    print("*  Warning: No parameters file name is defined in provided config file. Using default value.")

# Retrieve ARG_HOME path
if argHomeKey in config.keys() and config.get(argHomeKey):
    argHome = config.get(argHomeKey)
else:
    print("*  Warning: No parameters file name is defined in provided config file. Using default value.")

# Print results
print("{}: {}".format(backendTypesKey, backendTypes))
print("{}: {}".format(reportTypesKey, reportTypes))
print("{}: {}".format(hostKey, host))
print("{}: {}".format(machineKey, machine))
print("{}: {}".format(argFileKey, argFile))
print("{}: {}".format(parametersFileKey, parametersFile))
print("{}: {}".format(argHomeKey, argHome))

########################################################################
# Complete PYTHONPATH
argPath = os.environ[argVarKey] if argVarKey in os.environ else argHome if argHome else ''
pythonVarPath = os.environ[pythonVarKey] if pythonVarKey in os.environ else ''

os.environ[pythonVarKey] = os.pathsep.join([argPath,
                                            pythonVarPath,
                                            os.path.join("lib", "python3.7", "site-packages")])

# Print PYTHONPATH
print("{}: {}".format(pythonVarKey, os.environ[pythonVarKey]))

########################################################################
