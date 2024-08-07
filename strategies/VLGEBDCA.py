from strategies.AbstractStrategy import AbstractStrategy
from utils import MarketDatapoint


class VLGEBDCA(AbstractStrategy):
    def __init__(self):
        super().__init__()
        self.lastClose = 0.0
        self.currentBuyAmount = 1000.0
        self.buyMinimum = 500.0
        self.buyIncrement = 1000.0
        self.buyReduction = 1.1

    def applyOrderStrategy(self, income: float, dp: MarketDatapoint):
        if self.lastClose > dp.marketClose:
            # The stock went down - Buy more, linear growth
            self.currentBuyAmount += self.buyIncrement
            self.currentBuyAmount = min(
                self.currentBuyAmount, income + self.bankBalance)
            stockShareCount = self.currentBuyAmount / dp.marketClose
            self.stockShareCount += stockShareCount

            # If we exceeded income, remove the excess from the bank
            if self.currentBuyAmount > income:
                self.bankBalance -= self.currentBuyAmount - income

            # Put the remainder in the bank, if there is any
            if self.currentBuyAmount < income:
                self.bankBalance += income - self.currentBuyAmount
        elif self.lastClose < dp.marketClose:
            # The stock went up - Buy less, exponentially backoff
            self.currentBuyAmount = max(
                self.currentBuyAmount / self.buyReduction, self.buyMinimum)
            stockShareCount = self.currentBuyAmount / dp.marketClose
            self.stockShareCount += stockShareCount

            # Put the remainder in the bank, if there is any
            if self.currentBuyAmount < income:
                self.bankBalance += income - self.currentBuyAmount
        else:
            # The stock stayed the same - Buy the same amount
            stockShareCount = self.currentBuyAmount / dp.marketClose
            self.stockShareCount += stockShareCount

            # Put the remainder in the bank, if there is any
            if self.currentBuyAmount < income:
                self.bankBalance += income - self.currentBuyAmount

        self.lastClose = dp.marketClose
