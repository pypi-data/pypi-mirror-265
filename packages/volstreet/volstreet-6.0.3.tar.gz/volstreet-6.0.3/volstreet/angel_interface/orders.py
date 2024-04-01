from time import sleep
import numpy as np
from SmartApi.smartExceptions import DataException
from volstreet import config
from volstreet.config import token_exchange_dict, logger
from volstreet.utils import custom_round
from volstreet.angel_interface.interface import (
    fetch_book,
    lookup_and_return,
    LiveFeeds,
    fetch_quotes,
    place_order_params,
    modify_order_params,
)


def generate_order_params(
    symbol: str,
    token: str,
    qty: int,
    action: str,
    price: str | float,
    order_tag: str = "",
    stop_loss_order: bool = False,
) -> dict:
    """Price can be a str or a float because "market" is an acceptable value for price."""
    action = action.upper()
    if isinstance(price, str):
        price = price.upper()
    order_tag = (
        "Automated Order" if (order_tag == "" or order_tag is None) else order_tag
    )
    exchange = token_exchange_dict[token]
    params = {
        "tradingsymbol": symbol,
        "symboltoken": token,
        "transactiontype": action,
        "exchange": exchange,
        "producttype": "CARRYFORWARD",
        "duration": "DAY",
        "quantity": int(qty),
        "ordertag": order_tag,
    }

    if stop_loss_order:
        execution_price = price * 1.1
        params.update(
            {
                "variety": "STOPLOSS",
                "ordertype": "STOPLOSS_LIMIT",
                "triggerprice": round(price, 1),
                "price": round(execution_price, 1),
            }
        )
    else:
        order_type, execution_price = (
            ("MARKET", 0) if price == "MARKET" else ("LIMIT", price)
        )
        execution_price = custom_round(execution_price)
        params.update(
            {"variety": "NORMAL", "ordertype": order_type, "price": execution_price}
        )

    return params


def place_order(
    symbol: str,
    token: str,
    qty: int,
    action: str,
    price: str | float,
    order_tag: str = "",
    stop_loss_order: bool = False,
) -> str:
    params = generate_order_params(
        symbol, token, qty, action, price, order_tag, stop_loss_order
    )
    return place_order_params(params)


def get_open_orders(
    order_book: list,
    order_ids: list[str] | tuple[str] | np.ndarray[str] = None,
    statuses: list[str] | tuple[str] | np.ndarray[str] = None,
):
    """Returns a list of open order ids. If order_ids is provided,
    it will return open orders only for those order ids. Otherwise,
    it will return all open orders where the ordertag is not empty.
    """
    if order_ids is None:
        order_ids = [
            order["orderid"] for order in order_book if order["ordertag"] != ""
        ]
    if statuses is None:
        statuses = ["open", "open pending", "modified", "modify pending"]
    open_orders_with_params: np.ndarray[dict] = lookup_and_return(
        order_book,
        ["orderid", "status"],
        [order_ids, statuses],
        config.modification_fields,
    )
    return open_orders_with_params


def update_order_params(
    current_params: dict, market_depth: dict, additional_buffer: float = 0
) -> dict:
    """Additional buffer is a percentage value that can further modify the price of the order.
    Additional buffer can be used when iteratively modifying orders to speed up the execution of persistently
    open orders."""

    action = current_params["transactiontype"]
    target_depth = "buy" if action == "SELL" else "sell"
    market_price = market_depth[target_depth][0]["price"]
    modifier = (
        (1 + config.LIMIT_PRICE_BUFFER + additional_buffer)
        if action == "BUY"
        else (1 - config.LIMIT_PRICE_BUFFER - additional_buffer)
    )

    new_price = market_price * modifier
    new_price = max(0.05, new_price)
    new_price = custom_round(new_price)

    modified_params = current_params.copy()
    modified_params["price"] = new_price
    current_params["price"] = new_price
    modified_params.pop("status")

    return modified_params


def modify_orders(open_orders_params: list[dict] | np.ndarray[dict]):
    ltp_cache = fetch_quotes(
        [order["symboltoken"] for order in open_orders_params],
        structure="dict",
    )

    for order in open_orders_params:
        market_depth = ltp_cache[order["symboltoken"]]["depth"]
        modified_params = update_order_params(order, market_depth)

        try:
            modify_order_params(modified_params)
        except Exception as e:
            if isinstance(e, DataException):
                sleep(1)
            logger.error(f"Error in modifying order: {e}")


def handle_open_orders(
    order_ids: list[str] | tuple[str] | np.ndarray[str],
    current_iteration: int = 0,
    cached_orderbook: list = None,
):
    """This will combine the functionality of both the turbo and backup mode, retaining the updated orderbook
    functionality of the turbo mode and the static version of the backup mode to fall back on.
    """
    modify_percentage = config.MODIFICATION_STEP_SIZE
    max_modification = config.MAX_PRICE_MODIFICATION
    max_iterations = max(int(max_modification / modify_percentage), 1)

    if current_iteration >= max_iterations:
        logger.info("Max iterations reached, exiting modification")
        return

    if LiveFeeds.order_feed_connected():
        logger.info(f"Using turbo mode to modify orders")
        order_book = LiveFeeds.order_book
    else:
        order_book = (
            fetch_book("orderbook") if cached_orderbook is None else cached_orderbook
        )

    open_orders_with_params: np.ndarray[dict] = get_open_orders(order_book, order_ids)
    if len(open_orders_with_params) == 0:
        return

    modify_orders(open_orders_with_params)

    open_order_ids = [order["orderid"] for order in open_orders_with_params]
    return handle_open_orders(open_order_ids, current_iteration + 1, order_book)
