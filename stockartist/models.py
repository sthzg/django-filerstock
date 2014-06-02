# -*- coding: utf-8 -*-
from __future__ import absolute_import
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django_extensions.db.models import TimeStampedModel
from filer.models import File
from filersets.models import Item


class StockPortal(models.Model):

    class Meta:
        verbose_name = _('stock portal')
        verbose_name_plural = _('stock portals')

    name = models.CharField(
        _('name'),
        max_length=40,
        blank=False,
        default=None
    )

    website = models.URLField(
        _('portal url'),
        blank=True,
        default=None,
        null=True
    )

    profile_url = models.URLField(
        _('profile page'),
        blank=True,
        default=None,
        null=True
    )

    api_id = models.CharField(
        _('api id'),
        max_length=12,
        blank=True,
        default=None,
        null=True
    )

    api_key = models.CharField(
        _('api key'),
        max_length=32,
        blank=True,
        default=None,
        null=True
    )

    def __unicode__(self):
        return u'{}'.format(self.name)


class StockLink(TimeStampedModel):

    class Meta:
        verbose_name = _('stock link')
        verbose_name_plural = _('stock links')

    file = models.ForeignKey(
        File,
        verbose_name=_('file'),
        related_name='file_stocklinks',
        blank=False,
        null=False
    )

    stock_portal = models.ForeignKey(
        StockPortal,
        verbose_name=_('stock portal'),
        related_name='portal_stocklinks',
        blank=False,
        null=False
    )

    link = models.URLField(
        _('asset link'),
        blank=False,
        null=False
    )

    def __unicode__(self):
        return u'{} | {}'.format(self.stock_portal, self.link)