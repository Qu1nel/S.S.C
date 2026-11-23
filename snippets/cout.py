import sys
from typing import Protocol, Self, TextIO, runtime_checkable


@runtime_checkable
class Stringable(Protocol):
    def __str__(self):
        ...


class Stream:
    def __init__(self, file: TextIO) -> None:
        self.__file = file

    def __lshift__(self, obj: Stringable) -> Self:
        if hasattr(self.__file, "write"):
            self.__file.write(str(obj))
        else:
            raise Exception("Stream don't have 'write' method.")

        return self


cout = Stream(sys.stdout)
nl = "\n"

cout << 5 << " + " << 3654 << " = " << 5 + 3654 << nl
