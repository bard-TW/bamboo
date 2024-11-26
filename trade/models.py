from django.db import models
from django.utils import timezone
# Create your models here.



class BasicCompanyInformation(models.Model):
    stk_no = models.CharField(max_length=10, verbose_name='股票代號')
    stk_na = models.CharField(max_length=50, verbose_name='股票名稱')
    stk_ab = models.CharField(max_length=50, verbose_name='簡稱')
    establishment_date = models.CharField(max_length=8, verbose_name='成立日期')
    listing_Date = models.CharField(max_length=8, verbose_name='上市日期')
    stk_ps = models.IntegerField(verbose_name='特別股數')
    stk_cs = models.IntegerField(verbose_name='普通股數')
    class Meta:
        db_table = 'basic_company_information'
        verbose_name = '公司基本資訊'
        verbose_name_plural = '公司基本資訊'

        constraints = [
            models.UniqueConstraint(fields=['stk_no'], name=f'{db_table} unique key')
        ]

        indexes = [
            models.Index(fields=['stk_no']),
        ]



# 交易日期 股票代號 成交價 股數 手續費 交易稅
class TradeDetails(models.Model):
    t_date = models.DateField(default=timezone.now, verbose_name='成交日期')
    stk_no_id = models.ForeignKey(BasicCompanyInformation, on_delete=models.CASCADE, help_text='股票代號')
    price = models.FloatField(verbose_name='成交價格')
    qty = models.IntegerField(verbose_name='成交數量')
    fee = models.IntegerField(verbose_name='手續費')
    tax = models.IntegerField(verbose_name='交易稅')

    class Meta:
        db_table = 'trade_details'
        verbose_name = '交易明細'
        verbose_name_plural = '交易明細'


# 股票代號 成交均價 庫存股 本金 剩餘本金
class TradeSummary(models.Model):
    stk_no_id = models.ForeignKey(BasicCompanyInformation, on_delete=models.CASCADE, help_text='股票代號')
    price_avg = models.FloatField(verbose_name='成交均價')
    qty = models.IntegerField(verbose_name='庫存股數')
    initial_funds = models.FloatField(verbose_name='初始資金')
    remaining_funds = models.IntegerField(verbose_name='剩餘資金')

    class Meta:
        db_table = 'trade_summary'
        verbose_name = '庫存總計'
        verbose_name_plural = '庫存總計'
