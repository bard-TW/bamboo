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
    '''啟動此程式自動下單'''
    help = '啟動此程式自動下單'

    def handle(self, *args, **options):
        logger.info('')
        # 讀取設定檔
        config = ConfigParser()
        config.read('./.information/config.ini')
        # 登入
        sdk = SDK(config)
        sdk.login()

    '''
    看過去的60天與30天的價格，如果60天的價格比30天的價格高，則買進

    交易時如何知道是買進還是賣出？
    資料庫的明細

    買入條件
    條件1 60天與30天
    條件2 低於上次買入價格或7天內未交易
    '''
