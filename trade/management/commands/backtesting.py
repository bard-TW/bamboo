import json
import logging

import pandas as pd
import requests
from django.conf import settings
from django.core.management.base import BaseCommand
from fugle_marketdata import RestClient

from trade.models import BasicCompanyInformation


class Backtesting:
    def __init__(self, symbol='0000', base_price=22.2, base_funds=200000):
        self.base_funds = base_funds
        self.symbol = symbol
        self.backtesting_df = pd.DataFrame({ # 儲存回測交易資訊
            'datetime': [], # 買賣時間
            'type': [], # 買賣類型 buy, sell
            'fractional_share': [], # 買賣股數
            'stock_price': [], # 股票單價
            'commission': [], # 手續費
            'tax': [], # 交易稅
            'remark': [], # 備註

            'total_cost': [], # 總成本
            'remaining_funds': [], # 剩餘本金
            'hold_stock': [], # 持有股數
            'hold_stock_avg_price': [], # 持有平均單價
            'status': [], # 交易狀態 0: 失敗 1: 成功
            })

        self.backtesting_df.loc[len(self.backtesting_df)] = {
            'datetime': '2021-01-01',
            'type': 'buy',
            'fractional_share': 0,
            'stock_price': 0,
            'commission': 0,
            'tax': 0,
            'remark': '',
            'total_cost': 0,
            'remaining_funds': base_funds,
            'hold_stock': 0,
            'hold_stock_avg_price': base_price,
            'status': 0
        }


    def buy(self, datetime, buy_price, money, remark=''):
        # 上一筆紀錄
        previous_df = self.backtesting_df.iloc[len(self.backtesting_df)-1]

        # 買進
        shares_num = money // buy_price

        # 交易狀態 0: 失敗 1: 成功
        status = 1

        # 本金不足
        if previous_df['remaining_funds'] < shares_num * buy_price:
            shares_num = 0
            status = 0

        # 買進手續費
        pay = int(shares_num * buy_price * 0.001425)

        # 交易稅
        tax = int(shares_num * buy_price * 0.003)

        # 計算總成本
        total_cost = previous_df['total_cost'] + shares_num * buy_price + pay + tax

        # 計算剩餘本金
        remaining_funds = previous_df['remaining_funds'] - shares_num * buy_price - pay - tax

        # 更新持有股數
        hold_stock = previous_df['hold_stock'] + shares_num

        # 更新持有平均單價
        hold_stock_avg_price = (previous_df['hold_stock'] * previous_df['hold_stock_avg_price'] + shares_num * buy_price) / hold_stock

        self.backtesting_df.loc[len(self.backtesting_df)] = {
            'datetime': datetime,
            'type': 'buy',
            'fractional_share': shares_num,
            'stock_price': buy_price,
            'commission': pay,
            'tax': tax,
            'remark': remark,
            'total_cost': total_cost,
            'remaining_funds': remaining_funds,
            'hold_stock': hold_stock,
            'hold_stock_avg_price': hold_stock_avg_price,
            'status': status
        }


    def sell(self, datetime, sell_price, money, remark=''):
        # 上一筆紀錄
        previous_df = self.backtesting_df.iloc[len(self.backtesting_df)-1]

        # 取得賣出股數
        shares_num = money // sell_price

        # 交易狀態 0: 失敗 1: 成功
        status = 1

        # 沒有持有股票
        if previous_df['hold_stock'] < shares_num:
            shares_num = 0
            status = 0

        # 賣出手續費
        pay = int(shares_num * sell_price * 0.001425)

        # 交易稅
        tax = int(shares_num * sell_price * 0.003)

        # 計算總成本
        total_cost = previous_df['total_cost'] + pay + tax - shares_num * sell_price

        # 計算剩餘本金
        remaining_funds = previous_df['remaining_funds'] + shares_num * sell_price - pay - tax

        # 更新持有股數
        hold_stock = previous_df['hold_stock'] - shares_num

        # 更新持有平均單價
        hold_stock_avg_price = (previous_df['hold_stock'] * previous_df['hold_stock_avg_price'] - shares_num * sell_price) / hold_stock

        self.backtesting_df.loc[len(self.backtesting_df)] = {
            'datetime': datetime,
            'type': 'sell',
            'fractional_share': shares_num,
            'stock_price': sell_price,
            'commission': pay,
            'tax': tax,
            'remark': remark,
            'total_cost': total_cost,
            'remaining_funds': remaining_funds,
            'hold_stock': hold_stock,
            'hold_stock_avg_price': hold_stock_avg_price,
            'status': status
        }

    def export_csv(self):
        self.backtesting_df.to_csv(f'{self.symbol} backtesting.csv', index=False, encoding='BIG5')

    def calculate(self):
        # 計算獲利
        last_data = self.backtesting_df.loc[len(self.backtesting_df)-1]

        print('初始本金:', self.base_funds)
        print('股票現值:', last_data['hold_stock'] * last_data['stock_price'])
        print('剩餘本金:', last_data['total_cost'])
        print('純利:', last_data['hold_stock'] * last_data['stock_price'] + last_data['total_cost'] - self.base_funds)


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
        API_KEY = settings.FUGLE_API_KEY
        symbol = '2610' # 股票代號

        # 取得歷史資料 ---------------------
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
        # df.to_csv(f'{symbol}.csv', index=False)


        df = pd.read_csv(f'{symbol}.csv')
        backtesting = Backtesting(symbol=symbol, base_price=22.2, base_funds=200000)
        # 單筆交易金額
        price = 1000

        # 基準值、容許波動區間、最高成本、停利不停損、買賣依固定金額
        # 不同策略切換可以無痛銜接
        # 過去一年穩定波動 策略1: 網格交易策略，壓低持有價格策略

        #? 定期不定額持續買進，低於85%投入增加140%，高於115%投入增加60%，區間投入增加100%，150% 慢慢出清(人工) 停利不停損 有交易等一周

        # df['12MA'] = df['open'].rolling(window=12).mean()
        # df['26MA'] = df['open'].rolling(window=26).mean()
        # df['DIF'] = df['12MA'] - df['26MA']
        # df['signal'] = df['DIF'].rolling(window=9).mean()
        # df = df[['date', 'open', 'change', 'DIF', 'signal']]
        # df['RSI'] = self.calculate_rsi(df)
        # print(df)

        space = 0
        for row in df.itertuples(index=True, name='Person'):
            avg_price = backtesting.backtesting_df.loc[len(backtesting.backtesting_df)-1, 'hold_stock_avg_price']
            if space > 0:
                space -= 1
                continue
            if row.open < avg_price * 0.85:
                backtesting.buy(row.date, row.open, price*1.4, '低於85%投入140%')
                space = 5
            elif row.open > avg_price * 1.15:
                backtesting.buy(row.date, row.open, price*0.6, '高於115%投入60%')
                space = 5
            elif row.open < avg_price * 1.15 and row.open > avg_price * 0.85:
                backtesting.buy(row.date, row.open, price, '區間投入100%')
                space = 5

            elif row.open > avg_price * 1.5:
                answer = input('1賣出 0不賣出: ')
                if answer == '1':
                    backtesting.sell(row.date, row.open, price*1.5, '150% 慢慢出清(人工)')
                space = 5
        backtesting.export_csv()
        backtesting.calculate()


    def calculate_rsi(self, df, period=14):
        delta = df['change']
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        return rsi
