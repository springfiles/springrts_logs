# -*- coding: utf-8 -*-

# This file is part of the "springrts logs site" program. It is published
# under the AGPLv3.
#
# Copyright (C) 2018 Daniel Troeder (daniel #at# admin-box #dot# com)
#
# You should have received a copy of the GNU Affero General Public License v3
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from django.db import models


class Tag(models.Model):
    name = models.CharField(max_length=128, primary_key=True)

    def __repr__(self):
        return "Tag({}, {})".format(self.pk, self.name)

    def __unicode__(self):
        return self.name


class Logfile(models.Model):
    name = models.CharField(max_length=2048)
    text = models.TextField()
    tags = models.ManyToManyField(Tag, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    def __repr__(self):
        return "Logfile({}, {}, {}, {})".format(
            self.pk, ','.join(self.tags.all().values_list('name', flat=True)), self.name[:20], self.text[:30]
        )

    class Meta:
        ordering = ('created',)
