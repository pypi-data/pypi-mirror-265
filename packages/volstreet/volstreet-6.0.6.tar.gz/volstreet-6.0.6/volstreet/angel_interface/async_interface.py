import asyncio
from collections import defaultdict
import functools
import threading
from itertools import groupby
import numpy as np
from volstreet import config
from volstreet.config import token_exchange_dict, logger
from volstreet.angel_interface.interface import lookup_and_return
from volstreet.angel_interface.orders import update_order_params
from volstreet.angel_interface.active_session import ActiveSession

order_placement_lock = threading.Lock()


def retry_on_error(func):
    """Only for async functions. Retries the function 5 times with exponential backoff if an error occurs."""

    @functools.wraps(func)
    async def async_wrapped(*args, **kwargs):
        sleep_time = 1
        for attempt in range(5):
            try:
                return await func(*args, **kwargs)
            except Exception as e:
                message = (
                    f"Attempt {attempt + 1} function {func.__name__} failed with error {e}. "
                    f"Retrying in {sleep_time} seconds."
                )
                if attempt < 4:
                    logger.warning(message, exc_info=True)
                    await asyncio.sleep(sleep_time)
                    sleep_time *= 1.2  # Exponential backoff
                else:
                    logger.error(f"Max attempts reached. {message}")
                    raise e

    return async_wrapped


@retry_on_error
async def get_ltp_async(params: dict, session=None):
    response = await ActiveSession.obj.async_get_ltp(params, session)
    return response["data"]["ltp"]


@retry_on_error
async def get_quotes_async(
    tokens: list, mode: str = "FULL", return_type="dict", session=None
):
    payload = defaultdict(list)
    for token in tokens:
        exchange = token_exchange_dict.get(token)
        if exchange:
            payload[exchange].append(token)
    payload = dict(payload)
    params = {"mode": mode, "exchangeTokens": payload}
    response = await ActiveSession.obj.async_get_quotes(params, session)

    # Formatting the response
    response = response["data"]["fetched"]
    if return_type.lower() == "dict":
        return {entry["symbolToken"]: entry for entry in response}
    elif return_type.lower() == "list":
        return response


@retry_on_error
async def place_order_async(params: dict, session=None):
    response = await ActiveSession.obj.async_place_order(params, session)
    return response["data"]


@retry_on_error
async def unique_order_status_async(unique_order_id: str, session=None):
    response = await ActiveSession.obj.async_unique_order_status(
        unique_order_id, session
    )
    return response["data"]


@retry_on_error
async def modify_order_async(params: dict, session=None):
    return await ActiveSession.obj.async_modify_order(params, session)


async def place_orders(list_of_orders: list[dict], session=None) -> list[str]:
    """Designed to be used for a specific action type.
    For example, all orders are BUY orders.
    """
    order_coros = [
        place_order_async(order, session=session) for order in list_of_orders
    ]
    results = await asyncio.gather(*order_coros)
    unique_ids = [result["uniqueorderid"] for result in results]
    return unique_ids


async def fetch_statuses(list_of_unique_ids: list[str], session=None) -> list[dict]:
    status_coros = [
        unique_order_status_async(unique_id, session=session)
        for unique_id in list_of_unique_ids
    ]
    # noinspection PyTypeChecker
    return await asyncio.gather(*status_coros)


def check_for_rejection(statuses: list[dict]):
    if any(status["status"] == "rejected" for status in statuses):
        logger.warning(
            f"One or more orders were rejected in batch: {statuses}"
        )  # todo: raise exception here after testing or implement rejection handling logic


def filter_for_open_orders(statuses: list[dict]) -> list[dict]:
    open_order_statuses = ["open", "open pending", "modified", "modify pending"]
    open_orders = [
        status for status in statuses if status["status"] in open_order_statuses
    ]
    if not open_orders:
        return []
    open_orders_formatted = [
        {field: status[field] for field in config.modification_fields}
        for status in open_orders
    ]
    return open_orders_formatted


async def modify_open_orders(
    open_orders: list[dict], ltp_data: dict, additional_buffer: float = 0, session=None
):
    modified_params = [
        update_order_params(
            order, ltp_data[order["symboltoken"]]["depth"], additional_buffer
        )
        for order in open_orders
    ]
    modify_coros = [modify_order_async(params, session) for params in modified_params]
    await asyncio.gather(*modify_coros)


def calculate_average_price(orders: list, ids: list[str]) -> float:
    avg_prices = lookup_and_return(
        orders, ["uniqueorderid", "status"], [ids, "complete"], "averageprice"
    )
    return avg_prices.astype(float).mean() if avg_prices.size > 0 else np.nan


async def execute_orders_per_symbol(orders: list[dict], symbol: str, session=None):
    """
    Used to execute orders for a particular action type and symbol token.
    Executes orders in a loop until all orders are executed.
    Or max iterations are reached.
    Returns the average price of all executed orders.
    """
    if session is None:
        with ActiveSession.obj.async_session() as session:
            await execute_orders_per_symbol(orders, symbol, session)
            return

    order_ids = await place_orders(orders, session)
    statuses = await fetch_statuses(order_ids, session)
    check_for_rejection(statuses)
    open_orders = filter_for_open_orders(statuses)

    iteration = 0
    while open_orders:
        iteration += 1
        if iteration == 10:
            logger.error(f"Max modification iterations reached for symbol {symbol}.")
            break
        additional_buffer = iteration / 100
        ltp_data = await get_quotes_async(
            [order["symboltoken"] for order in open_orders], session=session
        )
        await modify_open_orders(open_orders, ltp_data, additional_buffer, session)
        statuses = await fetch_statuses(order_ids, session)
        check_for_rejection(statuses)
        open_orders = filter_for_open_orders(statuses)

    logger.info(f"Orders successfully executed for symbol {symbol}.")

    avg_price = calculate_average_price(statuses, order_ids)
    return avg_price


async def _execute_orders(orders: list[dict]) -> dict:
    """The difference between this function and execute_order_group is that this function
    can take in orders of different action types and symbols. It groups the orders
    into transaction types and symbol tokens and executes them in parallel, prioritizing
    buy orders to be executed first.
    """
    master_dict = {}
    orders.sort(key=lambda x: x["transactiontype"])
    orders_grouped_by_action = groupby(orders, key=lambda x: x["transactiontype"])

    async with ActiveSession.obj.async_session() as session:
        for action, orders_per_action in orders_grouped_by_action:
            orders_per_action = list(orders_per_action)
            orders_per_action.sort(key=lambda x: x["tradingsymbol"])
            orders_grouped_by_symbol = groupby(
                orders_per_action, key=lambda x: x["tradingsymbol"]
            )
            orders_grouped_by_symbol = {
                symbol: list(orders_per_symbol)
                for symbol, orders_per_symbol in orders_grouped_by_symbol
            }  # Just converting it to a dict
            order_tasks = [
                execute_orders_per_symbol([*orders], symbol, session)
                for symbol, orders in orders_grouped_by_symbol.items()
            ]
            avg_prices = await asyncio.gather(*order_tasks)

            for symbol, avg_price in zip(orders_grouped_by_symbol.keys(), avg_prices):
                master_dict[symbol] = avg_price

    return master_dict


async def execute_orders(orders: list[dict]) -> dict:
    with order_placement_lock:
        logger.info(f"{threading.current_thread().name} is executing orders.")
        result = await _execute_orders(orders)
        return result
