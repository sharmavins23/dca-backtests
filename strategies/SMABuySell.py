from strategies.AbstractStrategy import AbstractStrategy
from utils import MarketDatapoint


class SMABuySell(AbstractStrategy):
    def __init__(self):
        super().__init__()
        # Initial value stupidly high to avoid early sells
        self.marketHistory = [1_000_000]

        # Variables to play with!
        self.timeMax = 12  # months
        self.percentGainHappy = 0.2

    def applyOrderStrategy(self, income: float, dp: MarketDatapoint):
        sma = 0
        if len(self.marketHistory) > 0:
            sma = sum(self.marketHistory) / len(self.marketHistory)

        # If the stock is % above the SMA, sell our entire position
        if dp.marketClose > sma * (1 + self.percentGainHappy):
            self.bankBalance += self.stockShareCount * dp.marketClose
            self.stockShareCount = 0
            # Also add income to our bank balance
            self.bankBalance += income
        # If the stock is % below the SMA, buy as much as we can!
        elif dp.marketClose < sma * (1 - self.percentGainHappy):
            stockShareCount = (self.bankBalance + income) / dp.marketClose
            self.stockShareCount += stockShareCount
            # Also subtract the cost from our bank balance
            self.bankBalance = 0
            # We also don't keep income here, so moving on!
        # Otherwise, continue DCAing
        else:
            stockShareCount = income / dp.marketClose
            self.stockShareCount += stockShareCount

        # Add the datapoint to our history, popping the oldest after timeMax
        self.marketHistory.append(dp.marketClose)
        if len(self.marketHistory) > self.timeMax:
            self.marketHistory.pop(0)
