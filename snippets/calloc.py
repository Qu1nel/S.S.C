from array import array
from collections import namedtuple
from enum import Enum, IntEnum, StrEnum, unique
from typing import TypeAlias


def printf(_format: str, *args) -> None:
    print(_format % args, end="")


@unique
class SizeofLable(StrEnum):
    SIGNED_CHAR = "b"
    UNSIGNED_CHAR = "B"
    INT16_T = "h"
    UINT16_T = "H"
    INT32_T = "i"
    UINT32_T = "I"
    INT64_T = "l"
    UINT64_T = "L"
    FLOAT = "f"
    DOUBLE = "d"


class SizeofNumber(IntEnum):
    SIGNED_CHAR = 1
    UNSIGNED_CHAR = 1
    INT16_T = 2
    UINT16_T = 2
    INT32_T = 2
    UINT32_T = 2
    INT64_T = 4
    UINT64_T = 4
    FLOAT = 4
    DOUBLE = 8


Size = namedtuple("Size", ("name", "size"))


class Sizeof(Enum):
    int8_t = Size(name=SizeofLable.UNSIGNED_CHAR.value, size=SizeofNumber.UNSIGNED_CHAR.value)
    int16_t = Size(name=SizeofLable.UINT16_T.value, size=SizeofNumber.UINT16_T.value)
    int32_t = Size(name=SizeofLable.UINT32_T.value, size=SizeofNumber.UINT32_T.value)
    int64_t = Size(name=SizeofLable.UINT64_T.value, size=SizeofNumber.UINT64_T.value)


Address: TypeAlias = int
Length: TypeAlias = int


def calloc(size: Sizeof, count: int) -> array:
    _size = size.value.name
    result = array(_size, [0 for _ in range(count)])
    return result


def to_bin_string(area: array) -> str:
    result = "-".join(f"{byte:08b}" for byte in area.tobytes())

    for byte in area.tobytes():
        print(f"nibble - {byte:08b}")

    return result


mem = calloc(Sizeof.int32_t, 4)
printf("%s\n", mem)
printf("%s\n", mem.buffer_info())
printf("total sizeof mem - %ld\n", mem.buffer_info()[1] * mem.itemsize)
printf("%s\n", mem.tobytes())
mem[0] = 0xA
mem[1] = 0xF3A597FA
printf("%s\n", mem.tobytes())

printf("bytes in bin = %s\n", to_bin_string(mem))
