import asyncio
from datetime import datetime
from datetime import timedelta

from torchtrader.data.collection import MarketData
from torchtrader.utils import timeframe_to_seconds


market_data = MarketData("binance")
start_time = datetime.now() - timedelta(days=30)
end_time = datetime.now() - timedelta(days=29)
start_str = start_time.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
end_str = end_time.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
base = "BTC"
quote = "USDT"
timeframe = "1m"
timeframe_in_seconds = timeframe_to_seconds(timeframe)


async def main():
    # Example 1: Get data with start_time and end_time

    data = await market_data.get_data(base, quote, timeframe, start_str, end_str)
    print("Example 1: Data with start_time and end_time")
    print(data)

    await asyncio.sleep(2)

    # Example 2: Get data without specifying time period
    data = await market_data.get_data(base, quote, timeframe)
    print("\nExample 2: Data without specifying time period")
    print(data)

    await asyncio.sleep(2)

    # Example 3: Get live data
    stop_event = asyncio.Event()
    print("\nExample 3: Get live data")
    while True:
        try:
            live_data = await market_data.get_live_data(base, quote, timeframe, stop_event)
            print(live_data)
            await asyncio.sleep(timeframe_in_seconds)  # Sleep for (timeframe)
        except KeyboardInterrupt:
            stop_event.set()
            break


if __name__ == "__main__":
    asyncio.run(main())
