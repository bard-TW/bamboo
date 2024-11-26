from django.contrib import admin

from trade.models import BasicCompanyInformation, TradeDetails, TradeSummary

# Register your models here.

@admin.register(BasicCompanyInformation)
class CityCodeTableAdmin(admin.ModelAdmin):
    list_display = ('stk_no', 'stk_na', 'establishment_date', 'listing_Date', 'stk_ps', 'stk_cs')
    search_fields = ['stk_no', 'stk_na']  # 搜尋條件


@admin.register(TradeSummary)
class CityCodeTableAdmin(admin.ModelAdmin):
    list_display = ('stk_no_id', 'price_avg', 'qty', 'initial_funds', 'remaining_funds')


@admin.register(TradeDetails)
class CityCodeTableAdmin(admin.ModelAdmin):
    list_display = ('t_date', 'stk_no_id', 'price', 'qty', 'fee', 'tax')
