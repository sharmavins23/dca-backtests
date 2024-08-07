import os
from dataclasses import dataclass
import datetime

from strategies.Sit import Sit
from strategies.DCA import DCA
from strategies.HedgedDCA import HedgedDCA
from strategies.VLGEBDCA import VLGEBDCA
from strategies.SMABuySell import SMABuySell
from strategies.BBMEDCA import BBMEDCA
from strategies.AddBBMEDCA import AddBBMEDCA
from strategies.StocksGoUp import StocksGoUp

from utils import MarketDatapoint
import matplotlib.pyplot as plt

# ===== Global variables =======================================================

# Monthly cashflow/income
monthlyIncome = 3_000.00  # USD for stock investing

# Yield rates, historically
yieldRates = []

# Stock tickers - Data from Yahoo! Finance historical trends
tickers = [filename for filename in os.listdir(
    "tickers") if filename.endswith(".csv")]
tickers = [ticker[:-4] for ticker in tickers]
strategies = [Sit, DCA, HedgedDCA, VLGEBDCA,
              SMABuySell, BBMEDCA, AddBBMEDCA, StocksGoUp]

# ===== Data processing step ===================================================


# Given a ticker, return a full list of all market datapoints
def getMarketDatapoints(ticker: str) -> list[MarketDatapoint]:
    datapoints = []
    with open(f"tickers/{ticker}.csv", "r") as file:
        for line in file:
            data = line.split(",")
            if data[0] == "Date":
                continue
            if data[1] == "null":
                continue
            dp = MarketDatapoint(
                date=datetime.datetime.strptime(
                    data[0], "%Y-%m-%d").date(),
                marketOpen=float(data[1]),
                marketHigh=float(data[2]),
                marketLow=float(data[3]),
                marketClose=float(data[4]),
                marketAdjClose=float(data[5]),
                marketVolume=int(data[6])
            )
            datapoints.append(dp)
    return datapoints


# Collect all yield rates once so we don't have to do it again several times
def getYieldRates():
    # Start by collecting all of the FRB_H15 yield rates
    with open("data/FRB_H15.csv", "r") as file:
        for line in file:
            data = line.split(",")

            # Some data points don't exist
            if data[4] == "ND" or data[4] == "null":
                continue

            date = datetime.datetime.strptime(data[0], "%Y-%m-%d").date()
            yieldRate = float(data[4])
            yieldRates.append((date, yieldRate))


# Given a date, return the nearest FRB_H15 yield rate as a monthly rate
def getMonthlyFederalYieldRate(date: datetime.date) -> float:
    # Iterate through the list and find the last yield rate before the date
    for i in range(len(yieldRates)):
        if yieldRates[i][0] > date:
            # Check! If this date is before the first date, we return the first
            #  yield rate
            if i == 0:
                annualYieldRate = yieldRates[0][1] / 100.0
                return (1 + annualYieldRate) ** (1 / 12) - 1

            annualYieldRate = yieldRates[i - 1][1] / 100.0
            return (1 + annualYieldRate) ** (1 / 12) - 1

    # If we reach this point, we have no data for this date, in which case we
    #  yield the latest yield rate
    annualYieldRate = yieldRates[-1][1] / 100.0
    return (1 + annualYieldRate) ** (1 / 12) - 1


# ===== Driver code ============================================================


def main():
    # Collect our datapoints and create our strategy objects
    getYieldRates()
    datapoints = {ticker: getMarketDatapoints(ticker) for ticker in tickers}
    strategyTrackers = {ticker: [] for ticker in tickers}
    for ticker in tickers:
        for strategy in strategies:
            strategyTrackers[ticker].append(strategy())

    # * Data collection

    # Iterate through each datapoint and apply it to each strategy
    for ticker in tickers:
        for dp in datapoints[ticker]:
            for strategy in strategyTrackers[ticker]:
                strategy.preApplyOrderStrategy(
                    getMonthlyFederalYieldRate(dp.date))
                strategy.applyOrderStrategy(monthlyIncome, dp)
                strategy.postApplyOrderStrategy(dp)

    # Now print out the bank balance of each strategy
    for ticker in tickers:
        for strategy in strategyTrackers[ticker]:
            print(f"Strategy {strategy.__class__.__name__} for {
                  ticker} has a net worth of ${strategy.netWorth:,.2f}")

    # * Data aggregation

    # Make one graph for each ticker
    for ticker in tickers:
        plt.figure()
        plt.title(f"Net worth of strategies for {ticker}")
        plt.xlabel("Date")
        plt.ylabel("Net worth (USD)")
        for strategy in strategyTrackers[ticker]:
            plt.plot([dp.date for dp in datapoints[ticker]],
                     strategy.netWorthHistory, label=strategy.__class__.__name__)
        plt.legend()
        plt.savefig(f"graphs/Stock_{ticker}.png")
        plt.close()

    # Also make one graph for each strategy
    for strategy in strategies:
        plt.figure()
        plt.title(f"Net worth of strategies for {strategy.__name__}")
        plt.xlabel("Date")
        plt.ylabel("Net worth (USD)")
        for ticker in tickers:
            for strategyTracker in strategyTrackers[ticker]:
                if isinstance(strategyTracker, strategy):
                    plt.plot([dp.date for dp in datapoints[ticker]],
                             strategyTracker.netWorthHistory, label=ticker)
        plt.legend()
        plt.savefig(f"graphs/Strat_{strategy.__name__}.png")
        plt.close()

    # Let's also make a graph for each ticker normalized over Sit strategy
    for ticker in tickers:
        plt.figure()
        plt.title(f"Net worth of strategies for {ticker} (norm. Sit)")
        plt.xlabel("Date")
        plt.ylabel("Net worth (ratio)")
        for strategy in strategyTrackers[ticker]:
            plt.plot([dp.date for dp in datapoints[ticker]],
                     [nw / strategyTrackers[ticker][0].netWorthHistory[i]
                      for i, nw in enumerate(strategy.netWorthHistory)],
                     label=strategy.__class__.__name__)
        plt.legend()
        plt.savefig(f"graphs/Stock_{ticker}_Normalized.png")
        plt.close()

    # Finally, let's create graphs for each ticker normalized over DCA strategy
    for ticker in tickers:
        plt.figure()
        plt.title(f"Net worth of strategies for {ticker} (norm. DCA)")
        plt.xlabel("Date")
        plt.ylabel("Net worth (ratio)")
        for strategy in strategyTrackers[ticker]:
            plt.plot([dp.date for dp in datapoints[ticker]],
                     [nw / strategyTrackers[ticker][1].netWorthHistory[i]
                      for i, nw in enumerate(strategy.netWorthHistory)],
                     label=strategy.__class__.__name__)
        plt.legend()
        plt.savefig(f"graphs/Stock_{ticker}_Normalized_DCA.png")
        plt.close()


if __name__ == "__main__":
    main()
