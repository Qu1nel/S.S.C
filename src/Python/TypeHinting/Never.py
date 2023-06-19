#!/usr/bin/env python3.11
from enum import Enum
from typing import Never, NoReturn, assert_never

# Аннотация typing.Never может быть использовано для определения функции, которая никогда не должна вызываться.
#
# Never добавлена только в python 3.11
# assert_never доступна в python 3.11 из typing. В версиях ниже - из typing_extensions
#
# assert_never вызывает исключение.
#
# Пододные камни assert_never
#
# При использовании coverage может возникнуть некторые проблемы. Короче говоря программа coverage не увидет
# случае такие как "case _ as unreachable:" и "assert_never(...)"
#
# Для решения этой проблемы можно использовать настройку coverage в `pyproject.toml`:
#
# [tool.coverage.report]
# exclude_lines = [
#     '^ +assert_never\(.*?\)$',
#     '^ +case _ as unreachable:$',
# ]


def never_call_me(arg: Never) -> NoReturn:
    raise AssertionError(f"Expected code to be unreachable, but got '{arg}'")


class Status(Enum):
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
            assert_never(unreachable)  # never_call_me(unreachable)


# Порой системы контроля типизации не настолько сильны, чтобы понять, что какой-то из кусков кода
# unreachable и для этого можно использовать следующий примем:
#
# def lowest_unused(street: str) -> int:
#     for i in itertools.count(1):
#         if not is_used(street, i):
#             return i
#     assert False, "unreachable code"

if __name__ == "__main__":
    main()
