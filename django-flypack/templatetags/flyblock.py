from django import template
from django.conf import settings
from django.contrib.sites.models import get_current_site
from flypack.models import Block


register = template.Library()
block_cache = []


class FlyBlockNode(template.Node):
    def __init__(self, block_name, block_code):
        self.block_name = block_name
        self.block_code = block_code

    def render(self, context):
        global block_cache
        if 'request' in context:
            site_pk = get_current_site(context['request']).pk
        else:
            site_pk = settings.SITE_ID

        if not block_cache.__len__():
            block_cache = Block.objects.filter(site=site_pk, active=1)

        result = None
        for block in block_cache:
            if block.code == self.block_code:
                result = block

        context[self.block_name] = result
        return ''


@register.tag
def get_flyblock(parser, token):
    """
    Syntax::

        {% get_flyblock ['code'] as context_name %}

    Example usage::

        {% get_flyblock 'general' as general_block %}
    """
    bits = token.split_contents()

    syntax_message = ("%(tag_name)s expects a syntax of %(tag_name)s "
                      "['code_group'] as menu_name" %
                      dict(tag_name=bits[0]))

    if len(bits) == 2 or len(bits) == 4:
        block_code = bits[1]

        if bits[-2] != 'as':
            block_name = bits[1]
        else:
            block_name = bits[-1]

        return FlyBlockNode(block_name, block_code)
    else:
        raise template.TemplateSyntaxError(syntax_message)