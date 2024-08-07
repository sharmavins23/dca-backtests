from strategies.AbstractStrategy import AbstractStrategy
from utils import MarketDatapoint

# Dollar Cost Averaging (DCA) is a strategy that involves buying a fixed dollar
# amount of a particular investment on a regular schedule, regardless of the
# investment's price. This strategy is used to avoid making poor investment
# decisions based on market conditions, and is instead focused on long-term
# growth.


class DCA(AbstractStrategy):
    def __init__(self):
        super().__init__()

    def applyOrderStrategy(self, income: float, dp: MarketDatapoint):
        # Calculate the number of shares to buy
        stockShareCount = income / dp.marketClose

        # Since we aren't adding to our bank balance, we can just add shares
        self.stockShareCount += stockShareCount
