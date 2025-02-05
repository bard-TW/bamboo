from django.contrib import admin, messages

from trade.enum import BuySellEnum
from trade.models import BasicCompanyInformation, TradeDetails, TradeSummary

# Register your models here.

@admin.register(BasicCompanyInformation)
class BasicCompanyInformationAdmin(admin.ModelAdmin):
    list_display = ('stk_no', 'stk_na', 'establishment_date', 'listing_Date', 'stk_ps', 'stk_cs')
    search_fields = ['stk_no', 'stk_na']  # 搜尋條件


@admin.register(TradeDetails)
class TradeDetailsAdmin(admin.ModelAdmin):
    list_display = ('order_no', 'buy_sell', 't_date', 'stk_no_id', 'price', 'qty', 'qty_price', 'fee', 'tax', 'note', 'funds_invested', 'funds_remaining', 'shares', 'price_avg', 'hold_qty_price')
    search_fields = ['stk_no_id__stk_no']  # 搜尋條件
    actions = ['update_result']

    @admin.action(description='更新此筆後相同股票的持有結果')
    def update_result(self, request, queryset):
        # 成交日期，當天可能會有多筆 前1天也有很多筆 如何判斷最後一筆
        details_qs = TradeDetails.objects.filter(stk_no_id=queryset[0].stk_no_id, t_date__gte=queryset[0].t_date).order_by('t_date')
        if len(details_qs) <= 1:
            self.message_user(request, f"此為最新一筆交易，若要更新此筆持有結果，請選擇上一筆資料。", messages.ERROR)
            return
        funds_remaining = details_qs[0].funds_remaining
        shares = details_qs[0].shares
        price_avg = details_qs[0].price_avg
        hold_qty_price = details_qs[0].hold_qty_price

        for detail in details_qs[1:]:
            if BuySellEnum(detail.buy_sell) == BuySellEnum.SELL:
                funds_remaining += (detail.qty_price-detail.fee-detail.tax)
                shares -= detail.qty
                hold_qty_price -= detail.qty*price_avg

            else:
                funds_remaining -= (detail.qty_price-detail.fee-detail.tax) # 總花費
                shares += detail.qty
                hold_qty_price += detail.qty_price
                price_avg = round(hold_qty_price/shares, 2)
                pass

            detail.funds_remaining = funds_remaining
            detail.shares = shares
            detail.price_avg = price_avg
            detail.hold_qty_price = hold_qty_price
            detail.save()

        last_detail = details_qs.last()
        summary_q, _ = TradeSummary.objects.get_or_create(stk_no_id=details_qs[0].stk_no_id)
        summary_q.last_date = last_detail.t_date
        summary_q.funds_invested = last_detail.funds_invested
        summary_q.funds_remaining = funds_remaining
        summary_q.shares = shares
        summary_q.price_avg = price_avg
        summary_q.hold_qty_price = hold_qty_price
        summary_q.save()
        self.message_user(request, f"更新成功", messages.SUCCESS)


@admin.register(TradeSummary)
class TradeSummaryAdmin(admin.ModelAdmin):
    list_display = ('stk_no_id', 'last_date', 'funds_invested', 'funds_remaining', 'shares', 'price', 'price_avg', 'hold_qty_price', 'now_qty_price')
    search_fields = ['stk_no_id__stk_no']  # 搜尋條件
