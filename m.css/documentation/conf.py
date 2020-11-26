# import arg.Aggregation.argAggregator as argAggregator
import arg.Applications.ARG as ARG
import arg.Applications.argExplorator as argExplorator
import arg.Applications.argGenerator as argGenerator
import arg.Applications.Explorator as Explorator
import arg.Backend.argBackendBase as argBackendBase
# import arg.Backend.argLaTeXBackend as argLaTeXBackend
# import arg.Backend.argReportLaTeXBackend as argReportLaTeXBackend
# import arg.Backend.argReportWordBackend as argReportWordBackend
import arg.Backend.argWordBackend as argWordBackend
import arg.Common.argInformationObject as argInformationObject
import arg.Common.argMath as argMath
import arg.Common.argMultiFontStringHelper as argMultiFontStringHelper
import arg.Common.argReportParameters as argReportParameters
import arg.DataInterface.argDataInterface as argDataInterface
import arg.DataInterface.argDataInterfaceBase as argDataInterfaceBase
import arg.DataInterface.argHDF5Reader as argHDF5Reader
import arg.DataInterface.argKeyValueFilesReader as argKeyValueFilesReader
import arg.DataInterface.argVTKExodusReader as argVTKExodusReader
import arg.DataInterface.argVTKSTLReader as argVTKSTLReader
import arg.Generation.argPlot as argPlot
import arg.Generation.argVTK as argVTK

PROJECT_TITLE = 'ARG (AUTOMATIC REPORT GENERATOR)'
MAIN_PROJECT_URL = 'arg/'
INPUT = '../../arg'
OUTPUT = '../docs/output'
FAVICON = '../../docs/assets/images/arg.png'
STYLESHEETS = [
    'https://fonts.googleapis.com/css?family=Source+Sans+Pro:400,400i,600,600i%7CSource+Code+Pro:400,400i,600',
    '../css/m-dark+documentation.compiled.css']
THEME_COLOR = '#22272e'
LINKS_NAVBAR1 = [('Classes', 'arg/classes.html', [])]

INPUT_MODULES = [  # argAggregator,
    ARG, argExplorator, argGenerator, Explorator, argBackendBase,
    # argLaTeXBackend, argReportLaTeXBackend, argReportWordBackend,
    argWordBackend, argInformationObject, argMath,
    argMultiFontStringHelper, argReportParameters, argDataInterface, argDataInterfaceBase,
    argHDF5Reader, argKeyValueFilesReader, argVTKExodusReader, argVTKSTLReader, argPlot, argVTK]
