from django.conf.urls import patterns

urlpatterns = patterns('flypack.views', (r'^(?P<url>.*)$', 'flypage'))
