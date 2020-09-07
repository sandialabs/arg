#HEADER
#                           arg/tests/test_file_tag_swapper.py
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
import shutil
import string
from unittest import TestCase

from docs.file_tag_swapper import FileFinder, FileUrlSwapper, TagFinder


class TestFileTagSwapper(TestCase):
    LIST_OF_FILES = ['test_1.md', 'test_2.md', 'test_3.md', 'test_4.html', 'test_5.html', 'test_6.md']

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
    def delete_files_to_copy(list_of_files):
        for file in list_of_files:
            os.remove(file)

    @staticmethod
    def delete_copied_files():
        shutil.rmtree('test')

    def setUp(self) -> None:
        self.create_files_with_markers(opn_tag='@@@', cls_tag='@@@', list_of_files=self.LIST_OF_FILES)

    def test_swap_tags(self):
        fus = FileUrlSwapper(files_with_tag_dir='.', file_ext='.md', opn_tag='@@@', cls_tag='@@@',
                             src_code_dest_dir='test')
        fus.swap_tags()
        list_of_files = FileFinder(directory='', file_extension='.md').get_files()
        list_of_files_with_markers = TagFinder(opening_tag='@@@', closing_tag='@@@', files_list_to_look=list_of_files,
                                               source_code_dest_dir='test').get_files_with_tag()
        self.assertEqual(list_of_files_with_markers, [])
        list_of_expected_files = ['test/test_1.md', 'test/test_3.md']
        for file in list_of_expected_files:
            self.assertTrue(os.path.isfile(file))

    def tearDown(self) -> None:
        self.delete_files_to_copy(list_of_files=self.LIST_OF_FILES)
        self.delete_copied_files()
