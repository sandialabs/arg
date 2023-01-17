#HEADER
#                      arg/web/api/application.py
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

# Import python packages
from datetime import datetime
import threading

# Import PySide2 packages
from PySide2.QtCore import QObject, QFile, QFileInfo, Qt, Slot

# Import ARG-GUI modules from the ARG-GUI logic layer
from arg.GUI.Logic.argParameterController import *
from arg.GUI.Logic.argRunner import *
from arg.GUI.Logic.argSettingsController import *

from .session_manager import SessionManager
from .session import Session
from .settings import ServerSettings

from yaml.scanner import ScannerError
from yaml.parser import ParserError


class Application(QObject):
    
    """
    An application class for the web arg application
    This class is similar to the GUI argApplication class (QT one) except there is no user
    interface.
    """

    def __init__(self):
        """
        Initializes a new instance of Application.
        """
        super(Application, self).__init__(parent=None)

        # Create controllers, runner and action manager
        self.settingsController = argSettingsController()
        # Retrieve list of missing settings from settings controller initialization
        missingSettings = self.settingsController.initialize()

        # Show missing settings when exist
        if missingSettings:
            self.showConfigMissingSettings(missingSettings, True)

        self.parameterController = argParameterController()
        self.parameterController.setSettingsController(self.settingsController)
        self.runner = argRunner()
        self.runner.setSettingsController(self.settingsController)
        self.logs = []

        # Save before run
        self.saveBeforeRunEnabled = False

        # connection to signals
        self.parameterController.dataCreated.connect(self.onDataCreated, Qt.DirectConnection)
        self.runner.logErrorDetected.connect(self.onLogErrorDetected, Qt.DirectConnection)
        self.runner.logStandardDetected.connect(self.onLogStandardDetected, Qt.DirectConnection)
        self.runner.argRunStarted.connect(self.onArgRunStarted, Qt.DirectConnection)
        self.runner.argRunFinished.connect(self.onArgRunFinished, Qt.DirectConnection)

        # Load some flask server settings
        self.serverSettings = ServerSettings()

        # Load settings.yml from current directory if exists
        s_settings_filepath = os.path.join(os.path.dirname(__file__), 'settings.yml')
        if (os.path.exists(s_settings_filepath)):
            self.serverSettings.from_file(s_settings_filepath)
        self.serverSettings.make_dirs()
        self.applicationName = self.serverSettings.app_name

        # Variable to store the data returned by the slot onDataCreated
        # This variable is used by reload or load parameters to retrieve results
        self.loadedParameters = None

    def saveBeforeRunRequested(self, enabled):
        self.saveBeforeRunEnabled = enabled


    def runRequested(self, parameters):
        """Upon run action request
        """

        # Clean logs
        self.clearLogs()

        if self.saveBeforeRunEnabled:
            self.actionManager.saveAct.trigger()

        # Get current file
        parameterFile = self.settingsController.getCurrentParameterFile()

        # Call 'Run' action if current file defined
        if parameterFile:

            # Save current parameters values in temp file
            parameterQFile = QFileInfo(parameterFile)
            fileCanonicalFilePath = parameterQFile.canonicalPath()
            fileBaseName = parameterQFile.baseName()
            fileSuffix = parameterQFile.suffix()
            fileDateTime = datetime.now().strftime("-%Y-%m-%d-%H-%M-%S")
            filePathTemp = "{}/{}{}.{}".format(
                fileCanonicalFilePath, fileBaseName, fileDateTime, fileSuffix)
            self.parameterController.write(filePathTemp, parameters)
            self.settingsController.setCurrentParameterFileRun(filePathTemp)

            # Write overwrite the currentParameter file, but here, it is done with a temp file
            # As a consequence, we really need to give it is previous and correct value
            self.settingsController.setCurrentParameterFile(parameterFile)
            self.runner.start()

        # Ask for parameters file otherwise
        else:
            self.onLogErrorDetected("Cannot run without a parameters file. ")
            raise Exception("Cannot run without a parameters file.")

    def cleanRequested(self):
        """Upon clean action request
        """
        # Retrieve data from parameters values
        data = self.parameterController.backupData
        outputFolder = ''

        if self.settingsController.outputFolderKey() in data:
            outputFolder = data.get(self.settingsController.outputFolderKey())

        # Call the clean method of the runner
        self.runner.clean(outputFolder)


    def reloadRequested(self):
        """Upon reload action request
        """

        # Reload backup data, as read from current parameters file initial state
        self.parameterController.reloadData()

    @Slot(dict)
    def onDataCreated(self, data):
        """Dictionary slot receiving created data
        """

        self.loadedParameters = data

    @Slot(str)
    def onLogStandardDetected(self, log):
        """String slot receiving standard log message
        """

        self.logInfo(log)

    @Slot(str)
    def onLogErrorDetected(self, log):
        """String slot receiving error log message
        """

        self.logError(log)

    @Slot()
    def onArgRunStarted(self):
        """Slot receiving ARG run state
        """

        self.logInfo("Starting ARG process on server...")

    @Slot()
    def onArgRunFinished(self):
        """Slot receiving ARG run state
        """

        parameterFile = self.settingsController.getCurrentParameterFileRun()
        currentRunFile = QFile(parameterFile)
        currentRunFile.remove()
        self.settingsController.setCurrentParameterFileRun("")

    def showConfigMissingSettings(self, missings, exitEarly):
        """
        Shows an error listing all missing settings
        """

        # Print error message for log
        print("[{}] Following settings are missing:\n"
              "\t- \'{}\'\nPlease define at USER or ADMIN level. Exiting."
              .format(app, "\'\n\t- \'".join(missings)))

        # Path to Word documentation -- contained in repository
        err = ("ARG-GUI missing settings\n"
               "Following settings are missing:<br>"
               "- \'<code>{}</code>\'<br>Please define at USER or ADMIN level. Exiting.")
        err = err.format("</code>\'<br>- \'<code>".join(missings))
        self.logError(err, raise_error=True)

    # added methods for api

    def log(self, level: str, message: str, applicationName: str = None):
        """Adds a log to the logs of the current application

        level: INFO|SUCCESS|ERROR
            the log level
        message: str
            the log message
        """

        log = {}
        log["date"] = datetime.now().__str__()
        log["level"] = level
        if applicationName is None:
            log["message"] = message
        else:
            log["message"] = str.format('[{}] {}', applicationName, message)
        self.logs.append(log)

    def clearLogs(self):
        """Clears the logs array
        """

        self.logs = []

    def logError(self, err, raise_error: bool = False):
        """Logs an error or raise it

        err: str
            the error message
        raise_error: boolean
            (optional) True to raise the error instead of adding it to the logs
        """

        if raise_error:
            raise(Exception(err))
        else:
            self.log('ERROR', err)

    def logInfo(self, msg):
        """Logs an information

        msg:
            the log message
        """
        self.log('INFO', msg)

    def logWarn(self, msg):
        """Logs a warning message

        msg:
            the log message
        """
        self.log('WARNING', msg)

    def logSuccess(self, msg):
        """Logs a success message

        msg:
            the log message
        """
        self.log('SUCCESS', msg)

    def run(self, parameters, run_opt: str = '-e'):
        """
        call this method to run arg by specifying parameters and a run option

        parameters: dict
            the parameters to run arg
        run_opt: str
            (optional) -e|-g. Default -e
        """

        print("{} -> run".format(threading.currentThread().name))

        if run_opt != '-e':
            self.runner.setGOption()
        else:
            self.runner.setEOption()

        # Forward the process to the runRequested method
        self.runRequested(parameters)

        self.logSuccess("Run done.")


    def read_parameters_file(self, path: str):
        """
        Reads a parameters file from its path and returns an error if the file not valid

        path: str
            local path to the arg parameters file
        """

        print("{} -> read_parameters_file".format(threading.currentThread().name))

        self.loadedParameters = None

        try:
            # if the following method becomes async we will need to wait for it to end
            result = self.parameterController.read(path)
        except (Exception) as e:
            raise e

        if result:
            self.logSuccess("File " + os.path.basename(path) + " successfully loaded")
            return self.loadedParameters
        else:
            raise Exception("An uncaught error has occured while reading the file")


    def write_parameters_file(self, path: str, data: dict):
        """
        Writes a parameters file to its path and returns an error if the file not valid

        data: dict
            parameters to save
        """

        print("{} -> write_parameters_file".format(threading.currentThread().name))

        try:
            print('writing using argParameterController...')
            result = self.parameterController.write(path, data)
        except (Exception) as e:

            raise e

        if result:
            self.logSuccess("Parameters file saved to " + path)
            return self.parameterController.backupData
        else:
            raise Exception("An uncaught error has occured while reading the file")


    def default_arg_parameters(self) -> dict:
        """
        Returns some default arg parameters
        """

        print("{} -> default_arg_parameters".format(threading.currentThread().name))

        return {
            # Report information
            'BackendType': "LaTeX",
            'ReportType': "Report",
            'Mutables': "",
            'StructureFile': "",
            'StructureEnd': "",
            'ArtifactFile': "",
            'OutputDir': os.path.join(self.serverSettings.tmp_dir, 'output'),
            'Verbosity': 1,
            # general
            'Title': 'My Report',
            'Number': '',
            'Issue': '',
            'Versions': '',
            'Authors': '',
            'Organizations': '',
            'Location': '',
            'Year': '',
            'Month': '',
            'AbstractFile': '',
            'Preface': '',
            'Thanks': '',
            'ExecutiveSummary': '',
            'Nomenclature': '',
            'Final': True,
            'KeySeparator': '@'
        }


    def reload(self) -> dict():
        """Call the reloadRequested method and returns the backupData of the parameterController member"""
        self.loadedParameters = None

        # if the following method becomes async we will need to wait for it to end
        self.reloadRequested()

        if self.loadedParameters:
            self.logSuccess("Parameters reloaded.")
            return self.loadedParameters
        else:
            self.logWarn("No values to reload")
