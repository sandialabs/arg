# HEADER
#                      arg/web/api/session_manager.py
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
# HEADER

from .session import Session
import os

import uuid
from . import application


class SessionManager:
    """
    Manages sessions
    A session is currently represented by an id and a working folder with the same name in the
    sessions directory.
    """
    _sessions = {}
    LOCAL_SESSION_ID = "local"

    def __init__(self):
        self.sessions_directory = None
        self.init_session_listeners = []
        self.destroy_session_listeners = []

    def _get_session_dir(self, session_id: str):
        """Return the combination of self.sessions_directory and the session identifier"""

        return os.path.join(self.sessions_directory, session_id)

    def _load_or_create(self, id: str, mode: str = "create"):
        """Re-loads an existing session from storage or creates a new session."""

        # Check if session already loaded else create
        if mode == "load":
            loaded_session = self._get_loaded_session(id)
            if loaded_session:
                # Session was already loaded
                return loaded_session

        # Otherwise create new session
        session = Session(id)

        if mode == "create" and not os.path.isdir(self._get_session_dir(id)):
            os.mkdir(self._get_session_dir(session.id))

        # Other initialization actions from listeners
        for a in self.init_session_listeners:
            a(session)

        # Set session information
        session.directory = self._get_session_dir(id)

        # Keep session in loaded sessions in memory
        if session.id not in SessionManager._sessions:
            SessionManager._sessions[session.id] = session

        # Return created session
        return session

    def _get_loaded_session(self, id: str):
        """Retrieves an existing session which is already loaded in memory"""

        session = None
        if id in SessionManager._sessions:
            session = SessionManager._sessions[id]
        return session

    def create(self, id: str = None):
        """ Creates a new session """

        if id is None:
            id = uuid.uuid4().hex
        return self._load_or_create(id, "create")

    def get_session(self, id: str):
        """Retrieves an existing session"""

        session = self._get_loaded_session(id)
        if session is None and os.path.isdir(self._get_session_dir(id)):
            # If session unloaded then reload
            session = self._load_or_create(id, "load")
        else:
            # If an id is given then create a session with this id
            if session is None and id is not None:
                session = self._load_or_create(id, "create")
        return session

    def destroy(self, session: Session):
        """Removes a user session and removes the associated directory"""

        del SessionManager._sessions[session.id]

        session_dir = self._get_session_dir(session.id)
        if os.path.isdir(session_dir):
            os.rmdir(session_dir)

        for a in self.destroy_session_listeners:
            a(session)

        return True
