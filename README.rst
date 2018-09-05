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

JSONRPC
.......
TODO

XMLRPC
......
TODO
