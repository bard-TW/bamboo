from django.contrib import admin

from trade.models import BasicCompanyInformation, TradeDetails, TradeSummary

# Register your models here.

@admin.register(BasicCompanyInformation)
class BasicCompanyInformationAdmin(admin.ModelAdmin):
    list_display = ('stk_no', 'stk_na', 'establishment_date', 'listing_Date', 'stk_ps', 'stk_cs')
    search_fields = ['stk_no', 'stk_na']  # 搜尋條件


@admin.register(TradeDetails)
class TradeDetailsAdmin(admin.ModelAdmin):
    list_display = ('order_no', 'buy_sell', 't_date', 'stk_no_id', 'price', 'qty', 'qty_price', 'fee', 'tax', 'note', 'funds_invested', 'funds_remaining', 'shares', 'price_avg', 'hold_qty_price')


@admin.register(TradeSummary)
class TradeSummaryAdmin(admin.ModelAdmin):
    list_display = ('stk_no_id', 'last_date', 'funds_invested', 'funds_remaining', 'shares', 'price', 'price_avg', 'hold_qty_price', 'now_qty_price')
