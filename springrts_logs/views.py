# -*- coding: utf-8 -*-

# This file is part of the "springrts logs site" program. It is published
# under the AGPLv3.
#
# Copyright (C) 2018 Daniel Troeder (daniel #at# admin-box #dot# com)
#
# You should have received a copy of the GNU Affero General Public License v3
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from rest_framework import mixins, viewsets
from rest_framework.response import Response
from .models import Logfile, Tag
from .serializers import LogfileSerializer, TagSerializer


class LogfileViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """
    When creating a `Logfile` object the `name`, `text` and `tags` attributes
    can be set. The `created` attribute will be automatically created.

    The `tags` attribute is a list of strings. The API will automatically
    create and associate `Tag` objects from those.

    Allowed operations: `create`, `list` and `read`.
    """
    serializer_class = LogfileSerializer
    queryset = Logfile.objects.all()

    def list(self, request, *args, **kwargs):
        # shorten `text` in list view (not in retrieve view)
        # code copied from rest_framework.mixins.ListModelMixin.list()
        # only change is addition of text shortening
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            for logfile_repr in serializer.data:
                logfile_repr['text'] = logfile_repr['text'][:200]
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        for logfile_repr in serializer.data:
            logfile_repr['text'] = logfile_repr['text'][:200]
        return Response(serializer.data)


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    """
    `Tag` objects are automatically created and associated when creating
    `Logfile` objects through the API.

    Allowed operations: `list` and `read`.
    """
    serializer_class = TagSerializer
    queryset = Tag.objects.all()
