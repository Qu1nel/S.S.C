#!/usr/bin/env python3.11
from typing import Callable

# Callable[[t1, t2, ..., tn], tr] - вызываемый объект с позиционными аргументами t1, t2, ... и возвращаемым типом tr.

# Список аргументов может быть пустым n==0. Нет способа указать необязательные или ключевые аргументы, а также varargs,
# но вы можете сказать, что список аргументов полностью не проверяется, написав Callable[..., tr].


def func(a: int) -> str: ...
def wrapper(func: Callable[[int], str]): ...


wrapper(func)


def another_func(a: int, b: float) -> str:
    return str(a + b)


def another_wrapper(func: Callable[[int, float], str]): ...


another_wrapper(another_func)
another_wrapper(func)


def spam(a) -> None:
    print(a + 2)


def spam2() -> None: ...


def wrap(func: Callable[[], None]):
    print(func)


wrap(spam)
wrap(spam2)


def wrap2(func: Callable[..., None]):
    print(func)


# Callable[..., None] говорит за себя "я как бы хз что я могу принять".

def partial(func: Callable[..., str], *args) -> Callable[..., str]: ...


wrap2(spam)
wrap2(spam2)
