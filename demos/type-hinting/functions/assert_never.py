#!/bin/env python3.11
import enum
from typing import assert_never

# Never добавлена только в python 3.11
# assert_never доступна в python 3.11 из typing. В версиях ниже - из typing_extensions
#
# assert_never вызывает исключение.
#
# Пододные камни assert_never
#
# При использовании coverage может возникнуть некoторые проблемы. Короче говоря программа coverage не увидет
# случае такие как "case _ as unreachable:" и "assert_never(...)"
#
# Для решения этой проблемы можно использовать настройку coverage в `pyproject.toml`:
#
# [tool.coverage.report]
# exclude_lines = [
#     '^ +assert_never\(.*?\)$',
#     '^ +case _ as unreachable:$',
# ]


class Status(enum.IntEnum):
    BAD = 1
    GOOD = 0


def main() -> None:
    status = Status.GOOD

    match status:
        case Status.GOOD:
            print("Status is GOOD!")
        case Status.BAD:
            print("Status is BAD!")
        case _ as unreachable:
            assert_never(unreachable)


def int_or_str(arg: int | str) -> None:
    match arg:
        case int():
            print("It's an int")
        case str():
            print("It's a str")
        case _ as unreachable:
            assert_never(unreachable)
