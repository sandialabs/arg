#HEADER
#                           arg/tests/test_tag_finder.py
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
import random
import string
from unittest import TestCase
from unittest.mock import patch

from docs.file_tag_swapper import TagFinder


class TestTagFinder(TestCase):
    LIST_OF_FILES = ['test_1.md', 'test_2.md', 'test_3.md', 'test_4.md', 'test_5.md']

    @staticmethod
    def _mock_abs_path(path: str) -> str:
        return f"{path}"

    @staticmethod
    def get_random_string():
        letters = string.ascii_lowercase
        str_length = random.randint(250, 400)
        result_str = ''.join(random.choice(letters) for i in range(str_length))
        return result_str

    def create_files_with_markers(self, opn_tag, cls_tag, list_of_files):
        tag_list = [f"{opn_tag}test_{arg_num}.md{cls_tag}" for arg_num, col in enumerate(list_of_files, start=1)]
        for ind, file in enumerate(list_of_files):
            if ind % 2 == 0:
                with open(file, 'w') as f:
                    f.write(self.get_random_string())
                    f.write(tag_list[ind])
                    f.write(self.get_random_string())
            else:
                with open(file, 'w') as f:
                    f.write(self.get_random_string())
                    f.write(self.get_random_string())
                    f.write(self.get_random_string())

    @staticmethod
    def delete_files_with_markers(list_of_files):
        for file in list_of_files:
            os.remove(file)

    def setUp(self) -> None:
        self.create_files_with_markers(opn_tag='@@@', cls_tag='@@@', list_of_files=self.LIST_OF_FILES)

    def test_get_files_with_tag(self):
        tg = TagFinder(opening_tag='@@@', closing_tag='@@@', files_list_to_look=self.LIST_OF_FILES,
                       source_code_dest_dir='')
        list_with_tags = tg.get_files_with_tag()
        self.assertEqual(list_with_tags,
                         [('test_1.md', 'test_1.md'), ('test_3.md', 'test_3.md'), ('test_5.md', 'test_5.md')])

    @patch.object(os.path, 'abspath')
    def test_get_list_of_files_to_copy(self, abspath_mock):
        abspath_mock.side_effect = self._mock_abs_path
        tg = TagFinder(opening_tag='@@@', closing_tag='@@@', files_list_to_look=self.LIST_OF_FILES,
                       source_code_dest_dir='/test')
        list_of_files_to_copy = tg.get_list_of_files_to_copy()
        self.assertEqual(list_of_files_to_copy,
                         [('test_1.md', '/test/test_1.md'), ('test_3.md', '/test/test_3.md'),
                          ('test_5.md', '/test/test_5.md')])

    def test_remove_tag_marker(self):
        tg = TagFinder(opening_tag='@@@', closing_tag='@@@', files_list_to_look=self.LIST_OF_FILES,
                       source_code_dest_dir='/test')
        tg.remove_tag_marker()
        list_with_tags_after_removal = tg.get_files_with_tag()
        self.assertEqual(list_with_tags_after_removal, [])

    def tearDown(self) -> None:
        self.delete_files_with_markers(list_of_files=self.LIST_OF_FILES)
