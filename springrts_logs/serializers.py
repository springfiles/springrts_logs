# -*- coding: utf-8 -*-

# This file is part of the "springrts logs site" program. It is published
# under the AGPLv3.
#
# Copyright (C) 2018 Daniel Troeder (daniel #at# admin-box #dot# com)
#
# You should have received a copy of the GNU Affero General Public License v3
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import magic
from rest_framework import serializers
from rest_framework.reverse import reverse
from .models import Logfile, Tag


class LogfileSerializer(serializers.HyperlinkedModelSerializer):
    # The default serializer would require the user to submit URLs to existing
    # Tag objects (as its a ManyToManyField). To make the API easier to use,
    # we'll allow a list of strings as input and make the connection ourselves.
    tags = serializers.ListSerializer(child=serializers.CharField(), allow_empty=True, required=False)

    class Meta:
        model = Logfile
        fields = ('url', 'name', 'text', 'tags', 'created')
        read_only_fields = ('created',)

    def create(self, validated_data):
        return self.create_logfile(**validated_data)

    @staticmethod
    def create_logfile(name, text, tags=None):
        logfile = Logfile.objects.create(name=name, text=text)
        if tags:
            tags = [t.strip() for t in tags if t.strip()]
            tag_pks = [Tag.objects.get_or_create(name=tag)[0].pk for tag in tags]
            logfile.tags.add(*tag_pks)
        return logfile

    def to_representation(self, instance):
        # Replace the list of Tag repr strings with the list of Tag names.
        res = super().to_representation(instance)
        res['tags'] = list(instance.tags.all().values_list('name', flat=True))
        return res

    @staticmethod
    def validate_text(value):
        mime_type = magic.from_buffer(value[:200], mime=True)
        if not mime_type.startswith('text/'):
            raise serializers.ValidationError("Content type of 'text' argument must be 'text/*', detected {!r}.".format(
                mime_type))
        return value


class TagSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Tag
        fields = ('url', 'name')
        read_only_fields = ('name',)

    def to_representation(self, instance):
        res = super().to_representation(instance)
        logfile_pks = Logfile.objects.filter(tags=instance).values_list('pk', flat=True)
        res['logfiles'] = [
            reverse('logfile-detail', kwargs={'pk': pk}, request=self.context['request'])
            for pk in logfile_pks
        ]
        return res
