from django.contrib import admin
from flypack.models import *


class PageAdmin(admin.ModelAdmin):
    list_display = ('id', 'active', 'parent', 'code', 'title', 'date_create', 'date_update', 'updated_by', 'site')
    search_fields = ('code', 'title')
    list_filter = ('site__name', 'active', 'date_create', 'date_update')
    ordering = ('site', 'code')


class BlockAdmin(admin.ModelAdmin):
    list_display = ('id', 'active', 'code', 'site')
    search_fields = ('code',)
    list_filter = ('site__name', 'active')
    ordering = ('site', 'code')


class MenuGroupAdmin(admin.ModelAdmin):
    list_display = ('id', 'code', 'title', 'site')


class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'sort', 'group', 'parent', 'title', 'url')

admin.site.register(Page, PageAdmin)
admin.site.register(Block, BlockAdmin)
admin.site.register(MenuGroup, MenuGroupAdmin)
admin.site.register(MenuItem, MenuItemAdmin)