from strategies.AbstractStrategy import AbstractStrategy
from utils import MarketDatapoint


class StocksGoUp(AbstractStrategy):
    def __init__(self):
        super().__init__()
        self.lastClose = 0.0

    def applyOrderStrategy(self, income: float, dp: MarketDatapoint):
        # If the stock went down, buybuybuy
        if self.lastClose > dp.marketClose:
            stockShareCount = (income + self.bankBalance) / dp.marketClose
            self.stockShareCount += stockShareCount
            self.bankBalance = 0.0
        # If the stock went up, don't buy and just sit on it
        elif self.lastClose < dp.marketClose:
            self.bankBalance += income
        else:
            # If the stock stayed the same, just buy
            stockShareCount = income / dp.marketClose
            self.stockShareCount += stockShareCount

        # Finally, update the market close
        self.lastClose = dp.marketClose
