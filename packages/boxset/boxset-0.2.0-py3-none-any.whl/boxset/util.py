import functools
import itertools
import time
from threading import Lock
from typing import Any, Callable, Generator, Iterable


def split_seq(
    iterable: Iterable[Any],
    size: int,
) -> Generator[list[Any], None, None]:
    """
    Split a long sequence into smaller chunks of given size.
    Yields:
        Generator[list[Any], None, None]: A generator that yields lists of items.

    Examples:
        >>> list(split_seq(range(10), 3))
        [[0, 1, 2], [3, 4, 5], [6, 7, 8], [9]]

        >>> list(split_seq(range(10), 2))
        [[0, 1], [2, 3], [4, 5], [6, 7], [8, 9]]
    """
    # iterator: Iterator[Any] = iter(iterable)
    # while True:
    #     res: list[Any] = []
    #     try:
    #         for _ in range(size):
    #             item = next(iterator)
    #             if callback:
    #                 item = callback(item)
    #             if not is_skip_empty or item:
    #                 res.append(item)
    #     except StopIteration:
    #         if res:
    #             yield res
    #         break
    #     else:
    #         yield res
    it = iter(iterable)
    item = list(itertools.islice(it, size))
    while item:
        yield item
        item = list(itertools.islice(it, size))


# 10的3次方
ONE_K = 10**3
ONE_W = 10**4
ONE_KW = 10**7


def cn_human_number(num):
    """
    Convert a number to a human-readable string representation.

    Args:
        num (int or float): The number to be converted.

    Returns:
        str: The human-readable string representation of the number.

    Examples:
        >>> cn_human_number(123)
        '123'
        >>> cn_human_number(1234)
        '1.2k'
        >>> cn_human_number(12345678)
        '1.2kw'
        >>> cn_human_number(123456789)
        '12.3kw'
        >>> cn_human_number(12345678901)
        '1.2e+10'
    """
    if num < ONE_K:
        return str(num)
    elif num < ONE_W:
        return f"{num/ONE_K:.1f}k"
    elif num < ONE_KW:
        return f"{num/ONE_W:.1f}w"
    elif num < 100 * ONE_KW:
        return f"{num/ONE_KW:.1f}kw"
    else:
        # 科学计数法
        return f"{num:.1e}"


def delay_decorator(delay_seconds: float) -> Callable:
    """
    Decorator that delays the execution of a function by a specified number of seconds.

    Args:
        delay_seconds (float): The number of seconds to delay the function execution.

    Returns:
        Callable: The decorated function.

    Examples:
        >>> import time
        >>> @delay_decorator(0.5)
        ... def my_func():
        ...     return time.time()
        ...
        >>> my_func() - time.time() > -0.01 # 第一次调用不会延迟
        True
        >>> my_func() - my_func() < -0.5
        True

        >>> @delay_decorator(0.5)
        ... def add(a, b):
        ...     return a + b
        ...
        >>> add(1, 2)
        3
        >>> add(3, 4)
        7
    """

    def decorator(func: Callable) -> Callable:
        last_executed: float = 0
        lock = Lock()

        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            nonlocal last_executed
            current_time = time.time()
            time_diff = current_time - last_executed

            with lock:
                if time_diff < delay_seconds and last_executed != 0:
                    wait_time = delay_seconds - time_diff
                    time.sleep(wait_time)

                result = func(*args, **kwargs)
                last_executed = time.time()

            return result

        return wrapper

    return decorator


# 可以减少智能匹配的推荐量
__all__ = ["split_seq", "cn_human_number", "delay_decorator"]
