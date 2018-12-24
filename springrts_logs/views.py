# -*- coding: utf-8 -*-

# This file is part of the "springrts logs site" program. It is published
# under the AGPLv3.
#
# Copyright (C) 2018 Daniel Troeder (daniel #at# admin-box #dot# com)
#
# You should have received a copy of the GNU Affero General Public License v3
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from django.http import Http404
from rest_framework import mixins, viewsets
from rest_framework.response import Response
from rest_framework.renderers import BrowsableAPIRenderer, JSONRenderer
from rest_framework.negotiation import DefaultContentNegotiation
from .models import Logfile, Tag
from .serializers import LogfileSerializer, TagSerializer
from .renderers import SpringLauncherLogRenderer


class SpringLauncherContentNegotiation(DefaultContentNegotiation):
    def select_renderer(self, request, renderers, format_suffix=None):
        format_query_param = self.settings.URL_FORMAT_OVERRIDE
        format = format_suffix or request.query_params.get(format_query_param)
        if format:
            renderers = self.filter_renderers(renderers, format)
        accepts = self.get_accept_list(request)

        pk = request.parser_context.get('kwargs', {}).get('pk')
        if pk:
            try:
                instance = Logfile.objects.get(pk=pk)
            except (Logfile.DoesNotExist, ValueError):
                for renderer in renderers:
                    if 'text/html' in accepts:
                        if isinstance(renderer, BrowsableAPIRenderer):
                            return renderer, 'text/html'
                    else:
                        if isinstance(renderer, JSONRenderer):
                            return renderer, 'application/json'
                raise Http404

            if format_suffix != 'api' and format != 'json' and 'text/html' in accepts:
                    if format_suffix != 'json' and instance.tags.filter(name='spring-launcher').exists():
                        for renderer in renderers:
                            if isinstance(renderer, SpringLauncherLogRenderer):
                                return renderer, 'text/html'
                        else:
                            raise RuntimeError('SpringLauncherLogRenderer not in list of renderers.')

        return super(SpringLauncherContentNegotiation, self).select_renderer(request, renderers, format_suffix)


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
    renderer_classes = (JSONRenderer, BrowsableAPIRenderer, SpringLauncherLogRenderer)
    content_negotiation_class = SpringLauncherContentNegotiation

    def list(self, request, *args, **kwargs):
        # shorten `text` in list view (not in retrieve view)
        # code copied from rest_framework.mixins.ListModelMixin.list()
        # only change is addition of text shortening
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            for logfile_repr in serializer.data:
                logfile_repr['text'] = Logfile.shorten_text(logfile_repr['text'], 200),
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        for logfile_repr in serializer.data:
            logfile_repr['text'] = Logfile.shorten_text(logfile_repr['text'], 200)
        return Response(serializer.data)

    def retrieve(self, request, format=None, *args, **kwargs):
        instance = self.get_object()

        if (
                request.accepted_renderer.format == 'html' and
                format != 'api' and
                instance.tags.filter(name='spring-launcher').exists()
        ):
            self.renderer_classes = (SpringLauncherLogRenderer,)
            return Response({'logfile': instance}, template_name='logfile_spring-launcher_detail.html')

        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    """
    `Tag` objects are automatically created and associated when creating
    `Logfile` objects through the API.

    Allowed operations: `list` and `read`.
    """
    serializer_class = TagSerializer
    queryset = Tag.objects.all()
