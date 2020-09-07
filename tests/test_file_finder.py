#HEADER
#                           arg/tests/test_file_finder.py
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
from unittest import TestCase
from unittest.mock import patch, Mock

from docs.file_tag_swapper import FileFinder


class TestFileFinder(TestCase):
    @staticmethod
    def _mock_abs_path(path: str) -> str:
        return f"/test{path}"

    def setUp(self):
        os.path.abspath = Mock()
        os.path.abspath.side_effect = self._mock_abs_path

    @patch.object(os.path, 'isfile')
    @patch.object(os, 'listdir')
    def test_get_files_with_matching_files(self, listdir_mock, isfile_mock):
        listdir_mock.return_value = ['test_1.md', 'test_2.html', 'test_3.md', 'test_4.pdf', 'test_5_dir', 'test_6.md']
        isfile_mock.side_effect = [True, True, True, True, False, True]
        ff = FileFinder('', '.md')
        files_list = ff.get_files()
        self.assertEqual(files_list, ['/test/test_1.md', '/test/test_3.md', '/test/test_6.md'])

    @patch.object(os.path, 'isfile')
    @patch.object(os, 'listdir')
    def test_get_files_no_matching_files(self, listdir_mock, isfile_mock):
        listdir_mock.return_value = ['test_1.txt', 'test_2.html', 'test_3.txt', 'test_4.pdf', 'test_5_dir',
                                     'test_6.docx']
        isfile_mock.side_effect = [True, True, True, True, False, True]
        ff = FileFinder('', '.md')
        files_list = ff.get_files()
        self.assertEqual(files_list, [])

    @patch.object(os.path, 'isfile')
    @patch.object(os, 'listdir')
    def test_get_files_just_dirs(self, listdir_mock, isfile_mock):
        listdir_mock.return_value = ['test_1_dir', 'test_2_dir', 'test_3_dir', 'test_4_dir', 'test_5_dir', 'test_6_dir']
        isfile_mock.side_effect = [False, False, False, False, False, False]
        ff = FileFinder('', '.md')
        files_list = ff.get_files()
        self.assertEqual(files_list, [])
