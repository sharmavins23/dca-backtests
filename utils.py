from dataclasses import dataclass
import datetime


@dataclass
class MarketDatapoint:
    date: datetime.date
    marketOpen: float
    marketHigh: float
    marketLow: float
    marketClose: float
    marketAdjClose: float
    marketVolume: int
