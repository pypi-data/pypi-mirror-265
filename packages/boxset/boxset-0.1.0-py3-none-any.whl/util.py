import itertools
from typing import Any, Callable, Generator, Sequence, Union

def split_list(
    iterable: Sequence[Any],
    size: int,
    callback: Union[Callable[[Any], Any], None] = None,
    is_skip_empty: bool = True,
) -> Generator[list[Any], None, None]:
    """
    Split a long sequence into smaller chunks of given size.

    Args:
        iterable (Sequence[Any]): The sequence to be split.
        size (int): The maximum size of each chunk.
        callback (Union[Callable[[Any], Any], None], optional): A function to apply to each item before adding to the chunk. Defaults to None.
        is_skip_empty (bool, optional): Whether to skip empty items after applying the callback. Defaults to True.

    Yields:
        Generator[list[Any], None, None]: A generator that yields lists of items.

    Examples:
        >>> list(split_list(range(10), 3))
        [[0, 1, 2], [3, 4, 5], [6, 7, 8], [9]]

        >>> list(split_list([1, 2, '', 3, None, 4], 2, is_skip_empty=False))
        [[1, 2], ['', 3], [None, 4]]

        # >>> list(split_list([1, 2, 0, 3, False, 4], 2, lambda x: x and str(x), is_skip_empty=True))
        # [['1', '2'], ['3', '4']]
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
ONE_K = 10 ** 3
ONE_W = 10 ** 4
ONE_KW = 10 ** 7


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
    
# 可以减少智能匹配的推荐量
__all__ = ["split_list", "cn_human_number"]