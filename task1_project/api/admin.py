from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
import multiprocessing
import asyncio
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

    def async_clear_20_debt():
        pass
        
        def square(n):
            return (n*n)
        
        if __name__ == "__main__":
            # input list
            mylist = [1,2,3,4,5]
        
            # creating a pool object
            p = multiprocessing.Pool()
        
            # map list to target function
            result = p.map(square, mylist)
        
            print(result)

    def view_supplier_link(self, obj):
        url = reverse("admin:api_chain_change", args=[obj.supplier_id, ])
        return format_html('<a href="{}"> {} </a>', url, obj.supplier_id)
    view_supplier_link.short_description = "Supplier"

    def clear_debt(self, _, queryset):
        devision = 20
        query_len = queryset.count()
        if query_len > devision:
            pool_len_number = query_len // devision
            pool_len_number = pool_len_number if query_len % devision == 0 else pool_len_number+1
            pool = multiprocessing.Pool(processes=pool_len_number)
            # array = multiprocessing.Array(type(Chain), query_len)
            # for part in range(pool_len_number):
            for part in range(0, query_len, devision):
                pass
                # multiprocessing.Array()
                

        else:
            for chain in queryset:
                if chain.debt > 0:
                    chain.debt = 0
                    chain.save()
        # self.message_user(req, "Debt is cleaned")

    clear_debt.description = 'Clear debt'
    inlines = [
        ContactInline,
        ProductInline,
    ]


admin.site.register(Contact)
admin.site.register(Product)
admin.site.register(Chain, ChainAdmin)
