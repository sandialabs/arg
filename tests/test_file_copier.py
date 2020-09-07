#HEADER
#                           arg/tests/test_file_copier.py
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
import shutil
from unittest import TestCase

from docs.file_tag_swapper import FileCopier


class TestFileCopier(TestCase):
    LIST_OF_FILES = [('test_1.md', '/test/test_1.md'), ('test_2.md', '/test/test_2.md'),
                     ('test_3.md', '/test/test_3.md')]

    @staticmethod
    def create_files_to_copy(list_of_files):
        for file in list_of_files:
            with open(file[0], 'w') as f:
                f.write(file[0])

    @staticmethod
    def delete_files_to_copy(list_of_files):
        for file in list_of_files:
            os.remove(file[0])

    @staticmethod
    def delete_copied_files(list_of_files):
        dir_to_delete = list_of_files[0][1].split('/')[1]
        shutil.rmtree(f"{dir_to_delete}")

    @staticmethod
    def prepare_list_of_files(list_to_change):
        prepared_list = [(os.path.abspath(file[0]), os.path.abspath(file[1][1:])) for file in list_to_change]
        return prepared_list

    def setUp(self) -> None:
        self.create_files_to_copy(list_of_files=self.LIST_OF_FILES)

    def test_copy_files(self):
        ls_fl_src_dest = self.prepare_list_of_files(self.LIST_OF_FILES)
        fc = FileCopier(list_of_files_src_dest=ls_fl_src_dest)
        fc.copy_files()
        dir_created = os.path.abspath(self.LIST_OF_FILES[0][1].split('/')[1])
        self.assertTrue(dir_created)
        for file in ls_fl_src_dest:
            self.assertTrue(os.path.isfile(file[1]))

    def tearDown(self) -> None:
        self.delete_files_to_copy(list_of_files=self.LIST_OF_FILES)
        self.delete_copied_files(list_of_files=self.LIST_OF_FILES)
