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
    
    list_display = ('id', 'name', 'type', 'debt', )
    
    list_display_links = ('name', )

    list_filter = ('contacts__city', )


    inlines = [
        ChainInline,
        ContactsInline,
    ]

admin.site.register(Contacts)
admin.site.register(Chain, ChainAdmin)