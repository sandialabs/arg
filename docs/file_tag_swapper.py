#HEADER
#                       docs/file_tag_swapper.py
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
import re
import shutil


class FileFinder:
    """Finds files with given extension in given directory."""

    def __init__(self, directory: str, file_extension: str):
        self.directory = os.path.abspath(directory)
        self.file_extension = file_extension

        self.files_list = None

    def get_files(self) -> list:
        """Returning found files."""
        if self.files_list is None:
            self.files_list = [f"{self.directory}/{file}" for file in os.listdir(self.directory) if
                               os.path.isfile(f"{self.directory}/{file}") if
                               os.path.splitext(file)[-1] == self.file_extension]
        return self.files_list


class TagFinder:
    """Finds given tags in given files list."""

    def __init__(self, opening_tag: str, closing_tag: str, files_list_to_look: list, source_code_dest_dir: str):
        self.opening_tag = opening_tag
        self.closing_tag = closing_tag
        self.files_list_to_look = files_list_to_look
        self.source_code_dest_dir = source_code_dest_dir

        self.pattern = f"{self.opening_tag}(.*?){self.closing_tag}"

    def __get_tag_content(self, file: str) -> tuple:
        """Returning (file, tag) tuple if tag is found in a file"""
        with open(file, 'r') as f:
            s = f.read()
            tag_match = re.search(self.pattern, s, re.DOTALL)
            if tag_match:
                return file, tag_match.group(1)

    def get_files_with_tag(self) -> list:
        """Returning list of tuples, (file, tag)"""
        files_list_to_copy = []
        for file in self.files_list_to_look:
            file_with_match = self.__get_tag_content(file)
            if file_with_match is not None:
                files_list_to_copy.append(file_with_match)
        return files_list_to_copy

    def __remove_tag_marker_in_file(self, file: str) -> None:
        """Removes first tag marker in a file and substitutes it with a production path"""
        with open(file, 'r') as f:
            s = f.read()
            pattern_match = re.search(self.pattern, s, re.DOTALL)
            first_part = s[0:pattern_match.regs[0][0]]
            last_part = s[pattern_match.regs[0][1]:]
            new_tag_content = f"/{self.source_code_dest_dir}/{pattern_match.group(1).split('/')[-1]}"
            new_md_file_content = f"{first_part}{new_tag_content}{last_part}"
        with open(file, 'w') as f:
            f.write(new_md_file_content)

    def remove_tag_marker(self):
        files_with_tag = self.get_files_with_tag()
        for file in files_with_tag:
            self.__remove_tag_marker_in_file(file[0])

    def get_list_of_files_to_copy(self) -> list:
        """Returning list of tuples (source path, destination path) of files to copy"""
        list_of_files_to_copy = []
        files_with_tag = self.get_files_with_tag()
        for path in files_with_tag:
            source_path = os.path.abspath(path[1])
            dest_path = os.path.abspath(f"{self.source_code_dest_dir}/{path[1].split('/')[-1]}")
            list_of_files_to_copy.append((source_path, dest_path))
        return list_of_files_to_copy


class FileCopier:
    """Copy files from source dir to destination directory"""

    def __init__(self, list_of_files_src_dest):
        self.list_of_files_src_dest = list_of_files_src_dest

    def __make_dest_dir(self):
        """Make directories if they don't exist"""
        file_dest_path = self.list_of_files_src_dest[0][1]
        path_depth = len(file_dest_path.split('/'))
        for path_nesting in reversed(range(1, path_depth)):
            dest_dir_path = file_dest_path.rsplit('/', path_nesting)[0]
            if dest_dir_path != '' and not os.path.exists(dest_dir_path):
                os.mkdir(dest_dir_path)

    def copy_files(self) -> None:
        """Copy files from source dir to destination directory"""
        self.__make_dest_dir()
        for paths in self.list_of_files_src_dest:
            shutil.copy(paths[0], paths[1])


class FileUrlSwapper:
    """Change string between tags 
    :param files_with_tag_dir: Directory where the files with tags are located (relative path)
    :param file_ext: Files with tags extension e.g. '.md'
    :param opn_tag: Opening tag e.g. '@@@'
    :param cls_tag: Closing tag e.g. '@@@'
    :param src_code_dest_dir: Destination directory where the source code files will be copied (relative path)
    """

    def __init__(self, files_with_tag_dir: str, file_ext: str, opn_tag: str, cls_tag: str, src_code_dest_dir: str):
        self.files_with_tag_dir = files_with_tag_dir
        self.file_ext = file_ext
        self.opn_tag = opn_tag
        self.cls_tag = cls_tag
        self.src_code_dest_dir = src_code_dest_dir

        self.tags_need_change = None

    def __check_if_tags_to_swap(self):
        ff = FileFinder(directory=self.files_with_tag_dir, file_extension=self.file_ext)
        fltl = ff.get_files()
        tf = TagFinder(opening_tag=self.opn_tag, closing_tag=self.cls_tag, files_list_to_look=fltl,
                       source_code_dest_dir=self.src_code_dest_dir)
        files_to_change = tf.get_files_with_tag()
        if files_to_change:
            self.tags_need_change = True
        else:
            self.tags_need_change = False

    def swap_tags(self):
        if self.tags_need_change is None:
            self.tags_need_change = True
        while self.tags_need_change:
            ff = FileFinder(directory=self.files_with_tag_dir, file_extension=self.file_ext)
            fltl = ff.get_files()
            tf = TagFinder(opening_tag=self.opn_tag, closing_tag=self.cls_tag, files_list_to_look=fltl,
                           source_code_dest_dir=self.src_code_dest_dir)
            files_to_copy = tf.get_list_of_files_to_copy()
            fc = FileCopier(list_of_files_src_dest=files_to_copy)
            fc.copy_files()
            tf.remove_tag_marker()
            self.__check_if_tags_to_swap()


if __name__ == "__main__":
    fus = FileUrlSwapper(files_with_tag_dir='', file_ext='.md', opn_tag='@@@', cls_tag='@@@',
                         src_code_dest_dir='source_code')
    fus.swap_tags()
