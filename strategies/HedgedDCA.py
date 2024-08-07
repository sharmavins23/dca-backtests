from strategies.AbstractStrategy import AbstractStrategy
from utils import MarketDatapoint


class HedgedDCA(AbstractStrategy):
    def __init__(self):
        super().__init__()

    def applyOrderStrategy(self, income: float, dp: MarketDatapoint):
        # Instead of YOLO-ing into the market, we'll hedge our bets
        self.bankBalance += income * 0.3

        # Now we can just do DCA with the remainder
        stockShareCount = (income * 0.7) / dp.marketClose
        self.stockShareCount += stockShareCount
