from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from api.models import (
    Chain,
    Contact,
    Product
)


# Register your models here.
class ContactInline(admin.TabularInline):
    model = Contact


class ProductInline(admin.TabularInline):
    model = Product


class ChainAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'type', 'view_supplier_link', 'debt', )
    list_display_links = ('name', 'view_supplier_link')

    list_filter = ('contact__city', )

    actions = ('clear_debt', )

    def view_supplier_link(self, obj):
        url = reverse("admin:api_chain_change", args=[obj.supplier_id, ])
        return format_html('<a href="{}"> {} </a>', url, obj.supplier_id)
    view_supplier_link.short_description = "Supplier"

    def clear_debt(self, req, queryset):
        for chain in queryset:
            if chain.debt < 0:
                chain.debt = 0
                chain.save()
        self.message_user(req, "Debt is cleaned")

    clear_debt.description = 'Clear debt'
    inlines = [
        ContactInline,
        ProductInline,
    ]


admin.site.register(Contact)
admin.site.register(Product)
admin.site.register(Chain, ChainAdmin)
