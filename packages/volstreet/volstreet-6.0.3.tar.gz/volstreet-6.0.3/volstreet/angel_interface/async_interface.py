import asyncio
from collections import defaultdict
import functools
from typing import Callable
from itertools import groupby
from volstreet import config
from volstreet.config import token_exchange_dict, logger
from volstreet.angel_interface.orders import update_order_params
from volstreet.angel_interface.active_session import ActiveSession


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
                    logger.error(message, exc_info=True)
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
        )  # todo: raise exception here after testing


def filter_for_open_orders(statuses: list[dict]) -> list[dict]:
    open_orders = [status for status in statuses if status["status"] == "open"]
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


async def _execute_orders(orders: list[dict], session=None):
    """
    Pass a list of order params to this function.
    Executes a list of orders in a loop until all orders are executed.
    Or max iterations are reached.
    """

    order_ids = await place_orders(orders, session)
    statuses = await fetch_statuses(order_ids, session)
    check_for_rejection(statuses)
    open_orders = filter_for_open_orders(statuses)

    iteration = 0
    while open_orders:
        iteration += 1
        if iteration == 10:
            logger.error("Max iterations reached. Exiting loop.")
            break
        additional_buffer = iteration / 100
        ltp_data = await get_quotes_async(
            [order["symboltoken"] for order in open_orders], session=session
        )
        await modify_open_orders(open_orders, ltp_data, additional_buffer, session)
        statuses = await fetch_statuses(order_ids, session)
        check_for_rejection(statuses)
        open_orders = filter_for_open_orders(statuses)

    logger.info("All orders executed successfully.")


async def execute_orders(orders: list[dict], grouper: Callable = None):
    """The difference between this function and execute_orders is that this function
    groups the orders before executing them parallely. The grouping is done based on the grouper
    function provided. The grouper function is iterated over the list of order params (dicts)
    """
    if grouper is not None:
        orders.sort(key=grouper)
        orders_grouped = groupby(orders, key=grouper)
    else:
        orders_grouped = [(None, orders)]

    async with ActiveSession.obj.async_session() as session:
        order_tasks = [
            _execute_orders([*order_group], session=session)
            for _, order_group in orders_grouped
        ]
        await asyncio.gather(*order_tasks)
