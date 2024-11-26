import logging

from django.core.management.base import BaseCommand
from fugle_marketdata import RestClient, WebSocketClient
from configparser import ConfigParser
from fugle_trade.sdk import SDK
from fugle_trade.order import OrderObject
from fugle_trade.constant import (APCode, Trade, PriceFlag, BSFlag, Action)
import requests
import json
from trade.models import BasicCompanyInformation
logger = logging.getLogger(__name__)

class Command(BaseCommand):
    '''取得股票代碼'''
    help = ''

    def add_arguments(self, parser):
        parser.add_argument(
                '--type',
                dest='type',
                default=1,
                type=int,
                help='''無作用'''
            )

    def handle(self, *args, **options):
        response = requests.get('https://openapi.twse.com.tw/v1/opendata/t187ap03_L')
        json_data = json.loads(response.text)

        bulk_create_list = []
        bulk_update_list = []

        for data in json_data:
            print(data['公司代號'], data['公司名稱'], data['公司簡稱'], data['成立日期'], data['上市日期'], data['實收資本額'], data['特別股'], data['已發行普通股數或TDR原股發行股數'])

            qs = BasicCompanyInformation.objects.filter(stk_no=data['公司代號'])
            if qs.exists() == False:
                bulk_create_list.append(
                    BasicCompanyInformation(stk_no=data['公司代號'], stk_na=data['公司名稱'], stk_ab=data['公司簡稱'], establishment_date=data['成立日期'],
                                            listing_Date=data['上市日期'], stk_ps=data['特別股'], stk_cs=data['已發行普通股數或TDR原股發行股數']))
            else:
                Company_information = qs[0]
                Company_information.stk_ps=data['特別股']
                Company_information.stk_cs=data['已發行普通股數或TDR原股發行股數']
                bulk_update_list.append(Company_information)

        if bulk_create_list:
            BasicCompanyInformation.objects.bulk_create(bulk_create_list, batch_size=1000)

        if bulk_update_list:
            BasicCompanyInformation.objects.bulk_update(bulk_update_list, ['stk_ps', 'stk_cs'], batch_size=1000)
