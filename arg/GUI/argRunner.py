#HEADER
#                           arg/GUI/argRunner.py
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
DEBUG_ARG_GUI           = True
app                     = "ARG-GUI"

########################################################################
# Import python packages
import re

# Import GUI packages
from PySide2.QtCore             import QCoreApplication, \
                                       QFileInfo, \
                                       QDir, \
                                       QObject, \
                                       QProcess, \
                                       Signal

# Import ARG-GUI modules
from arg.GUI.argSettingsController      import *

########################################################################
class argRunner(QObject):
    """A runner class
    """

    # Signals
    logStandardDetected = Signal(str)
    logErrorDetected = Signal(str)
    argRunStarted = Signal()
    argRunFinished = Signal()

    ####################################################################
    def __init__(self, parent=None):

        super(argRunner, self).__init__(parent)

        settings = QCoreApplication.instance().settingsController

        self.argPythonExe = ""
        self.argPythonSitePackage= ""
        self.argScript = ""
        self.argParaviewPath = ""
        self.argParaviewLibrariesPath = ""
        self.argLatexProcessorPath = ""

        self.parameterFile = ""

        # Process creation
        self.process = QProcess()

        # Define connections
        self.process.readyReadStandardError.connect(self.onErrorDetected)
        self.process.readyReadStandardOutput.connect(self.onOutputDetected)

        # Set ARG execution default option
        self.argExecutionOption = settings.eOption()


    ####################################################################
    def initializeEnv(self):
        """Initialize environment to be applied on ARG process started by Runner
        """

        # Initialize QProcess environment
        env = QProcess.systemEnvironment()

        # Set PYTHONPATH
        env = self.initializeEnvVar(env,
            "PYTHONPATH",
            [self.argPythonExe, self.argPythonSitePackage, self.argParaviewPath])
        # Set DYLD_FALLBACK_LIBRARY_PATH
        env.append("DYLD_FALLBACK_LIBRARY_PATH={}".format(self.argParaviewLibrariesPath))

        # Set PATH
        env = self.initializeEnvVar(env,
            "PATH",
            [os.path.dirname(self.argPythonExe), self.argPythonExe,
             self.argParaviewLibrariesPath,
             os.path.dirname(self.argLatexProcessorPath), self.argLatexProcessorPath,
             os.environ["PATH"] if "PATH" in os.environ else ""])

        # Update environment of process to be used to run ARG
        self.process.setEnvironment(env)
        if DEBUG_ARG_GUI:
            print("[DEBUG_ARG_GUI] Completed ARG process environment:\n{}".format(env))

    ####################################################################
    def initializeEnvVar(self, env, envVarName, pathsList):
        """Initialize environment variable with provided list of paths
        """

        # Define regex
        regex = re.compile(r"^{}=(.*)".format(envVarName), re.IGNORECASE)

        # Build
        pathsStr = os.pathsep.join(pathsList)

        # TBD
        regexSub = r"{}={}".format(envVarName, os.pathsep.join(pathsList))
        # regexSub = r"{}=\1{}".format(envVarName, os.pathsep.join(pathsList))
        env = [regex.sub(regexSub.replace('\\', '/'), var.replace('\\', '/')) for var in env]

        # Loop over system environment to look for possibly existing value
        isPathFound = False
        for var in env:
            if envVarName in var:
                isPathFound = True
        if not isPathFound:
            env.append("{}={}".format(envVarName, pathsStr))

        # Print debug information when requested
        if DEBUG_ARG_GUI:
            print("[DEBUG_ARG_GUI] Building \'{}\' environment variable".format(envVarName))
            print("\tpathsStr: {}".format(pathsStr))
            print("\tregex: {}".format(regex))
            print("\tregexSub: {}".format(regexSub))
        return env

    ####################################################################
    def updateEnv(self):
        """Initialize Runner attributes, including parsed setting values
        """

        settings = QCoreApplication.instance().settingsController


        # Initialize setting values
        self.argPythonExe = settings.getArgPythonExePath()
        self.argPythonSitePackage = settings.getArgPythonSitePackagePath()
        self.argScript = settings.getArgScriptPath()
        self.argParaviewPath = settings.getArgParaviewPath()
        self.argParaviewLibrariesPath = settings.getArgParaviewLibrariesPath()
        self.argLatexProcessorPath = settings.getArgLatexProcessorPath()

        # Initialize ARG process environement
        self.initializeEnv()

    ########################################################################
    def start(self):

        # Update ARG process environement
        self.updateEnv()

        # Retrieve settings controller
        settings = QCoreApplication.instance().settingsController

        # Retrieve current file
        self.parameterFile = settings.getCurrentParameterFileRun()

        # Initiate ARG process if current file defined
        if(self.parameterFile) :

            # Set working directory
            parameterFileDir = QFileInfo(self.parameterFile).canonicalPath()
            self.process.setWorkingDirectory(parameterFileDir)
            print("[{}] Working directory: {}".format(app, parameterFileDir))

            # Gather arguments to run ARG with
            arguments = [settings.getArgScriptPath(), self.argExecutionOption, "-p", self.parameterFile]
            if self.argLatexProcessorPath:
                arguments.append("-l")
                arguments.append(self.argLatexProcessorPath)
            print("[{}] Starting with {} {}".format(app, settings.getArgPythonExePath(), arguments))

            # Emit start of process signal
            self.argRunStarted.emit()

            # Run ARG process
            self.process.start(settings.getArgPythonExePath(), arguments)
            self.process.waitForFinished()
            # print("[{}] Ending: {}".format(app, self.process.readAll()))
            # print("[{}] Error: {}".format(app, self.process.readAllStandardError()))

            # Emit end of process signal
            self.argRunFinished.emit()

        # Ask for parameters file otherwise
        else :
            self.logErrorDetected.emit("Please, set a parameters file to run.")

        return 1

    ########################################################################
    def clean(self, outputFolder):
        settings = QCoreApplication.instance().settingsController

        # Get current file
        parameterFile = settings.getCurrentParameterFile()
        if parameterFile:
            # Set working directory
            parameterFileDir = QFileInfo(parameterFile).canonicalPath()

            if outputFolder:
                if os.path.exists(outputFolder) and os.path.isdir(outputFolder):
                    outputFolderFullPath = outputFolder
                else:
                    outputFolderFullPath = os.path.join(parameterFileDir, outputFolder)
                outputFolderFullPathAsDir = QDir(outputFolderFullPath)
                if outputFolderFullPathAsDir.removeRecursively():
                    self.logStandardDetected.emit("[{}] 'Clean' action - the following output folder has been cleaned: {}"
                                                  .format(app, outputFolderFullPath))
                else:
                    self.logErrorDetected.emit("** ERROR: 'Clean' action - the following output folder cannot be cleaned: {}"
                                               .format(outputFolderFullPath))
            else:
                self.logErrorDetected.emit("** ERROR: 'Clean' action - the following output folder cannot be cleaned: {}"
                                           .format(outputFolder))

    ########################################################################
    def runEButtonClicked(self):
        """ Switch runner to E execution mode
        """

        settings = QCoreApplication.instance().settingsController
        self.argExecutionOption = settings.eOption()

    ########################################################################
    def runGButtonClicked(self):
        """ Switch runner to G execution mode
        """

        settings = QCoreApplication.instance().settingsController
        self.argExecutionOption = settings.gOption()

    ########################################################################
    def onErrorDetected(self):
        self.logErrorDetected.emit(str(self.process.readAllStandardError(), 'utf-8'))

    ########################################################################
    def onOutputDetected(self):
        self.logStandardDetected.emit(str(self.process.readAllStandardOutput(), 'utf-8'))

########################################################################
