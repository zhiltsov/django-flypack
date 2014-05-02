# -*- coding: utf-8 -*-

from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.db import models
from django.conf import settings


class Page(models.Model):
    code = models.SlugField(db_index=True)
    parent = models.ForeignKey('self', null=True, blank=True)
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=200, blank=True)
    keywords = models.CharField(max_length=255, blank=True)
    text = models.TextField(blank=True)
    active = models.BooleanField(default=1, db_index=True)
    template_name = models.CharField(max_length=70,
                                     choices=settings.PUBLIC_TEMPLATES,
                                     default=settings.DEFAULT_TEMPLATE)
    date_create = models.DateTimeField(auto_now_add=True, editable=False)
    date_update = models.DateTimeField(auto_now=True, editable=False)
    updated_by = models.ForeignKey(User, related_name='+', editable=False, null=True, on_delete=models.SET_NULL)
    site = models.ForeignKey(Site)

    class Meta:
        ordering = ['code']
        unique_together = (('code', 'parent', 'site'),)
        index_together = [
            ['code', 'active', 'site'],
        ]

    def __unicode__(self):
        return u'[%s] %s' % (self.code, self.title)

    def get_absolute_url(self):
        url = '/'
        if self.parent is None and self.code != 'index':
            url += self.code + '/'
        elif self.parent is not None:
            url = Page.objects.get(pk=self.parent.pk).get_absolute_url() + self.code + url
        return url


class Block(models.Model):
    code = models.SlugField(db_index=True)
    text = models.TextField(blank=True)
    active = models.BooleanField(default=1, db_index=True)
    date_create = models.DateTimeField(auto_now_add=True, editable=False)
    date_update = models.DateTimeField(auto_now=True, editable=False)
    updated_by = models.ForeignKey(User, related_name='+', editable=False, null=True, on_delete=models.SET_NULL)
    site = models.ForeignKey(Site)

    class Meta:
        ordering = ['code']
        unique_together = (('code', 'site'),)
        index_together = [
            ['code', 'active', 'site'],
        ]

    def __unicode__(self):
        return self.code


class Menu:
    title = None
    url = None
    parent = None
    selected = False

    def __init__(self, title, url):
        self.title = title
        self.url = url

    def __hash__(self):
        return hash(self.__class__.__name__ + str(self.url))


class MenuGroup(models.Model):
    site = models.ForeignKey(Site)
    code = models.SlugField(max_length=20, unique=True, db_index=True)
    title = models.CharField(max_length=50)

    def __unicode__(self):
        return u'[%s] %s' % (self.code, self.title)

    def __hash__(self):
        return hash(self.__class__.__name__ + str(self._get_pk_val()))


class MenuItem(models.Model):
    group = models.ForeignKey(MenuGroup)
    parent = models.ForeignKey('self', null=True, blank=True)
    sort = models.SmallIntegerField(default=500)
    title = models.CharField(max_length=50)
    url = models.CharField(max_length=255)
    extended = models.SlugField(blank=True, choices=settings.FLYMENU_EXTENDED)

    class Meta:
        ordering = ['sort']

    def __unicode__(self):
        return self.title

    def __hash__(self):
        return hash(self.__class__.__name__ + str(self._get_pk_val()))