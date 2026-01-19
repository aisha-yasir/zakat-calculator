from django.contrib import admin
from .models import ZakatCalculation

@admin.register(ZakatCalculation)
class ZakatAdmin(admin.ModelAdmin):
    list_display = ('user', 'date', 'zakat_amount', 'cash', 'inventory')
    list_filter = ('date', 'user')
    search_fields = ('user__username',)