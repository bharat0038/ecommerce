from django.contrib import admin
from .models import Cart, Order ,OrderItem, Payment

admin.site.register(Cart)
#admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Payment)


from django.contrib import admin
from .models import Order

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'total_amount', 'status', 'created_at')
    list_filter = ('status',)
    list_editable = ('status',)






