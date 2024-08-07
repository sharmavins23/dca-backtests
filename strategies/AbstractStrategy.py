from abc import ABC, abstractmethod
from utils import MarketDatapoint


# The abstract base class (ABC) for all trading strategies.
class AbstractStrategy(ABC):
    @abstractmethod
    def __init__(self):
        self.bankBalance = 0.0
        self.stockShareCount = 0.0
        self.netWorth = 0.0
        self.netWorthHistory = []

    def preApplyOrderStrategy(self, yr: float):
        self.bankBalance *= (1 + yr)

    @abstractmethod
    def applyOrderStrategy(self, income: float, dp: MarketDatapoint):
        pass

    def postApplyOrderStrategy(self, dp: MarketDatapoint):
        self.netWorth = self.bankBalance + \
            (self.stockShareCount * dp.marketClose)
        self.netWorthHistory.append(self.netWorth)
