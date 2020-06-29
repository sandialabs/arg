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
paraviewVarKey = "PARAVIEW_PATH"
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
paraviewPath = os.environ[paraviewVarKey] if paraviewVarKey in os.environ else ''
pythonVarPath = os.environ[pythonVarKey] if pythonVarKey in os.environ else ''

os.environ[pythonVarKey] = os.pathsep.join([argPath,
                                            pythonVarPath,
                                            os.path.join(paraviewPath, "lib", "python3.7", "site-packages")])

# Print PYTHONPATH
print("{}: {}".format(pythonVarKey, os.environ[pythonVarKey]))

########################################################################
