#!/usr/bin/env python3.11
from copy import deepcopy
from typing import Any, Sequence, TypeVar

T = TypeVar("T")

'''
Фабрика TypeVar предназначен для записывания некоторых экземпляров для использования типов
только во время присваивания конкретного типа, когда это необходимо, предоставляемых в 
качестве параметров функций и т.п.

Поскольку информация о типах объектов, хранящихся в контейнерах, не может быть статически 
выведены общим способом, абстрактные базовые классы были расширен для поддержки подписки для 
обозначения ожидаемых типов для контейнера элементы.
'''


def raw_first_element(source: Sequence[Any]) -> Any:
    return source[0]


def first_element(source: Sequence[T]) -> T:
    """
    В этом случае контракт заключается в том, что возвращаемое значение соответствует элементы,
    содержащиеся в коллекции.
    """
    return source[0]


def copyof(obj: T) -> T:
    return deepcopy(obj)


'''
Кроме того, TypeVar может несколько типов. Которые подставяться* во время линтинга.
'''

AnyStr = TypeVar("AnyStr", str, bytes)


class MyStr(str):
    pass


def concat(a: AnyStr, b: AnyStr) -> AnyStr:
    return a + b


def main() -> None:
    letters = ['a', 'b', 'c', 'd']
    letter = first_element(letters)
    bad_letter = raw_first_element(letters)

    # Type hint работает для строк
    print(f"Type hint работает и мы получили это - '{letter.lower()}'")

    try:
        print(bad_letter.bit_count())  # Type hint не работает
    except AttributeError:
        print("Type hint не сработа и мы получили вот эту каку! AttributeError")

    number = 234
    copy_number = copyof(number)  # Type hint - int
    compl = 34j
    copy_compl = copyof(compl)  # Type hint - complex
    print(f'{copy_number = } {type(copy_number) = }')
    print(f'{copy_compl = } {type(copy_compl) = }')

    my_str = MyStr("some")
    another_str = ' string'

    result = concat(my_str, another_str)  # Type hint - str
    result_bytes = concat(b'a', b' is byte')  # Type hint - bytes

    print(f'{result = } {type(result) = }',
          f'{result_bytes = } {type(result_bytes) = }', sep='\n')


if __name__ == "__main__":
    main()
