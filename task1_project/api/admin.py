from django.contrib import admin
from .models import *

from django.utils.html import format_html
from django.urls import reverse


# Register your models here.
class ChainInline(admin.StackedInline):
    model = Chain
class ContactsInline(admin.StackedInline):
    model = Contacts
class ChainAdmin(admin.ModelAdmin):
    
    list_display = ('id', 'name', 'type', 'view_supplier_link', 'debt', )
    
    list_display_links = ('name', 'view_supplier_link')

    list_filter = ('contacts__city', )

    def view_supplier_link(self, obj):
        url = reverse(f"admin:api_chain_change", args=[obj.supplier_id, ])
        return format_html('<a href="{}"> {} </a>', url, obj.supplier_id)

    view_supplier_link.short_description = "Supplier"

    inlines = [
        ChainInline,
        ContactsInline,
    ]

admin.site.register(Contacts)
admin.site.register(Chain, ChainAdmin)