#HEADER
#                      arg/web/api/__init__.py
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

from flask import Flask, render_template, send_from_directory  # Add render_template
from flask_cors import CORS
from werkzeug.exceptions import HTTPException


def create_app(test_config=None):

    print('arg_web.api.create_app')

    # create and configure the app
    app = Flask(__name__, instance_relative_config=True, instance_path=os.path.join(
        os.path.dirname(os.path.abspath(__file__)), 'instance'))

    app.config.from_mapping(
        SECRET_KEY='dev'
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        # the configuration file cannot be applied if flask app is started from
        # the 'flask' command because flask command expects the config as environment variables)
        # Win example :
        # set FLASK_APP=api && set FLASK_DEBUG=0 && set FLASK_ENV=development
        # && set FLASK_RUN_PORT=5002 && flask run
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    if not os.path.isdir(app.instance_path):
        try:
            os.makedirs(app.instance_path)
        except OSError:
            pass

    # this is required by the latest flask version
    import werkzeug
    werkzeug.cached_property = werkzeug.utils.cached_property

    # error handling layer
    from web.api.error_handler import err
    app.register_blueprint(err)

    # load API v1
    from web.api.apiv1 import blueprint as v1
    app.register_blueprint(v1)

    @app.route('/', methods=['GET'])
    def root():
        return render_template('index.html')

    # @app.route('/static/<path>', methods=['GET'])
    # def static():
    #     return render_template('index.html')

    # enable cross origin requests
    CORS(app)

    return app


if __name__ == '__main__':
    app = create_app()
    app.run()
