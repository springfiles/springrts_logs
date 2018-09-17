Spring Logs
===========

Upload service for logfile from `SpringRTS <https://springrts.com/>`_ games, clients and tools. It has a RESTish, a JSONRPC and a XMLRPC interface.

This is developed on Python 3.5 (Debian Stretch). It probably runs on newer Python versions too.

API
---

Objects
~~~~~~~
The are two object types:

* ``logfile``: The logfile. Allowed operations to unauthenticated clients: ``create``, ``list``, ``read``. Attributes:
   * ``name``: The name of the logfile (string).
   * ``text``: The content of the logfile (string).
   * ``tags``: Tags for this logfile (list of strings).
   * ``created``: The date the object was created (date, read only).
* ``tag``: A tag used on one or more logfile objects. Allowed operations to unauthenticated clients: ``list``, ``read``. Attributes:
   * ``name``: The tag (string).


Interfaces
~~~~~~~~~~

REST
....
A RESTish HTTP interface is available. Interactive online documentation is available the document root (https://dom.ain/), as well as at the resource endpoints. Additionally

The Swagger/OpenAPI generator used (`drf-yasg <https://github.com/axnsan12/drf-yasg>`_) creates only a OpenAPI version 2 schema, which does not support links in headers (v3 required). So pagination is done through entries in the JSON response body.

Documentation and schemes for client auto-generation are available:

* Swagger/OpenAPI:
   * Swagger-UI: https://dom.ain/swagger/
   * Swagger spec as JSON: https://dom.ain/swagger.json
   * Swagger spec as YAML: https://dom.ain/swagger.yaml
   * ReDoc: https://dom.ain/redoc/
* Core API: https://dom.ain/schema.js

JSON-RPC and XML-RPC over HTTP
..............................
Methods ``logfile_create``, ``logfile_get``, ``logfile_list`` and ``tag_list`` are available at https://dom.ain/rpc/ for both JSON-RPC (v2) and XML-RPC. At that URL is also a website with online documentation, when opened with a browser.

Whether to server HTML (documentation), JSON-RPC or XML-RPC is decided by the content type of the request.

(For JSON-RPC currently ``application/json`` is required and ``application/json-rpc`` is ignored. I have opened a `PR <https://github.com/alorence/django-modern-rpc/pull/25>`_ to fix this.)

XML-RPC is currently disabled.

JSON-RPC over TCP
.................
The same methods as JSON-RPC over HTTP are also available over plain TCP.

The port can be set, when starting the service via ``./manage.py runserver_jsonrpc_over_tcp <port>``


Installing
----------
* create a virtualenv for Python 3.5+
* ``pip install -U -r requirements.txt``
* setup DB, copy ``settings_local_.py`` to ``settings_local.py`` and adjust it
* ./manage.py migrate
* ``cp conf/gunicorn_logs /etc/gunicorn.d``, adjust, (re)start Gunicorn
* ``cp conf/logs_via_tcp.service /etc/systemd/system``, adjust, enable, start
* if you wish to share the cache (and thus the throttling counters) between the Django HTTP process and the JSON-RPC-over-TCP process, setup memcached and adjust the Django ``CACHES`` settings accordingly (see `Django docs <https://docs.djangoproject.com/en/2.0/topics/cache/#setting-up-the-cache>`_)

RSS feed
--------
An RSS feed listing the latest logfile uploads can be found at https://dom.ain/feed/latest/