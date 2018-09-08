# -*- coding: utf-8 -*-

# This file is part of the "springrts logs site" program. It is published
# under the AGPLv3.
#
# Copyright (C) 2018 Daniel Troeder (daniel #at# admin-box #dot# com)
#
# You should have received a copy of the GNU Affero General Public License v3
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from six import string_types
from modernrpc.core import rpc_method
from modernrpc.exceptions import RPCInvalidParams
from .models import Logfile, Tag
from .serializers import LogfileSerializer


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
        raise RPCInvalidParams('An argument has the wrong type.')
    if tags:
        for tag in tags:
            if not isinstance(tag, string_types):
                raise RPCInvalidParams('Argument "tags" must be a list of strings.')
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
        raise RPCInvalidParams('Argument has wrong type.')
    try:
        logfile = Logfile.objects.get(pk=logfile_id)
    except Logfile.DoesNotExist:
        raise RPCInvalidParams('Logfile with ID {!r} does not exist.'.format(logfile_id))

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
        raise RPCInvalidParams('Argument has wrong type.')
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
        raise RPCInvalidParams('Argument has wrong type.')
    if name:
        kwargs = dict(name__icontains=name)
    else:
        kwargs = {}
    return list(Tag.objects.filter(**kwargs).values_list('name', flat=True))
