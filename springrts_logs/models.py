# -*- coding: utf-8 -*-

# This file is part of the "springrts logs site" program. It is published
# under the AGPLv3.
#
# Copyright (C) 2018 Daniel Troeder (daniel #at# admin-box #dot# com)
#
# You should have received a copy of the GNU Affero General Public License v3
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from typing import Dict
from django.db import models
from django.urls import reverse
from django.conf import settings
from rest_framework.reverse import reverse
from rest_hooks.signals import hook_event


class Tag(models.Model):
    name = models.CharField(max_length=128, primary_key=True)

    def __repr__(self):
        return "Tag({}, {})".format(self.pk, self.name)

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('tag-detail', kwargs={'pk': str(self.name)})


class Logfile(models.Model):
    name = models.CharField(max_length=2048)
    text = models.TextField()
    tags = models.ManyToManyField(Tag, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    def __repr__(self):
        return "Logfile({}, {}, {}, {})".format(
            self.pk, ','.join(self.tags.all().values_list('name', flat=True)), self.name[:20], self.text[:30]
        )

    def to_dict(self) -> Dict[str, str]:
        return {
            'name': self.name,
            'text': self.text,
            'tags': list(self.tags.all().values_list('name', flat=True)),
            'created': str(self.created),
        }

    @property
    def short_text(self) -> str:
        return self.shorten_text(self.text, 500)

    @staticmethod
    def shorten_text(text: str, length: int) -> str:
        if length < len(text):
            return '{}\n({} characters truncated)'.format(text[:length], len(text[length:]))
        else:
            return text

    def serialize_hook(self, hook):
        return {
            'hook': hook.dict(),
            'data': {
                'id': self.pk,
                'name': self.name,
                'text': self.text,
                'tags': list(self.tags.values_list(flat=True)),
                'created': self.created,
        }
    }

    def created_with_tags(self, tags):
        """
        Custom event for webhook. Builtin "created" event is to early, because
        the tags get attached _after_ the creation.

        :param list(str) tags: list of tags
        """
        for tag in set(tags).intersection(set(settings.LOGFILE_TAG_TO_EVENT.keys())):
            action = settings.LOGFILE_TAG_TO_EVENT[tag][1]
            action = action.replace('springrts_logs.Logfile.', '').strip('+')
            hook_event.send(
                sender=self.__class__,
                action=action,
                instance=self,
                user_override=False
            )

    class Meta:
        ordering = ('created',)
