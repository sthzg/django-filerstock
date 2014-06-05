# -*- coding: utf-8 -*-
# ______________________________________________________________________________
#                                                                         Future
from __future__ import absolute_import
# ______________________________________________________________________________
#                                                                         Django
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from django.contrib.admin.options import TabularInline, ModelAdmin
# ______________________________________________________________________________
#                                                                        Contrib
from filer.admin import ImageAdmin
from filer.models import Image
# ______________________________________________________________________________
#                                                                         Custom
from filersets.admin import ItemAdmin
from filersets.models import Item
from stockartist.models import StockLink, StockPortal
# ______________________________________________________________________________
#                                                                    Django Suit
try:
    from suit.admin import SortableModelAdmin, SortableTabularInline
    from suit.widgets import AutosizedTextarea
    has_suit = True
except ImportError:
    has_suit = False
# ______________________________________________________________________________
#                                                                 Django Select2
try:
    from django_select2 import AutoSelect2MultipleField, Select2MultipleWidget
    has_select2 = True
except ImportError:
    has_select2 = False


# ______________________________________________________________________________
#                                                         InlineAdmin: StockLink
class StockLinkInlineAdmin(TabularInline):
    model = StockLink
    fields = ('stock_portal', 'link')
    extra = 0

# ______________________________________________________________________________
#                                                               Admin: StockLink
class StockLinkAdmin(ModelAdmin):
    inlines = []


# ______________________________________________________________________________
#                                                             Admin: StockPortal
class StockPortalAdmin(ModelAdmin):
    list_display = ('get_favicon', 'name',)
    readonly_fields = ('get_favicon',)
    list_display_links = ('get_favicon', 'name',)
    inlines = []


# ______________________________________________________________________________
#                                                            Extension ItemAdmin
class OnStockFilter(admin.SimpleListFilter):
    """
    Filter by stock portals.
    """
    title = _('stock')
    parameter_name = 'stock'

    def lookups(self, request, model_admin):
        portals = list()
        portals.append(('on_stock', _('Any stock portal')))
        portals.append(('no_stock', _('Not on stock')))
        portals.append(('sep', '---'))
        for portal in StockPortal.objects.all().order_by('name'):
            portals.append((portal.name, portal.name,))

        return portals

    def queryset(self, request, queryset):
        if self.value() == 'sep':
            return queryset

        if self.value() == 'on_stock':
            return queryset.exclude(
                filer_file__file_stocklinks__stock_portal=None)

        if self.value() == 'no_stock':
            return queryset.filter(
                filer_file__file_stocklinks__stock_portal=None)

        if self.value():
            portal = StockPortal.objects.get(name=self.value())
            return queryset.filter(
                filer_file__file_stocklinks__stock_portal__in=[portal.pk])


# ______________________________________________________________________________
#                                              Extension for Filersets ItemAdmin
ItemAdmin = admin.site._registry[Item].__class__


class ExtendedItemAdmin(ItemAdmin):
    """
    Extends the default filersets ItemAdmin to show a column that lists the
    stock portals where that particular file could be found.
    """
    def __init__(self, *args, **kwargs):
        super(ItemAdmin, self).__init__(*args, **kwargs)

    def get_list_display(self, request):
        default_list_display = super(ItemAdmin, self).get_list_display(request)
        return list(default_list_display) + [self.on_stock]

    def get_list_filter(self, request):
        default_list_filter = super(ItemAdmin, self).get_list_filter(request)
        return default_list_filter + [OnStockFilter]

    def on_stock(self, obj):
        """
        List all stock platforms that this item is listed on.
        """
        stock_portals = [sl.stock_portal.name for sl
                         in obj.filer_file.file_stocklinks.all()]
        return ', '.join(stock_portals)

    on_stock.allow_tags = True

ItemAdmin = ExtendedItemAdmin

admin.site.unregister(Item)
admin.site.register(Item, ItemAdmin)


# ______________________________________________________________________________
#                                                 Extension for Filer ImageAdmin
ImageAdmin = admin.site._registry[Image].__class__


class ExtendedImageAdmin(ImageAdmin):
    """
    Extends the filer image change page with an inline for stock links.
    """
    def __init__(self, *args, **kwargs):
        super(ImageAdmin, self).__init__(*args, **kwargs)
        self.inlines = self.inlines + [StockLinkInlineAdmin]

ImageAdmin = ExtendedImageAdmin

admin.site.unregister(Image)
admin.site.register(Image, ImageAdmin)


# ______________________________________________________________________________
#                                                                   Registration
admin.site.register(StockPortal, StockPortalAdmin)
admin.site.register(StockLink, StockLinkAdmin)

