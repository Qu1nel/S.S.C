#!/usr/bin/env python3.11
from typing import Union

# Union - тип объединения типов. Т.е. просто пачка типов:
# Для случаев, когда необходимо допустить использование не любых типов, а только некоторых

container: Union[int, str] = 213
container = "123"

container = 234.3  # Wrong

# Кстати, аннотация Optional[T] эквивалентна Union[T, None], хотя такая запись и не рекомендуется.


# Некторые замечания:
#
# * Union[Union[int, str], float] = Union[int, str, float]
#
# * Union[int] = int
#
# * Union[float, None] = Optional[float]
#
# * Union[int, str] = Union[str, int]
#
# * Union[int, float, int] = Union[int, float] = int | float

# В python 3.11 объединения можно писать через | -> Union[foat, complex] = float | complex
