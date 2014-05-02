from django.conf import settings
from django.contrib.sites.models import get_current_site
from django.core.xheaders import populate_xheaders
from django.http import Http404, HttpResponse, HttpResponsePermanentRedirect
from django.shortcuts import get_object_or_404
from django.template import loader, RequestContext
from django.utils.safestring import mark_safe
from flypack.models import Page


def flypage(request, url):
    site_id = get_current_site(request).id
    page = Page
    parent = None

    path = url.split('/')

    if not url.endswith('/') and url != u'' and settings.APPEND_SLASH:
        return HttpResponsePermanentRedirect('%s/' % request.path)

    if path.count > 0 and path[-1] == u'':
        del path[-1]

    if url == u'' or (path.count == 1 and path[0] == u''):
        path = ['index']

    try:
        for folder in path:
            f = get_object_or_404(Page, code__iexact=folder, active=1, site__id__exact=site_id, parent__exact=parent)
            parent = f.pk
            page = f
    except Http404:
        raise

    return render_flypage(request, page)


def render_flypage(request, f):
    if f.template_name:
        t = loader.select_template((f.template_name, settings.DEFAULT_TEMPLATE))
    else:
        t = loader.get_template(settings.DEFAULT_TEMPLATE)

    f.title = mark_safe(f.title)
    f.text = mark_safe(f.text)

    c = RequestContext(request, {
        'title': f.title,
        'content': f.text,
        'description': f.description,
        'keywords': f.keywords,
        'flypage': f,
        'request': request,
    })
    response = HttpResponse(t.render(c))
    populate_xheaders(request, response, Page, f.id)
    return response