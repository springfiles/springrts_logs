# -*- coding: utf-8 -*-

# This file is part of the "springrts logs site" program. It is published
# under the AGPLv3.
#
# Copyright (C) 2018 Daniel Troeder (daniel #at# admin-box #dot# com)
#
# You should have received a copy of the GNU Affero General Public License v3
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from django.contrib import admin
from .models import Logfile,Tag


class LogfileAdmin(admin.ModelAdmin):
    list_display = ('pk', 'created', 'text_short')

    @staticmethod
    def text_short(obj):
        return obj.text[:40]


class TagAdmin(admin.ModelAdmin):
    list_display = ('pk',)


admin.site.register(Logfile, LogfileAdmin)
admin.site.register(Tag, TagAdmin)
