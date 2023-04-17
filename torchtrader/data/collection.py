import asyncio
from dataclasses import dataclass
from datetime import datetime
from typing import Dict
from typing import Union

import ccxt
import ccxt.async_support as ccxt_async

from torchtrader.logs.logger import app_logger


@dataclass
class OHLCV:
    timestamp: int
    open: float
    high: float
    low: float
    close: float
    volume: float


class MarketData:
    def __init__(self, market: str):
        self.market = market.lower()
        self.is_crypto = self._check_market_type()
        self.exchange = self._initialize_exchange()

    def _check_market_type(self) -> bool:
        if self.market in ccxt.exchanges:
            return True
        else:
            raise ValueError(f"Market '{self.market}' is not supported by ccxt")

    def _initialize_exchange(self) -> Union[ccxt.Exchange, ccxt_async.Exchange]:
        if self.is_crypto:
            exchange_class = getattr(ccxt_async, self.market)
        else:
            exchange_class = getattr(ccxt, self.market)

        return exchange_class()

    async def get_historical_data(
        self, symbol: str, timeframe: str, since: int = None, limit: int = None
    ) -> Dict[str, OHLCV]:
        app_logger.info(
            f"Fetching historical data for {symbol} on {self.market} with timeframe {timeframe}"
        )
        try:
            ohlcv_data = await self.exchange.fetch_ohlcv(symbol, timeframe, since, limit)
            await self.exchange.close()
            return {entry[0]: OHLCV(*entry) for entry in ohlcv_data}
        except Exception as e:
            app_logger.error(
                f"Error fetching historical data for {symbol} on {self.market}: {str(e)}"
            )
            raise

    async def close(self):
        await self.exchange.close()

    async def run(self, symbol: str, timeframe: str, since: int = None, limit: int = None):
        data = await self.get_historical_data(symbol, timeframe, since, limit)
        await self.close()
        return data

    async def get_historical_data_for_period(
        self, symbol: str, timeframe: str, start_time: datetime, end_time: datetime
    ) -> Dict[str, OHLCV]:
        app_logger.info(
            f"Fetching historical data for {symbol} on {self.market} with timeframe"
            f" {timeframe} between {start_time} and {end_time}"
        )

        start_timestamp = int(start_time.timestamp() * 1000)
        end_timestamp = int(end_time.timestamp() * 1000)
        limit = 1000

        ohlcv_data = {}
        while start_timestamp <= end_timestamp:
            try:
                new_data = await self.exchange.fetch_ohlcv(
                    symbol, timeframe, start_timestamp, limit
                )
                if not new_data:
                    break

                for entry in new_data:
                    ohlcv_data[entry[0]] = OHLCV(*entry)
                await self.exchange.close()
                start_timestamp = new_data[-1][0] + self.exchange.parse_timeframe(timeframe) * 1000

            except Exception as e:
                app_logger.error(
                    f"Error fetching historical data for {symbol} on {self.market}: {str(e)}"
                )
                raise

        app_logger.info(
            f"Fetched historical data for {symbol} on {self.market} with timeframe "
            f"{timeframe} between {start_time} and {end_time}"
        )
        return ohlcv_data


async def main():
    market = "binance"
    symbol = "BTC/USDT"
    timeframe = "1h"
    start_time = datetime(2021, 1, 1)
    end_time = datetime(2021, 1, 31)

    market_data = MarketData(market)
    await market_data.get_historical_data_for_period(symbol, timeframe, start_time, end_time)

    # Use ohlcv_data with the TorchtraderDatabase class here


if __name__ == "__main__":
    asyncio.run(main())
