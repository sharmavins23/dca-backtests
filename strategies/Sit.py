from strategies.AbstractStrategy import AbstractStrategy
from utils import MarketDatapoint

# The Sit strategy does nothing but sit on its current income in money market
# funds. This is a simple strategy that does not involve any significant trading
# or portfolio management; However, the returns are capped to the federal yield
# rate alone.


class Sit(AbstractStrategy):
    def __init__(self):
        super().__init__()

    def applyOrderStrategy(self, income: float, dp: MarketDatapoint):
        self.bankBalance += income
