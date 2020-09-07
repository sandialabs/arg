#HEADER
#                      arg_web/api/resources/server.py
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

from flask_restx import Namespace, Resource, fields
import os
from flask import request
from werkzeug.exceptions import HTTPException, NotFound, Forbidden
import yaml

api = Namespace(path='/server', name='Server',
                description='This service enables to run some server operations')


@api.route("/hello/<username>")
class HelloResource(Resource):
    """Simple resource to check the server and the api availablility"""
    @api.doc(
        description='This endpoint returns a hello message to a user useful to verify that the '
                    'server is connected and ready, otherwise you will receive an http error code',
        params={'username': 'The name of the user'})
    def get(self, username):
        """Test server presence by requesting a hello response"""
        return {"message": 'Hello, ' + username + '!'}


stop_server_query_parser = api.parser()
stop_server_query_parser.add_argument('key', required=True, type=str)


@api.route('/shutdown')
@api.expect(stop_server_query_parser)
@api.errorhandler(Forbidden)
class StopResource(Resource):

    def get(self):
        """Shutdown the server.
        To use only if the server is managed by the client app.
        When starting the server provide the following environment variable :
            ARG_API_SERVER_STOP_KEY=[WHATEVER YOU WANT]
        You will then need to pass this key when calling this method.
        """

        
        # Try to retrieve key from arguments
        args = stop_server_query_parser.parse_args()
        key = args.get("key")
        if key:
            # Look for stop key in environment
            if os.environ.get("ARG_API_SERVER_STOP_KEY") == key:
                # Retrieve function
                func = request.environ.get("werkzeug.server.shutdown")
                if func is None:
                    raise RuntimeError("Not running with the Werkzeug Server")

                # Execute function
                func()
            else:
                # Raise forbidden exception
                raise Forbidden()
        else:
            # Raise forbidden exception
            raise Forbidden()
