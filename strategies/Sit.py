from strategies.AbstractStrategy import AbstractStrategy
from utils import MarketDatapoint


class Sit(AbstractStrategy):
    def __init__(self):
        super().__init__()

    def applyOrderStrategy(self, income: float, dp: MarketDatapoint):
        self.bankBalance += income
