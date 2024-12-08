from enum import Enum


class BuySellEnum(Enum):
    BUY = 'B'
    SELL = 'S'
    OTHER = ''

    @classmethod
    def choices(cls):
        return [(key.value, key.name.capitalize()) for key in cls]
