# -*- coding: utf-8 -*-

# This file is part of the "springrts logs site" program. It is published
# under the AGPLv3.
#
# Copyright (C) 2018 Daniel Troeder (daniel #at# admin-box #dot# com)
#
# You should have received a copy of the GNU Affero General Public License v3
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from rest_framework import mixins, viewsets
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


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    """
    `Tag` objects are automatically created and associated when creating
    `Logfile` objects through the API.

    Allowed operations: `list` and `read`.
    """
    serializer_class = TagSerializer
    queryset = Tag.objects.all()
