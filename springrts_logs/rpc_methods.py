# -*- coding: utf-8 -*-

# This file is part of the "springrts logs site" program. It is published
# under the AGPLv3.
#
# Copyright (C) 2018 Daniel Troeder (daniel #at# admin-box #dot# com)
#
# You should have received a copy of the GNU Affero General Public License v3
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import asyncio
import asyncore
import signal
from six import string_types
from modernrpc.core import rpc_method
from modernrpc.exceptions import RPCInvalidParams
from jsonrpcserver.aio import AsyncMethods
from jsonrpcserver.exceptions import InvalidParams, MethodNotFound, ParseError
from jsonrpcserver.response import ExceptionResponse
from rest_framework.throttling import AnonRateThrottle
from rest_framework.exceptions import Throttled
from .models import Logfile, Tag
from .serializers import LogfileSerializer


InvalidParamsException = RPCInvalidParams  # plain TCP server will set this to InvalidParams


@rpc_method
def logfile_create(name, text, tags=None):
    """
    Create a logfile object.

    :param name: the name of the logfile being uploaded
    :type name: str
    :param text: the content of the logfile
    :type text: str
    :param tags: a optional list of strings
    :type tags: list[str]
    :return: the ID of the created logfile object
    :rtype: int
    """
    if not isinstance(name, string_types) or not isinstance(text, string_types) or not (isinstance(tags, list) or tags is None):
        raise InvalidParamsException('An argument has the wrong type.')
    if tags:
        for tag in tags:
            if not isinstance(tag, string_types):
                raise InvalidParamsException('Argument "tags" must be a list of strings.')
    return LogfileSerializer.create_logfile(name, text, tags).pk


@rpc_method
def logfile_get(logfile_id):
    """
    Retrieve an existing logfile object.

    The ID is one returned by ``logfile_create`` and ``logfile_list``.
    Keys in the returned dict are: ``name``, ``text``, ``tags``, ``created``.

    :param logfile_id: the ID of the logfile object
    :type logfile_id: int
    :return: dict representation of logfile object
    :rtype: dict
    """
    if not isinstance(logfile_id, int):
        raise InvalidParamsException('Argument has wrong type.')
    try:
        logfile = Logfile.objects.get(pk=logfile_id)
    except Logfile.DoesNotExist:
        raise InvalidParamsException('Logfile with ID {!r} does not exist.'.format(logfile_id))

    return logfile.to_dict()


@rpc_method
def logfile_list(name=None, **kwargs):
    """
    List existing logfile objects.

    When the ``name`` argument is used, a *case insensitive search* is done for
    logfile objects with a name *containing* the argument.

    :param name: optional case insensitive name search for logfile objects
    :type name: str
    :return: list of [ID, name] pairs
    :rtype: list[[int, str], ..]
    """
    if not (isinstance(name, string_types) or name is None):
        raise InvalidParamsException('Argument has wrong type.')
    if name:
        kwargs = dict(name__icontains=name)
    else:
        kwargs = {}
    return list(Logfile.objects.filter(**kwargs).values_list('id', 'name'))


@rpc_method
def tag_list(name=None):
    """
    List existing tag objects.

    When the ``name`` argument is used, a *case insensitive search* is done for
    name objects with a name *containing* the argument.

    :param name: optional case insensitive name search for tag objects
    :type name: str
    :return: list of tags names
    :rtype: list[str]
    """
    if not (isinstance(name, string_types) or name is None):
        raise InvalidParamsException('Argument has wrong type.')
    if name:
        kwargs = dict(name__icontains=name)
    else:
        kwargs = {}
    return list(Tag.objects.filter(**kwargs).values_list('name', flat=True))


class FakeRequest(object):
    class FakeUser(object):
        is_authenticated = False

    def __init__(self, ip):
        self.user = self.FakeUser()
        self.ip = ip


class JsonTcpAnonRateThrottle(AnonRateThrottle):
    def get_ident(self, request):
        """
        Identify the machine making the request.
        """
        if isinstance(request, FakeRequest):
            return request.ip
        else:
            return super(JsonTcpAnonRateThrottle, self).get_ident(request)


async def _logfile_create_async(name, text, tags=None):
    return logfile_create(name, text, tags)


async def _logfile_get_async(logfile_id):
    return logfile_get(logfile_id)


async def _logfile_list_async(name=None):
    return logfile_list(name)


async def _tag_list_async(name=None):
    return tag_list(name)


async def _handle_request(reader, writer):
    from .views import LogfileViewSet  # cannot import this at the top, it'd cause a circular dependency
    # check rate limiting
    peer = writer.get_extra_info('socket').getpeername()
    fdr = FakeRequest(peer[0])
    lfvs = LogfileViewSet()
    try:
        lfvs.check_throttles(fdr)
    except Throttled as exc:
        # There is no error code for "permission denied" or the like in the
        # JSON-RPC spec, so using "Method not available" as it's somewhat
        # true (although it usually means that no method with the requested
        # methods name exists).
        json_exc = MethodNotFound(str(exc))
        json_exc.message = str(exc)
        response_obj = ExceptionResponse(json_exc, None)
        response = str(response_obj).encode('utf-8')
        writer.write(response)
        return

    methods = AsyncMethods(
        logfile_create=lambda name, text, tags=None: _logfile_create_async(name, text, tags),
        logfile_get=lambda logfile_id: _logfile_get_async(logfile_id),
        logfile_list=lambda name=None: _logfile_list_async(name),
        tag_list=lambda name=None: _tag_list_async(name),
    )
    while True:
        request_raw = await reader.readline()
        if not request_raw:
            break
        try:
            request_str = request_raw.decode('utf-8')
        except UnicodeDecodeError:
            raise ParseError('Error parsing request.')
        response_obj = await methods.dispatch(request_str)
        response = str(response_obj).encode('utf-8')
        writer.write(response)


def _term_handler(signum, frame):
    raise asyncore.ExitNow('SIGTERM received')


def run_tcp_server():
    global InvalidParamsException
    InvalidParamsException = InvalidParams
    loop = asyncio.get_event_loop()
    server = asyncio.start_server(_handle_request, loop=loop, port=5555)
    server = loop.run_until_complete(server)
    signal.signal(signal.SIGTERM, _term_handler)
    try:
        loop.run_forever()
    except (KeyboardInterrupt, asyncore.ExitNow):
        pass
