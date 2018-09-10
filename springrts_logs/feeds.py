# -*- coding: utf-8 -*-

# This file is part of the "springrts logs site" program. It is published
# under the AGPLv3.
#
# Copyright (C) 2018 Daniel Troeder (daniel #at# admin-box #dot# com)
#
# You should have received a copy of the GNU Affero General Public License v3
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import re
from xml.sax.saxutils import escape as xml_escape
from django.contrib.syndication.views import Feed
from django.urls import reverse
from .models import Logfile


class LatestLogfileUploadFeed(Feed):
    title = "Logfile uploads"
    link = "/logfiles/"
    description = "Logfile uploads."

    @staticmethod
    def _escape(text):
        text = xml_escape(text)
        return re.sub(r'[\x00-\x08\x0B-\x0C\x0E-\x1F]', '', text)

    def items(self):
        return Logfile.objects.order_by('-created')[:20]

    def item_title(self, item):
        return self._escape(item.name)

    def item_description(self, item):
        return self._escape(item.text[:500])

    def item_link(self, item):
        return reverse('logfile-detail', args=[item.pk])
