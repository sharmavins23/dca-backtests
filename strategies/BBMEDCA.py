from strategies.AbstractStrategy import AbstractStrategy
from utils import MarketDatapoint


class BBMEDCA(AbstractStrategy):
    def __init__(self):
        super().__init__()
        self.lastClose = 0.0
        self.Y = 300.0  # Fixed increment amount
        self.X = 3000.0  # Current buy amount (initial value)

    def applyOrderStrategy(self, income: float, dp: MarketDatapoint):
        # If the stock goes down, increase DCA amount by Y
        if self.lastClose > dp.marketClose:
            stockShareCount = min(
                self.X + self.Y, income + self.bankBalance) / dp.marketClose
            self.stockShareCount += stockShareCount

            # If there's excess income, throw it in the bank
            if self.X + self.Y < income:
                self.bankBalance += income - self.X - self.Y
            # If we exceeded income, remove the excess from the bank
            if self.X + self.Y > income:
                self.bankBalance -= self.X + self.Y - income
        # If the stock goes up, decrease DCA amount by Y
        elif self.lastClose < dp.marketClose:
            stockShareCount = max(self.X - self.Y, 0) / dp.marketClose
            self.stockShareCount += stockShareCount

            # If there's excess income, throw it in the bank
            if self.X - self.Y < income:
                self.bankBalance += income - self.X + self.Y
            # If we exceeded income, remove the excess from the bank
            if self.X - self.Y > income:
                self.bankBalance -= self.X - self.Y - income
        else:
            # If the stock stays the same, keep DCA amount the same
            stockShareCount = self.X / dp.marketClose
            self.stockShareCount += stockShareCount

            # If there's excess income, throw it in the bank
            if self.X < income:
                self.bankBalance += income - self.X
            # If we exceeded income, remove the excess from the bank
            if self.X > income:
                self.bankBalance -= self.X - income

        # Finally, update the market close
        self.lastClose = dp.marketClose
