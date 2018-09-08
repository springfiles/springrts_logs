#!/usr/bin/env python

# This file is part of the "springrts logs site" program. It is published
# under the AGPLv3.
#
# Copyright (C) 2018 Daniel Troeder (daniel #at# admin-box #dot# com)
#
# You should have received a copy of the GNU Affero General Public License v3
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""
Django manage.py command to run the JSON-RPC server over TCP.
"""

from django.core.management.base import BaseCommand
from springrts_logs.rpc_methods import run_tcp_server


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument(
            'port',
            type=int,
            help='Port to bind to.'
        )

    def handle(self, *args, **options):
        port = options['port']
        self.stdout.write('Starting JSON-RPC server on port {}.'.format(port))
        run_tcp_server()
        self.stdout.write('JSON-RPC server stopped.')
