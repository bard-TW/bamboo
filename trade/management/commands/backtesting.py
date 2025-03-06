import json
import logging

import pandas as pd
import requests
from django.conf import settings
from django.core.management.base import BaseCommand
from fugle_marketdata import RestClient
from trade.models import BasicCompanyInformation

class Command(BaseCommand):
    '''回測'''
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
        # API_KEY = settings.FUGLE_API_KEY
        # symbol = '0050' # 股票代號

        # client = RestClient(api_key=API_KEY)
        # stock = client.stock

        # candles_list = []
        # for y in range(2021, 2026):
        #     start_date = str(y) + "-01-01"
        #     end_date = str(y) + "-12-31"
        #     history_options = {
        #         "symbol": symbol,
        #         "from": start_date,
        #         "to": end_date,
        #         "timeframe": "D",
        #         "fields": "open,high,low,close,volume,change,turnover"
        #     }
        #     historical_data = stock.historical.candles(**history_options)
        #     candles_list = candles_list + historical_data['data']

        # df = pd.DataFrame(candles_list).sort_values('date')
        # df = df.reset_index().drop('index', axis=1)

        # df.to_csv('0050.csv', index=False)
        df = pd.read_csv('0050.csv')


        df['12MA'] = df['open'].rolling(window=12).mean()
        df['26MA'] = df['open'].rolling(window=26).mean()
        df['DIF'] = df['12MA'] - df['26MA']
        df['signal'] = df['DIF'].rolling(window=9).mean()
        df = df[['date', 'open', 'change', 'DIF', 'signal']]
        df['RSI'] = self.calculate_rsi(df)
        print(df)

    def calculate_rsi(self, df, period=14):
        delta = df['change']
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        return rsi
