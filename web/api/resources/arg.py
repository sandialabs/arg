#HEADER
#                      arg_web/api/resources/arg.py
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

import os

from flask import request, send_file
from flask_restx import Namespace, Resource, fields
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename

from ..application_context import ApplicationContext, ApplicationContextAction

api = Namespace(
    path='/arg',
    name='Automatic Report Generator',
    description='This service enables to run arg'
)

upload_parser = api.parser()
upload_parser.add_argument('file', location='files',
                           type=FileStorage, required=True)

# arg api error handling
@api.errorhandler(Exception)
def defaultHandler(error):
    message = [str(x) for x in error.args]
    message = "\\n".join(message)
    status_code = 400
    response = {
        'message': message
    }
    return response, status_code

# init arg application context
app_context = ApplicationContext.instance()
app_context.run()

# arg parameters model
prm_data_model = api.model('data', {
    "BackendType": fields.String(),
    "ReportType": fields.String(),
    "Classification": fields.String(),
    "Mutables": fields.String(Description='Mutables file name'),
    "StructureFile": fields.String(),
    "StructureEnd": fields.String(),
    "ArtifactFile": fields.String(),
    "OutputDir": fields.String(),
    "Verbosity": fields.Integer(),
    "Title": fields.String(Description='Title of the report'),
    "Number": fields.String(),
    "Issue": fields.String(),
    "Versions": fields.String(),
    "Authors": fields.String(),
    "Organizations": fields.String(),
    "Location": fields.String(),
    "Year": fields.String(),
    "Month": fields.String(),
    "AbstractFile": fields.String(),
    "Preface": fields.String(),
    "Thanks": fields.String(),
    "ExecutiveSummary": fields.String(),
    "Nomenclature": fields.String(),
    "Final": fields.Boolean(default=False, required=True),
    "KeySeparator": fields.String(),
})

prms_run_fields = api.model('RunParameters', {
    "run_opt": fields.String(enum=['-e', '-g']),
    'parameters': fields.Nested(prm_data_model)
})


@api.route("/parameters/default", methods=["GET"])
class ParametersFileDefaultResource(Resource):

    @api.doc(description=('Reads a parameters file for arg and returns either the data result or an\
             error message'))
    def get(self):
        """Get default arg parameters which will be managed in a parameters.yml file"""
        # check if the post request has the file part
        
        action = ApplicationContextAction(lambda: app_context.application.default_arg_parameters()) 
        app_context.invoke(action)
        app_context.join()
        action.raise_found_errors()

        return action.result


@api.route("/parameters/write", methods=["POST"])
@api.expect(prm_data_model)
class ParametersFileSaveResource(Resource):
    @api.doc(summary='Saves an arg parameters file',
             description=('Saves an arg parameters file'))
    def post(self):
        """Saves an arg parameters file"""
        filename = 'saved_parameters.yml'
        dest_filepath = os.path.join(app_context.application.serverSettings.tmp_dir, filename)
        prms = request.json

        # clear previous application logs
        app_context.application.clearLogs()

        action = ApplicationContextAction(lambda: app_context.application.write_parameters_file(dest_filepath, prms)) 
        app_context.invoke(action)
        app_context.join()
        action.raise_found_errors()
        
        return send_file(filename_or_fp=dest_filepath, attachment_filename='parameters.yml')


@api.route("/parameters/read", methods=["POST"])
@api.expect(upload_parser)
class ParametersFileReadResource(Resource):

    @api.doc(summary='Reads a arg parameters file',
             description=('Reads a parameters file for arg and returns either the data result or an\
             error message'))
    def post(self):
        # check if the post request has the file part
        if 'file' not in request.files:
            raise Exception('Missing file parameter')

        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            raise Exception('No selected file')
        if file:
            filename = secure_filename(file.filename)
            print('file received: ' + file.filename)
            dest_filepath = os.path.join(app_context.application.serverSettings.tmp_dir, filename)
            file.save(dest_filepath)
            
            # clear previous application logs
            app_context.application.clearLogs()

            action = ApplicationContextAction(lambda: app_context.application.read_parameters_file(dest_filepath)) 
            app_context.invoke(action)
            app_context.join()
            action.raise_found_errors()

            return { 'parameters': action.result, 'logs': app_context.application.logs }
        else:
            raise Exception('An error has occured')


@api.route("/run", methods=["POST"])
@api.expect(prms_run_fields)
class RunResource(Resource):

    @api.doc(summary='Runs arg')
    def post(self):
        """
        Runs arg (local server)
        """
        opt = request.json['run_opt']
        prms = request.json['parameters']

        # clear previous application logs
        app_context.application.clearLogs()

        action = ApplicationContextAction(lambda: app_context.application.run(parameters=prms, run_opt=opt)) 
        app_context.invoke(action)
        app_context.join()
        action.raise_found_errors()

        return {'logs': app_context.application.logs }

@api.route("/reload", methods=["POST"])
class ReloadResource(Resource):

    @api.doc(summary='Runs arg')
    def post(self):
        """
        Reloads parameters
        """
        # clear previous application logs
        app_context.application.clearLogs()

        action = ApplicationContextAction(lambda: app_context.application.reload()) 
        app_context.invoke(action)
        app_context.join()
        action.raise_found_errors()

        return {'parameters': action.result, 'logs': app_context.application.logs }
