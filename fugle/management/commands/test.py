import logging

from django.core.management.base import BaseCommand
from fugle_marketdata import RestClient, WebSocketClient

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    '''測試'''
    help = '測試'

    def add_arguments(self, parser):
        parser.add_argument(
                '--type',
                dest='type',
                default=1,
                type=int,
                help='''無作用'''
            )

    def handle(self, *args, **options):
        logger.info('asd')
        client = RestClient(api_key='')
        stock = client.stock  # Stock REST API client
        print(stock.intraday.quote(symbol="2330"))
