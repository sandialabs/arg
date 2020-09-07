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

from flask import request
from flask_restx import Namespace, Resource, fields
import yaml
from werkzeug.exceptions import NotFound

from ..application import Application

api = Namespace(
    path='/session',
    name='Session',
    description='This service enables to run user session operations'
)


@api.route("/new")
class SessionNewResource(Resource):
    """Intialize a new empty session"""

    def get(self):
        session = Application.instance().session_manager.create()
        return {"data": session.id}


@api.route("/<id>")
class SessionResource(Resource):
    @api.errorhandler(NotFound)
    def get(self, id):
        """Get session information"""
        session = Application.instance().session_manager.get_session(id)
        if session is None:
            raise NotFound()
        else:
            return {"data": session.id}

    @api.errorhandler(NotFound)
    def delete(self, id):
        """Deletes a session. Also deletes all data stored in this session."""
        session = Application.instance().session_manager.get_session(id)
        if session is None:
            raise NotFound()
        else:
            Application.instance().session_manager.destroy(session)
