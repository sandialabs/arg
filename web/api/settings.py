#HEADER
#                      arg/web/api/settings.py
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
import yaml
import os


class ServerSettings:
    """Class to represent the flask server and api settings"""

    def __init__(self):
        """Initializes a new settings object. Please load config before using."""
        self.shared_dir = os.path.join(
                    os.path.dirname(__file__), 'instance', 'shared')
        self.tmp_dir = os.path.join(
                    os.path.dirname(__file__), 'instance', 'tmp')
        self.sessions_dir = os.path.join(
                    os.path.dirname(__file__), 'instance', 'sessions')

    def make_dirs(self):
        """Creates the tmp, shared and sessions directories if it does not exist and all required
        intermediate required non-existing folders"""
        if not os.path.isdir(self.sessions_dir):
            os.makedirs(self.sessions_dir)
        if not os.path.isdir(self.shared_dir):
            os.makedirs(self.shared_dir)
        if not os.path.isdir(self.tmp_dir):
            os.makedirs(self.tmp_dir)

    def from_file(self, filepath):
        """Loads API configuration from a yaml file.

        filepath:
            The path to the file. This file must be in yaml format and may contain the following
            entries:
            SESSION_DIRECTORY: the directory where user sessions will be stores
            ARG_PATH: the absolute path to the arg module
        """

        # pParse configuration file
        with open(filepath, 'r') as stream:
            data = yaml.safe_load(stream)
            if not data:
                return

            # Attempt to retrieve optional app name
            self.app_name = data.get('APP_NAME', '')

            # Attempt to update other parameters
            if 'SHARED_DIRECTORY' in data:
                self.sessions_dir = data['SHARED_DIRECTORY']
            if 'TMP_DIRECTORY' in data:
                self.sessions_dir = data['TMP_DIRECTORY']
            if 'SESSION_DIRECTORY' in data:
                self.sessions_dir = data['SESSION_DIRECTORY']
