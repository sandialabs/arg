#HEADER
#                      arg/web/api/application_context.py
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
import threading
import queue

from .application import Application


class ApplicationContextAction:
    """Represents an action to invoke in an application context

    run_func: Callable
        The function that will be run when calling the invoke method.
    """
    def __init__(self, run_func):
        self.run_func = run_func
        self.result = None
        self.error: Exception = None

    def raise_found_errors(self):
        """If an error has been raised during invoke it is intercepted but can be raised by this method
        This is useful to raise the error in another thread than the caller thread.
        """
        if self.error is not None:
            raise self.error

    def invoke(self):
        """Calls the run function for this action"""
        return self.run_func.__call__()


class ApplicationContext:
    """Hosts an application in a separate thread"""
    _instance = None

    @staticmethod
    def instance() -> 'ApplicationContext':
        """
        Returns a unique ApplicationContext instance
        """
        if ApplicationContext._instance is None:
            ApplicationContext._instance = ApplicationContext()
        return ApplicationContext._instance

    """Inits a new instance
    """
    def __init__(self):
        """Initialize an application context"""
        self.error: Exception = None
        self.application = None
        self._queue: queue.Queue = queue.Queue()

    def run(self, thread_name='ApplicationContext'):
        """Starts the worker thread"""
        # turn-on the worker thread
        threading.Thread(target=self.__run_impl, daemon=True, name=thread_name).start()

    def invoke(self, action: ApplicationContextAction):
        """Invoke an action in the current application context"""
        self._queue.put(action)

    def join(self):
        """Blocks until all actions have run"""
        self._queue.join()

    def __run_impl(self):
        """Run implementation of the application thread"""

        # Create an arg api application'
        print("ApplicationContext thread started : {}".format(
            threading.currentThread().name))
        self.application = Application()

        # Start infinite loop
        while True:
            # Retrieve next item in queue
            item = self._queue.get()

            # The following variable will contain the dequeued item if
            # it is an ApplicationContextAction instance
            # In that case the action will be executed in this context
            action: ApplicationContextAction = None

            # Try to set action result
            if isinstance(item, ApplicationContextAction):
                action = item
                try:
                    action.result = action.invoke()
                except Exception as e:
                    # let caller decide to fire or not the error
                    # by just putting it in a variable
                    action.error = e
            else:
                # This item is not support
                raise Exception("Item type not supported")

            # Exit infinite loop
            self._queue.task_done()
