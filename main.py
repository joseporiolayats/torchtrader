"""
Torchtrader Main Module

This module contains the main script for the Torchtrader app, a simple trading app for stocks and
cryptocurrencies. It accepts command-line arguments for trading and logs messages using the logger
module.
"""
import argparse
import sys

from torchtrader.logs.logger import app_logger
from torchtrader.logs.logger import trade_logger


def trade_stocks(api_key, symbol, action, quantity):
    """
    Execute a trade order for stocks.

    Args:
        api_key (str): The API key for the trading account.
        symbol (str): The stock symbol to trade.
        action (str): The action to perform (buy or sell).
        quantity (int): The number of shares to trade.
    """
    app_logger.info(f"Trading stocks with API key: {api_key}")
    trade_logger.debug(f"Symbol: {symbol}, Action: {action}, Quantity: {quantity}")
    # Implement your stock trading logic here.


def trade_crypto(api_key, symbol, action, quantity):
    """
    Execute a trade order for cryptocurrencies.

    Args:
        api_key (str): The API key for the trading account.
        symbol (str): The cryptocurrency symbol to trade.
        action (str): The action to perform (buy or sell).
        quantity (int): The number of units to trade.
    """
    app_logger.info(f"Trading cryptocurrencies with API key: {api_key}")
    trade_logger.debug(f"Symbol: {symbol}, Action: {action}, Quantity: {quantity}")
    # Implement your cryptocurrency trading logic here.


def main(args):
    """
    The main function for the Torchtrader app. It parses command-line arguments and calls the
    appropriate trading function based on the provided arguments.

    Args:
        args (list): Command-line arguments for the app.
    """
    parser = argparse.ArgumentParser(
        description="Torchtrader: A simple trading app for stocks and cryptocurrencies."
    )

    parser.add_argument("api_key", type=str, help="API key for your trading account.")
    parser.add_argument(
        "asset_type",
        type=str,
        choices=["stock", "crypto"],
        help="The type of asset to trade: 'stock' or 'crypto'.",
    )
    parser.add_argument("symbol", type=str, help="The symbol of the asset you want to trade.")
    parser.add_argument(
        "action",
        type=str,
        choices=["buy", "sell"],
        help="The action you want to perform: 'buy' or 'sell'.",
    )
    parser.add_argument(
        "quantity", type=int, help="The number of shares or units of the asset you want to trade."
    )

    parsed_args = parser.parse_args(args)

    if parsed_args.asset_type == "stock":
        trade_stocks(
            parsed_args.api_key, parsed_args.symbol, parsed_args.action, parsed_args.quantity
        )
    elif parsed_args.asset_type == "crypto":
        trade_crypto(
            parsed_args.api_key, parsed_args.symbol, parsed_args.action, parsed_args.quantity
        )
    else:
        raise ValueError("Invalid asset type. Choose either 'stock' or 'crypto'.")


if __name__ == "main":
    main(sys.argv[1:])
