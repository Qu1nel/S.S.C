#!/usr/bin/env python3.11
from typing import NoReturn


def always_exception() -> NoReturn:
    """Функция всегда вызывает исключение RuntimeError

    NoReturn используется тогда, когда функция всегда не может что-либо вернуть.
    Наример, функция безусловно вызывает исключение.
    """
    raise RuntimeError(f"Error: {id(1):x}")

# Важно понять, что NoReturn валидно используется только как возвращаемое* значение
# То есть следующие примеры являются ошибками.
#
# def bad1(x: NoReturn) -> int:
#   ...
#
# def bad1() -> List[NoReturn]:
#   ...
#
# def bad3() -> Optional[NoReturn]:
#   ...
#
# bad4: NoReturn = None


def main() -> None:
    always_exception()

    print("no way")  # Code is unreachable


if __name__ == "__main__":
    main()
