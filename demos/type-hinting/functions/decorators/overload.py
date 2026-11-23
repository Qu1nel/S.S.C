#!/bin/env python3.11
import random
import typing
from collections.abc import Sequence

TPicture: typing.TypeAlias = list | set


# Декоратор @typing.overload() позволяет описывать функции и методы, которые поддерживают несколько различных=
# комбинаций типов аргументов. За серией определений с @overload должно следовать ровно одно определение без @overload
# (для той же функции/метода).

def double(input_: int | Sequence[int]) -> int | list[int]:
    if isinstance(input_, Sequence):
        return [i * i for i in input_]
    return input_ * 2

# При такой реализации типизации возникает ощущение "костыля", ведь в зависимости от типа аргумента input_ функция
# совершает совсем различную работы и следственно тип результата тоже отличается. Т.е. у нас возникает биекция между
# множеством входных типов и возвращаемых.


x = double(12)
typing.reveal_type(x)  # Покажет что тип int.
# Но статический анализатор этого не поймет и выдаст Union[int, Sequence[int]]

# Правильное использование overload:


@typing.overload
def double2(input_: int) -> int: ...


@typing.overload
def double2(input_: Sequence[int]) -> list[int]: ...


# Указание перечисления типов для параметров необязательно, без них, правда, статический анализатор не поймет типы
# параметров, ведь версии с overload не запускаются, а являются лишь stab функциями
def double2(input_: int | Sequence[int]) -> int | list[int]:
    if isinstance(input_, Sequence):
        return [i * 2 for i in input_]
    return input_ * 2


x = double2(24)
typing.reveal_type(x)  # Понимает, что тип int

x = double2((1, 4, 2, 6, 7))
typing.reveal_type(x)  # Все указано верно

# Так же можно применить это и к классам


class ProcessPNG:
    __slots__ = ('__picture',)
    __picture: TPicture

    def __init__(self, picture: TPicture) -> None:
        self._check_picture()
        self.__picture = picture

    def _check_picture(self) -> bool:
        return isinstance(self.__picture, TPicture)

    @typing.overload
    def process(self, responce: None) -> None: ...

    @typing.overload
    def process(self, responce: int) -> tuple[int, str]: ...

    def process(self, responce: typing.Optional[int]) -> typing.Optional[tuple[int, str]]:
        if responce is None:
            return None

        if isinstance(responce, int):
            return (random.randint(10, 100), random.choice(['324', '235']))

# Если же какой-нибудь метод принимает разные аргументы с разными типами, то здесь два пути:
#   1. Ограничить использования позиционных аргументов
#   2. Переписать код, чтобы использовать позиционные аргументы


class Driver:
    pass


class WebElement:
    pass


class By:
    pass


class PageObject:
    @typing.overload
    def __init__(self, *, driver: Driver) -> None: ...

    @typing.overload
    def __init__(self, *, by: tuple[By, str], driver: Driver) -> None: ...

    @typing.overload
    def __init__(self, *, context: WebElement, driver: Driver) -> None: ...

    @typing.overload
    def __init__(self, *, by: tuple[By, str], parent: "PageObject") -> None: ...

    @typing.overload
    def __init__(self, *, parent: "PageObject") -> None: ...

    def __init__(
        self,
        *,
        by: typing.Optional[tuple[By, str]] = None,
        context: typing.Optional[WebElement] = None,
        parent: typing.Optional["PageObject"] = None,
        driver: typing.Optional[Driver] = None,
    ) -> None:
        ...
