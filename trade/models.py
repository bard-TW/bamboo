from django.db import models
from django.utils import timezone
from trade.enum import BuySellEnum
# Create your models here.

class BasicCompanyInformation(models.Model):
    stk_no = models.CharField(max_length=10, verbose_name='股票代號')
    stk_na = models.CharField(max_length=50, verbose_name='股票名稱')
    stk_ab = models.CharField(max_length=50, null=True, blank=True, verbose_name='簡稱')
    establishment_date = models.CharField(max_length=8, null=True, blank=True, verbose_name='成立日期')
    listing_Date = models.CharField(max_length=8, null=True, blank=True, verbose_name='上市日期')
    stk_ps = models.IntegerField(default=0, verbose_name='特別股數')
    stk_cs = models.IntegerField(default=0, verbose_name='普通股數')
    class Meta:
        db_table = 'basic_company_information'
        verbose_name = '公司基本資訊'
        verbose_name_plural = '公司基本資訊'

        constraints = [
            models.UniqueConstraint(fields=['stk_no'], name=f'{db_table} unique key')
        ]

        indexes = [
            models.Index(fields=['stk_ab']),
        ]

    def __str__(self):
        return "{} {}".format(self.stk_no, self.stk_na)

# 交易日期 股票代號 成交價 股數 手續費 交易稅
class TradeDetails(models.Model):
    order_no = models.CharField(max_length=20, verbose_name='委託單號')
    buy_sell = models.CharField(max_length=1, choices=BuySellEnum.choices(), verbose_name='買賣')
    t_date = models.DateField(default=timezone.now, verbose_name='成交日期')
    # t_time = models.TimeField(default=timezone.now, verbose_name='成交時間')
    stk_no_id = models.ForeignKey(BasicCompanyInformation, on_delete=models.CASCADE, verbose_name='股票代號')
    price = models.FloatField(default=0, verbose_name='成交價格')
    qty = models.IntegerField(default=0, verbose_name='成交數量')
    qty_price = models.IntegerField(default=0, verbose_name='價值金額', help_text='股數x金額')
    fee = models.IntegerField(default=0, verbose_name='手續費')
    tax = models.IntegerField(default=0, verbose_name='交易稅')
    note = models.CharField(default='', max_length=30, verbose_name='備註')

    funds_invested = models.IntegerField(default=0, verbose_name='投入資金', help_text='只有設定時會變動')
    funds_remaining  = models.IntegerField(default=0, verbose_name='剩餘資金', help_text='買賣後剩下資金，投入資金變動時也會增減')
    shares = models.IntegerField(default=0, verbose_name='持有股數')
    price_avg = models.FloatField(default=0, verbose_name='成交均價')
    hold_qty_price = models.IntegerField(default=0, verbose_name='購買成本')

    class Meta:
        db_table = 'trade_details'
        verbose_name = '交易明細'
        verbose_name_plural = '交易明細'

        constraints = [
            models.UniqueConstraint(fields=['order_no', 'stk_no_id', 'qty'], name=f'{db_table} unique key')
        ]

        indexes = [
            models.Index(fields=['order_no', 'stk_no_id', 'qty']),
        ]


# 股票代號 成交均價 庫存股 本金 剩餘本金
class TradeSummary(models.Model):
    stk_no_id = models.ForeignKey(BasicCompanyInformation, on_delete=models.CASCADE, help_text='股票代號')
    last_date = models.DateField(default=timezone.now, verbose_name='最後成交日期')
    funds_invested = models.IntegerField(default=0, verbose_name='投入資金')
    funds_remaining  = models.IntegerField(default=0, verbose_name='剩餘資金', help_text='買賣後剩下資金')
    shares = models.IntegerField(default=0, verbose_name='持有股數')
    price = models.FloatField(default=0, verbose_name='價格')
    price_avg = models.FloatField(default=0, verbose_name='成交均價')
    hold_qty_price = models.IntegerField(default=0, verbose_name='購買成本')
    now_qty_price = models.IntegerField(default=0, verbose_name='最新價值', help_text='股數x最新股價')

    class Meta:
        db_table = 'trade_summary'
        verbose_name = '庫存總計'
        verbose_name_plural = '庫存總計'
