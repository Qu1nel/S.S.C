#!/bin/env python3.11
from functools import wraps
from typing import Any, Callable, TypeVar, cast

# Иногда анализатор статический анализатор не может корректно определить тип переменной, в этом случае можно
# использовать функцию cast. Её единственная задача — показать анализатору, что выражение имеет определённый тип.
# Например:


def find_first_str(a: list[Any]):
    index = next(i for i, x in enumerate(a) if isinstance(x, str))
    return cast(str, a[index])


string = find_first_str([123, "i'm a first string", 346, 2630.90j, 23.632])
print(string)
# Даже без указания возвращаемого типы, анализатор всё равно понимает какой тип должна вернуть функция.

# Также это может быть полезно для декораторов:

TMyCallable = TypeVar("TMyCallable", bound=Callable)


def logged(func: TMyCallable) -> TMyCallable:
    @wraps(func)
    def inner(*args, **kwargs):
        print(func.__name__, args, kwargs)
        return func(*args, **kwargs)

    return cast(TMyCallable, inner)
    # return inner  # TypeHint Error


@logged
def mysum(a: int, b: int) -> int:
    return a + b


mysum(a=1)  # TypeHint Error
