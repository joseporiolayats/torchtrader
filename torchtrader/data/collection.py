"""
torchtrader/data/collection.py
"""
import asyncio
from contextlib import asynccontextmanager
from dataclasses import dataclass
from typing import Any
from typing import Dict
from typing import List
from typing import Optional

import ccxt.async_support as ccxt


@dataclass
class OHLCV:
    timestamp: int
    base: str
    quote: str
    open: float
    high: float
    low: float
    close: float
    volume: float
    timeframe: str


class MarketData:
    def __init__(self, market: str):
        self.market = market.lower()
        self.exchange = None
        self.is_crypto = None

    @asynccontextmanager
    async def setup_exchange(self):
        if self.market not in ccxt.exchanges:
            raise ValueError(f"Market '{self.market}' not supported by CCXT")
        exchange_class = getattr(ccxt, self.market)
        self.exchange = exchange_class({"enableRateLimit": True})
        markets = await self.exchange.load_markets()
        self.is_crypto = "BTC/USDT" in markets
        try:
            yield
        finally:
            await self.exchange.close()

    async def get_data(
        self,
        base: str,
        quote: str,
        timeframe: str,
        start_time: Optional[str] = None,
        end_time: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        async with self.setup_exchange():
            symbol = f"{base}/{quote}"
            since = self.exchange.parse8601(start_time) if start_time else None
            if end_time:
                limit = int(
                    (self.exchange.parse8601(end_time) - since)
                    / self.exchange.parse_timeframe(timeframe)
                )
            else:
                limit = 1000

            data = await self.exchange.fetch_ohlcv(symbol, timeframe, since, limit)
            return self.process_data(data, base, quote, timeframe)

    async def get_live_data(
        self, base: str, quote: str, timeframe: str, stop_event: asyncio.Event
    ) -> list[dict[str, Any]]:
        async with self.setup_exchange():
            symbol = f"{base}/{quote}"

            while not stop_event.is_set():
                data = await self.exchange.fetch_ohlcv(symbol, timeframe, limit=1)
                return self.process_data(data, base, quote, timeframe)

    @staticmethod
    def process_data(
        data: List[List[float]], base: str, quote: str, timeframe: str
    ) -> List[Dict[str, Any]]:
        processed_data = []
        for entry in data:
            timestamp, open_, high, low, close, volume = entry
            ohlcv = OHLCV(timestamp, base, quote, open_, high, low, close, volume, timeframe)
            processed_data.append(ohlcv.__dict__)
        return processed_data
