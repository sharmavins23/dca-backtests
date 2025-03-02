from strategies.AbstractStrategy import AbstractStrategy
from utils import MarketDatapoint


class DCA(AbstractStrategy):
    def __init__(self):
        super().__init__()

    def applyOrderStrategy(self, income: float, dp: MarketDatapoint):
        # Calculate the number of shares to buy
        stockShareCount = income / dp.marketClose

        # Since we aren't adding to our bank balance, we can just add shares
        self.stockShareCount += stockShareCount
