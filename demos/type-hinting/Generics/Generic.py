#!/usr/bin/env python3.11
from collections.abc import Iterable
from typing import Any, Generic, TypeVar, TypeVarTuple
from uuid import UUID


class RawRecord:
    id: int
    value: Any

    def __init__(self, id: int, value: Any) -> None:
        id = id
        value = value


TValue = TypeVar("TValue")
TId = TypeVar("TId", int, UUID)


class Record(Generic[TValue, TId]):
    id: TId
    value: TValue

    def __init__(self, id: TId, value: TValue) -> None:
        self.id = id
        self.value = value


raw_record = RawRecord(1, "some string!")
# raw_record.value.lower()  # Type hint не работает(

record = Record(2, "another string")
record.value.count("3")  # Type hint работат!

record2 = Record(3, 100j)
record2.value.real  # Type hint работает!

TTupleValue = TypeVarTuple("TTupleValue")


class MulRecord(Generic[*TTupleValue]):
    values: tuple[*TTupleValue]

    def __init__(self, *values: *TTupleValue) -> None:
        self.values = values


mul_record = MulRecord("a", "b", "c")
mul_record.values[0].lower()  # Type hint работает!


TValues = TypeVarTuple("TValues")


class AnotherRecord(Generic[*TValues]):
    values: tuple[*TValues]

    def __init__(self, *values: *TValues) -> None:
        values = values

    def update(self, *values: *TValues) -> None:
        self.values = values


another_record = AnotherRecord("123", 123)
# Type hint работает (показывает какие типы нужно обновить)
another_record.update("some", 0)
# Type hint работает (показывает какие типы нужно обновить)
another_record.update(123, 124j)

T = TypeVar('T')


class LoggedVar(Generic[T]):
    def __init__(self, value: T, name: str) -> None:
        self.name = name
        self.value = value

    def set(self, new: T) -> None:
        self.value = new

    def get(self) -> T:
        return self.value


def zero_all_vars(vars: Iterable[LoggedVar[int]]) -> None:
    for var in vars:
        var.set(0)


zero_all_vars([LoggedVar(12, "some"), LoggedVar("123", "123")])
