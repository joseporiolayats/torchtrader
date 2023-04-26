from torchtrader.data.ops_specific import OpsSpecific

# Initialize OpsSpecific class
ops = OpsSpecific()

# Create an exchange
exchange_data = {
    "name": "Example Exchange",
}
exchange_id = ops.create_exchange(exchange_data)
# print(f"Created exchange with ID: {exchange_id}")

# Read exchanges
exchanges = ops.read_exchange()
# print(f"Exchanges: {exchanges}")

# Update an exchange
exchange_update_data = {"name": "Updated Example Exchange"}
ops.update_exchange(exchange_data, exchange_update_data)
# print("Updated exchange name")

# Create a trading product
trading_product_data = {
    "name": "Example Trading Product",
    "product_type": "Cryptocurrency",
    "ticker": "EXC",
}
trading_product_id = ops.create_trading_product(trading_product_data)
# print(f"Created trading product with ID: {trading_product_id}")

# Read trading products
trading_products = ops.read_trading_product()
# print(f"Trading products: {trading_products}")

# Update a trading product
trading_product_update_data = {"name": "Updated Example Trading Product"}
ops.update_trading_product(trading_product_data, trading_product_update_data)
# print("Updated trading product name")

# Create a trading product exchange relationship
trading_product_exchange_data = {
    "exchange_id": exchange_id,
    "trading_product_id": trading_product_id,
}
trading_product_exchange_id = ops.create_trading_product_exchange(trading_product_exchange_data)
# print(f"Created trading product exchange relationship with ID: {trading_product_exchange_id}")

# Read trading product exchange relationships
trading_product_exchanges = ops.read_trading_product_exchange()
# print(f"Trading product exchange relationships: {trading_product_exchanges}")

# Update a trading product exchange relationship
trading_product_exchange_update_data = {"exchange_id": 2}  # Assuming another exchange exists
ops.update_trading_product_exchange(
    trading_product_exchange_data, trading_product_exchange_update_data
)
# print("Updated trading product exchange relationship")

# Create an asset
asset_data = {
    "name": "Example Asset",
    "base_currency": "USD",
    "quote_currency": "EXMP",
    "trading_product_id": trading_product_id,
    "exchange_id": exchange_id,
}
asset_id = ops.create_asset(asset_data)

# Read assets
assets = ops.read_asset()
# print(f"Assets: {assets}")

# Update an asset
asset_updates = {"name": "Updated Example Asset"}
ops.update_asset({"id": asset_id}, asset_updates)

# Read updated assets
updated_assets = ops.read_asset()
# print(f"Updated Assets: {updated_assets}")

# Delete an asset
ops.delete_asset({"id": asset_id})

# Read assets after deletion
remaining_assets = ops.read_asset()
# print(f"Remaining Assets: {remaining_assets}")

# # Delete a trading product exchange relationship
ops.delete_trading_product_exchange(trading_product_exchange_update_data)
# print("Deleted trading product exchange relationship")
#
# # Delete a trading product
ops.delete_trading_product(trading_product_update_data)
# print("Deleted trading product")
#
# # Delete an exchange
ops.delete_exchange(exchange_update_data)
# print("Deleted exchange")
