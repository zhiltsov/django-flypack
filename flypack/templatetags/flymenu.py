# -*- coding: utf-8 -*-

from django import template
from django.conf import settings
from django.contrib.sites.models import get_current_site
from django.http import Http404
from flypack.models import Menu, MenuItem, Page


register = template.Library()


class FlyMenuNode(template.Node):
    """
    Вывод древовидного меню
    """
    def __init__(self, menu_name, menu_code):
        self.menu_name = menu_name
        self.menu_code = menu_code

    def render(self, context):
        request = None
        if 'request' in context:
            request = context['request']
            site_pk = get_current_site(request).pk
        else:
            site_pk = settings.SITE_ID

        flymenu = MenuItem.objects.filter(group__site=site_pk, group__code=self.menu_code)

        items = []
        item_objects = {}

        try:
            for menu in flymenu:
                item = Menu(menu.title, menu.url)
                item.id = menu.pk

                if menu.parent:
                    key = menu.parent.__hash__()
                    if key in item_objects.keys():
                        item.parent = item_objects[key]
                    else:
                        item.parent = item_objects[key] = Menu(menu.parent.title, menu.parent.url)

                if request is not None and request.path == item.url:
                    item.selected = True
                    if item.parent:
                        item.parent.selected = True

                item_objects[menu.__hash__()] = item

                # Подгрузка динамического меню
                if menu.extended:
                    for item_ext in eval(menu.extended):
                        if item_ext.parent is None:
                            item_ext.parent = item

                        if request is not None and request.path == item_ext.url:
                            item_ext.selected = True
                            item_ext.parent.selected = True

                        item_objects[item_ext.__hash__()] = item_ext

            # Собираем во едино
            for k in item_objects.keys():
                items.append(item_objects[k])

        except Page.DoesNotExist:
            raise Http404('Page Not Found: code %s' % self.menu_code)

        context[self.menu_name] = items
        return ''


@register.tag
def get_flymenu(parser, token):
    """
    Syntax::

        {% get_flymenu ['code group'] as context_name %}

    Example usage::

        {% get_flymenu 'general' as general_menu %}
    """
    bits = token.split_contents()

    syntax_message = ("%(tag_name)s expects a syntax of %(tag_name)s "
                      "['code_group'] as menu_name" %
                      dict(tag_name=bits[0]))

    if len(bits) == 4:
        menu_code = bits[1]

        if bits[-2] != 'as':
            raise template.TemplateSyntaxError(syntax_message)
        menu_name = bits[-1]

        return FlyMenuNode(menu_name, menu_code)
    else:
        raise template.TemplateSyntaxError(syntax_message)