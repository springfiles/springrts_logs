# -*- coding: utf-8 -*-

# This file is part of the "springrts logs site" program. It is published
# under the AGPLv3.
#
# Copyright (C) 2018 Daniel Troeder (daniel #at# admin-box #dot# com)
#
# You should have received a copy of the GNU Affero General Public License v3
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from django.contrib import admin
from django.urls import include, path, re_path
from rest_framework import routers
from rest_framework.documentation import include_docs_urls
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from modernrpc.views import RPCEntryPoint
from .feeds import LatestLogfileUploadFeed
from .views import LogfileViewSet, TagViewSet


schema_view = get_schema_view(
    openapi.Info(
        title='SpringRTS Logs API',
        default_version='v1',
        description='SpringRTS Logfile Upload API',
        contact=openapi.Contact(email='daniel@admin-box.com'),
        license=openapi.License(name="AGPLv3 License"),
        # permission_classes=(permissions.AllowAny,),
    ),
    # validators=['flex', 'ssv'],
    public=True,
)

router = routers.SimpleRouter()
router.register(r'logfiles', LogfileViewSet)
router.register(r'tags', TagViewSet)

urlpatterns = [
    path(r'', include_docs_urls(title='SpringRTS Logfile Upload API')),
    path(r'', include(router.urls)),
    path(r'admin/', admin.site.urls),
    path(r'api-auth/', include('rest_framework.urls')),
    path('feed/latest/', LatestLogfileUploadFeed()),
    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path(r'rpc/', RPCEntryPoint.as_view(enable_doc=True)),
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]
