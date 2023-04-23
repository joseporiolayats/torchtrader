import asyncio

from torchtrader.data.database import Asset
from torchtrader.data.database import TorchtraderDatabase


async def create_asset_table(db: TorchtraderDatabase):
    create_table_query = """
    CREATE TABLE IF NOT EXISTS assets (
        asset_id TEXT PRIMARY KEY,
        symbol TEXT NOT NULL,
        name TEXT NOT NULL,
        is_crypto BOOLEAN NOT NULL
    )
    """
    await db.query_data_points(create_table_query)


async def add_assets(db: TorchtraderDatabase):
    assets = [
        {"asset_id": "BTC", "symbol": "BTC", "name": "Bitcoin", "is_crypto": True},
        {"asset_id": "ETH", "symbol": "ETH", "name": "Ethereum", "is_crypto": True},
        {"asset_id": "AAPL", "symbol": "AAPL", "name": "Apple Inc.", "is_crypto": False},
    ]

    for asset in assets:
        existing_asset = await db.get_asset(asset["asset_id"])
        if not existing_asset:
            await db.add(Asset, asset)
            print(f"Added asset: {asset['name']} ({asset['symbol']})")
        else:
            print(f"Asset {asset['name']} ({asset['symbol']}) already exists")


async def main():
    db = TorchtraderDatabase()

    # Create the Asset table if it doesn't exist
    await create_asset_table(db)

    # Add assets
    await add_assets(db)

    # Close the database session
    await db.close_session()


if __name__ == "__main__":
    asyncio.run(main())
