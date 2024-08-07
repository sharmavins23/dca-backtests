from strategies.AbstractStrategy import AbstractStrategy
from utils import MarketDatapoint


class AddBBMEDCA(AbstractStrategy):
    def __init__(self):
        super().__init__()
        self.lastClose = 0.0
        self.Y = 1500.0  # Fixed increment amount
        self.X = 3000.0  # Current buy amount (initial value)

    def applyOrderStrategy(self, income: float, dp: MarketDatapoint):
        # If the stock goes down, increase DCA amount by Y
        if self.lastClose > dp.marketClose:
            self.X += self.Y
            self.X = min(self.X, income + self.bankBalance)
            stockShareCount = self.X / dp.marketClose
            self.stockShareCount += stockShareCount

            # If we exceeded income, remove the excess from the bank
            if self.X > income:
                self.bankBalance -= self.X - income
            # If we have excess income, throw it in the bank
            if self.X < income:
                self.bankBalance += income - self.X
        # If the stock goes up, decrease DCA amount by Y
        elif self.lastClose < dp.marketClose:
            self.X = max(self.X - self.Y, 0)
            stockShareCount = self.X / dp.marketClose
            self.stockShareCount += stockShareCount

            # If we exceeded income, remove the excess from the bank
            if self.X > income:
                self.bankBalance -= self.X - income
            # If we have excess income, throw it in the bank
            if self.X < income:
                self.bankBalance += income - self.X
        else:
            # If the stock stays the same, keep DCA amount the same
            stockShareCount = self.X / dp.marketClose
            self.stockShareCount += stockShareCount

            # If we exceeded income, remove the excess from the bank
            if self.X > income:
                self.bankBalance -= self.X - income
            # If we have excess income, throw it in the bank
            if self.X < income:
                self.bankBalance += income - self.X

        # Finally, update the market close
        self.lastClose = dp.marketClose
