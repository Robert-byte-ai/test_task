from django.contrib import admin

from .models import Item, Tax, Discount, Order


class ItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'currency')


admin.site.register(Item, ItemAdmin)
admin.site.register(Tax)
admin.site.register(Discount)
admin.site.register(Order)
