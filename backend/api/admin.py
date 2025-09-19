from django.contrib import admin
from .models import Company, IPO

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'sector', 'website', 'created_at')
    search_fields = ('name', 'sector')

@admin.register(IPO)
class IPOAdmin(admin.ModelAdmin):
    list_display = ('company', 'status', 'open_date', 'close_date', 'ipo_price', 'listing_price')
    search_fields = ('company__name', 'price_band', 'status')
    list_filter = ('status', 'open_date')
