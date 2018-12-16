# -*- coding: utf-8 -*-

# This file is part of the "springrts logs site" program. It is published
# under the AGPLv3.
#
# Copyright (C) 2018 Daniel Troeder (daniel #at# admin-box #dot# com)
#
# You should have received a copy of the GNU Affero General Public License v3
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import re
from rest_framework import renderers
from django.shortcuts import render as django_render


class SpringBoardLogRenderer(renderers.BaseRenderer):
    media_type = 'text/html'
    format = 'html'
    charset = 'utf-8'

    line_start_regex = re.compile(r'\[\d\d\d\d-\d\d-\d\d \d\d:\d\d:\d\d.\d\d\d\]')
    date_regex = re.compile(r'^\[\d\d\d\d-\d\d-\d\d \d\d:\d\d:\d\d.\d\d\d\] \[(\w+?)\]')
    lvl2css = {
        'info': 'default',
        'error': 'danger',
        'warn': 'warning',
    }

    def render(self, data, media_type=None, renderer_context=None):
        text = data['logfile'].text
        end = 0
        dates = []
        texts = []
        for m in self.line_start_regex.finditer(text, re.MULTILINE | re.DOTALL):
            if m.start() > 0:
                dates.append(text[m.start():m.end()])
                texts.append(text[end:m.start()].strip())
                end = m.end()
        texts.append(text[end:].strip())
        lines = [texts[0]] + ['{} {}'.format(dates[i], texts[i+1]) for i in range(len(dates))]
        data['lines'] = []
        for line in lines:
            m = self.date_regex.match(line)
            try:
                debug_level = m.groups()[0]
            except IndexError:
                debug_level = 'info'
            # this should really be done in the template, but it is easier here:
            try:
                css_class = self.lvl2css[debug_level]
            except KeyError:
                css_class = self.lvl2css['info']
            data['lines'].append((css_class, line))
        return django_render(renderer_context['request'], 'logfile_SpringBoard_detail.html', data)
