from django.contrib import admin
from .models import (
    Chain,
    Contacts,
    Product
)

from django.utils.html import format_html
from django.urls import reverse


# Register your models here.
class ChainInline(admin.TabularInline):
    model = Chain
class ContactsInline(admin.TabularInline):
    model = Contacts
class ProductInline(admin.TabularInline):
    model = Product
class ChainAdmin(admin.ModelAdmin):
    
    list_display = ('id', 'name', 'type', 'view_supplier_link', 'debt', )
    
    list_display_links = ('name', 'view_supplier_link')

    list_filter = ('contacts__city', )

    actions = ('clear_debt', )

    def view_supplier_link(self, obj):
        url = reverse(f"admin:api_chain_change", args=[obj.supplier_id, ])
        return format_html('<a href="{}"> {} </a>', url, obj.supplier_id)
    view_supplier_link.short_description = "Supplier"

    def clear_debt(self, req, queryset):
        for chain in queryset:
            if chain.debt < 0:
                chain.debt = 0
                chain.save()
        self.message_user(req, "Debt is cleaned")
    clear_debt.description='Clear debt'

    inlines = [
        ChainInline,
        ContactsInline,
        ProductInline,
    ]

admin.site.register(Contacts)
admin.site.register(Product)
admin.site.register(Chain, ChainAdmin)