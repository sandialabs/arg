#HEADER
#                       docs/html_tag_swapper.py
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


class HtmlTagSwapper:
    def __init__(self, open_tag_cp: str, cls_tag_cp: str, file_to_copy_from: str, destination_dir: str,
                 dest_start_location: str, files_to_change_dir: str, files_to_change_start_location: str,
                 replace_inside_tag: bool = True, open_tag_rplc: str = None, cls_tag_rplc: str = None,
                 action_name: str = None):
        self.action_name = action_name
        self.file_to_copy_from = file_to_copy_from
        self.dest_start_location = dest_start_location
        self.destination_dir = f"{os.path.abspath(self.dest_start_location)}/{destination_dir}"
        self.files_to_change_start_location = files_to_change_start_location
        self.files_to_change_dir = f"{os.path.abspath(self.files_to_change_start_location)}/{files_to_change_dir}"

        self.files_to_change = None
        self.tag_needed = None
        if replace_inside_tag:
            self.replace_inside_tag = 1
        else:
            self.replace_inside_tag = 0

        self.open_tag_cp = open_tag_cp
        self.cls_tag_cp = cls_tag_cp
        if open_tag_rplc is None:
            self.open_tag_rplc = self.open_tag_cp
        else:
            self.open_tag_rplc = open_tag_rplc
        if cls_tag_rplc is None:
            self.cls_tag_rplc = self.cls_tag_cp
        else:
            self.cls_tag_rplc = cls_tag_rplc
        self.pattern_cp = f"{self.open_tag_cp}(.*?){self.cls_tag_cp}"
        self.pattern_rplc = f"{self.open_tag_rplc}(.*?){self.cls_tag_rplc}"

    def get_tag(self):
        if self.tag_needed is None:
            with open(f"{self.destination_dir}/{self.file_to_copy_from}", 'r') as html:
                s = html.read()
                self.tag_needed = re.search(self.pattern_cp, s, re.DOTALL).group(1)

    def get_files_to_change(self):
        if self.files_to_change is None:
            self.files_to_change = [file for file in os.listdir(self.files_to_change_dir) if
                                    os.path.isfile(f"{self.files_to_change_dir}/{file}") if
                                    os.path.splitext(file)[-1] == '.html']

    def change_tag_content(self):
        self.get_tag()
        self.get_files_to_change()
        for html_file in self.files_to_change:
            print('===========================================')
            print(f"=== {self.action_name} in file {html_file}")
            with open(f"{self.files_to_change_dir}/{html_file}", 'r') as html:
                s = html.read()
                pattern_match = re.search(self.pattern_rplc, s, re.DOTALL)
                first_part = s[0:pattern_match.regs[self.replace_inside_tag][0]]
                last_part = s[pattern_match.regs[self.replace_inside_tag][1]:]
                new_html_file_content = f"{first_part}{self.tag_needed}{last_part}"
            with open(f"{self.files_to_change_dir}/{html_file}", 'w') as html:
                html.write(new_html_file_content)


if __name__ == "__main__":
    hts_js = HtmlTagSwapper(action_name='Changing search menu, Adding DIV', open_tag_cp='</a>',
                            cls_tag_cp='<div id="m-navbar-collapse" class="m-col-t-12 m-show-m m-col-m-none m-right-m">',
                            file_to_copy_from='classes.html',
                            destination_dir='output', dest_start_location='', files_to_change_dir='public',
                            files_to_change_start_location='..')
    hts_js.change_tag_content()
    hts_d = HtmlTagSwapper(action_name='Changing js import, above footer', open_tag_cp='</main>', cls_tag_cp='<footer>',
                           file_to_copy_from='classes.html', destination_dir='output', dest_start_location='',
                           files_to_change_dir='public', files_to_change_start_location='..')
    hts_d.change_tag_content()
    hts_css = HtmlTagSwapper(action_name='Changing style css', open_tag_cp='''400i,600" />''', cls_tag_cp='/>',
                             file_to_copy_from='classes.html', destination_dir='output',
                             dest_start_location='', files_to_change_dir='public', files_to_change_start_location='..')
    hts_css.change_tag_content()
    hts_s = HtmlTagSwapper(action_name='Changing search menu, Changing search',
                           open_tag_cp='<ol class="m-col-t-6 m-col-m-none" start="2">', cls_tag_cp='</ol>',
                           open_tag_rplc='''<li>
              <a href="/arg/search.html" >''', cls_tag_rplc='</li>', file_to_copy_from='classes.html',
                           destination_dir='output', dest_start_location='', files_to_change_dir='public',
                           files_to_change_start_location='..', replace_inside_tag=False)
    hts_s.change_tag_content()
    hts_h = HtmlTagSwapper(action_name='Changing header', open_tag_cp='<header>',
                           cls_tag_cp='</header>', file_to_copy_from='classes.html',
                           destination_dir='public', dest_start_location='..', files_to_change_dir='output',
                           files_to_change_start_location='')
    hts_h.change_tag_content()
    hts_f = HtmlTagSwapper(action_name='Changing footer', open_tag_cp='<footer>', cls_tag_cp='</footer>',
                           file_to_copy_from='classes.html', destination_dir='public', dest_start_location='..',
                           files_to_change_dir='output', files_to_change_start_location='')
    hts_f.change_tag_content()
