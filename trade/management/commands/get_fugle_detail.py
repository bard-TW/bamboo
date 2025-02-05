import logging

from django.core.management.base import BaseCommand
from fugle_marketdata import RestClient, WebSocketClient
from configparser import ConfigParser
from fugle_trade.sdk import SDK
from fugle_trade.order import OrderObject
from fugle_trade.constant import (APCode, Trade, PriceFlag, BSFlag, Action)

from trade.models import TradeDetails, BasicCompanyInformation, TradeSummary
from trade.enum import BuySellEnum
import datetime
logger = logging.getLogger(__name__)

class Command(BaseCommand):
    '''使用富果API取得交易明細'''
    help = '測試'

    def add_arguments(self, parser):
        parser.add_argument(
                '--start_date',
                dest='type',
                default='2024-11-01',
                type=int,
                help='''輸入查詢起始日期 ex: 2024-11-01'''
            )
        parser.add_argument(
                '--end_date',
                dest='type',
                default='2024-12-08',
                type=int,
                help='''輸入查詢結束日期 ex: 2024-12-08'''
            )
    def handle(self, *args, **options):
        logger.info('')
        # 讀取設定檔
        config = ConfigParser()
        config.read('./.information/config.ini')
        # 登入
        sdk = SDK(config)
        sdk.login()

        # 取得交易明細 >> 並計算總額
        transactions_by_date = sdk.get_transactions_by_date("2024-11-01", "2024-12-08")

        for x in transactions_by_date:
            for y in x['mat_dats']:
                print(y)
                stk_no_qs = BasicCompanyInformation.objects.filter(stk_no=y['stk_no'])
                if stk_no_qs.exists():
                    stk_no = stk_no_qs[0]
                else:
                    stk_no, _ = BasicCompanyInformation.objects.get_or_create(stk_no=y['stk_no'], stk_na=y['stk_na'])

                qs = TradeDetails.objects.filter(order_no=y['order_no'], stk_no_id=stk_no, qty=int(y['qty']))
                if qs.exists() == False:
                    self.record(stk_no, y)

    def record(self, stk_no, mat_data):
        t_date = datetime.datetime.strptime(mat_data['t_date'], "%Y%m%d").date()
        price = float(mat_data['price'])
        qty = int(mat_data['qty'])
        fee = int(mat_data['fee'])
        tax = int(mat_data['tax'])
        qty_price = int(price*qty)
        buy_sell = BuySellEnum(mat_data['buy_sell'])

        funds_remaining = 0
        funds_invested = 0
        shares = 0
        price_avg = 0
        hold_qty_price = 0

        last_qs = TradeDetails.objects.filter(stk_no_id=stk_no).order_by('id')
        if last_qs.exists():
            last_q = last_qs.last()
            funds_invested = last_q.funds_invested
            funds_remaining = last_q.funds_remaining
            shares = last_q.shares
            price_avg = last_q.price_avg
            hold_qty_price = last_q.hold_qty_price

        if buy_sell == BuySellEnum.SELL:
            # 賣出
            funds_remaining += (qty_price-fee-tax)
            shares -= qty
            hold_qty_price -= qty*price_avg
        else:
            # 買入 #* buy_sell是其他的話再觀察如何寫
            funds_remaining -= (qty_price-fee-tax) # 總花費
            shares += qty
            hold_qty_price += qty_price
            price_avg = round(hold_qty_price/shares, 2)


        create_data = {
            'order_no': mat_data['order_no'],
            'buy_sell': mat_data['buy_sell'],
            't_date': t_date,
            'stk_no_id': stk_no,
            'price': price,
            'qty': qty,
            'qty_price': qty_price,
            'fee': fee,
            'tax': tax,
            'note': mat_data['user_def'],

            'funds_invested': funds_invested,
            'funds_remaining': funds_remaining,
            'shares': shares,
            'price_avg': price_avg,
            'hold_qty_price': hold_qty_price
        }
        TradeDetails.objects.create(**create_data)

        summary_q, is_new = TradeSummary.objects.get_or_create(stk_no_id=stk_no)
        summary_q.last_date = t_date
        summary_q.funds_invested = funds_invested
        summary_q.funds_remaining = funds_remaining
        summary_q.shares = shares
        summary_q.price_avg = price_avg
        summary_q.hold_qty_price = hold_qty_price
        if is_new:
            summary_q.price = price
            summary_q.now_qty_price = price*shares
        summary_q.save()
