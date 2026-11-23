#!/c/venv_pythons/V_ForPOOP/Scripts/python310.exe
import os
import sys
from collections import namedtuple
from functools import partial
from typing import Any, Generator, Iterable, Literal, TypeAlias

from numpy import double as float64
from numpy import single as float32

BIT_PRECISION: TypeAlias = Literal[32, 64]
ExponentBits: TypeAlias = Literal[8, 11]
MantissaBits: TypeAlias = Literal[23, 52]
OffsetBit: TypeAlias = int

try:
    BIT_PREVIEW: BIT_PRECISION = int(os.getenv('BIT_PRECISION'))
except TypeError:
    print('Создайте переменную окружения BIT_PRECISION, которая означает в каком представлении будет число [32, 64].')
    sys.exit(-1)

EXPONENT_BITS: ExponentBits = 8 if BIT_PREVIEW == 32 else 11
MANTISSA_BITS: MantissaBits = 23 if BIT_PREVIEW == 32 else 52
EXPONENT_BIAS: OffsetBit = (2 ** (EXPONENT_BITS - 1)) - 1


def get_correct_number_from_user(welcome_str: str = '$_> ') -> float32 | float64:
    if BIT_PREVIEW == 32:
        _get_number = float32
    elif BIT_PREVIEW == 64:
        _get_number = float64
    else:
        _get_number = float

    return _get_number(input(welcome_str))


def get_bits_from_float(number: float, prefer_len_bits: int = 200) -> str:
    result: list[str] = []

    while prefer_len_bits > 0:
        sub_result: float = number * 2
        whole_sub_result: int = int(sub_result)

        result.append(str(whole_sub_result))

        if sub_result - whole_sub_result == 0:
            result.extend(['0' for _ in range(prefer_len_bits - 1)])
            break

        number = sub_result - whole_sub_result
        prefer_len_bits -= 1

    return ''.join(result)


def bin_to_float32(number: str, exponent: int) -> float32:
    def reverse_enumerate(iterator: Iterable, start: int = 0) -> Generator[tuple[int, Any], None, None]:
        for element in iterator:
            yield start, element
            start -= 1

    exponent += 1

    if exponent > 0:
        whole_part = float32(int(number[:exponent], 2))
        small_part = float32()

        for idx, digit in reverse_enumerate(number[exponent:], -1):
            digit = int(digit)
            if digit:
                small_part += 2 ** idx

        return float32(whole_part + small_part)

    result = float32()
    for idx, digit in reverse_enumerate(number.rjust(abs(exponent) + len(number), '0'), -1):
        digit = int(digit)
        if digit:
            result += 2 ** idx
    return result


def main():
    printDD(f"Выбран стандарт хранения в {BIT_PREVIEW} bit")

    number = get_correct_number_from_user()
    sign = 0 if number >= 0 else 1

    print(f"Число {number:.53f}")
    number = abs(number)

    printDD(f"Целая часть: {int(number)}\nДробная часть: {number - int(number):.51f}")

    whole = int(number)
    small = number - whole

    bits_whole: str = bin(whole)[2:]
    print(f"Целая часть \"{whole}\" в двоичной СС - {bits_whole} (len {len(bits_whole)})")

    bits_small: str = get_bits_from_float(small)
    printDD(f"Дробная часть \"{small}\" в двоичной СС - {bits_small} (len - {len(bits_small)})")

    result_bin_number = bits_whole + bits_small
    printDD(f"Число {number} в двоичной СС выглядит так:\n{bits_whole}.{bits_small} - ({result_bin_number})")

    printDD('-' * 140)

    offset_bit = len(bits_whole) - 1 if whole > 0 else -result_bin_number.find('1')
    print('Порядок без смещения равен', offset_bit)
    printDD('Порядок со смещением равен', offset_bit + EXPONENT_BIAS)

    print(f"Число было {'отрицательное' if sign == 1 else 'положительное'}", end=', ')
    printDD(f'поэтому знаковый бит равен {sign}')

    printDD('-' * 140, '\n\nСобираем представление...')

    Performance = namedtuple("Performance", ('sign', 'exponent', 'mantissa'))
    print(Performance.__doc__)

    if bits_whole[1:]:
        source = Performance(
            sign=str(sign),
            exponent=bin(offset_bit + EXPONENT_BIAS)[2:].rjust(EXPONENT_BITS, '0'),
            mantissa=(bits_whole[1:] + bits_small)[:MANTISSA_BITS]
        )
    else:
        mantissa = bits_small.lstrip('0')[:MANTISSA_BITS + 1][1:]
        print(mantissa)
        source = Performance(
            sign=str(sign),
            exponent=bin(offset_bit + EXPONENT_BIAS)[2:].rjust(EXPONENT_BITS, '0'),
            mantissa=mantissa
        )

    print(source)

    bin_number = source.sign + source.exponent + source.mantissa

    if BIT_PREVIEW == 32:
        printDD("Число в памяти храниться так:")
        print(bin_number)

        print('_' * (len(bin_number) * 4 + 1), end='\n| ')
        print(' | '.join(bin_number), end=f' | - {BIT_PREVIEW} bits\n')
        printDD('‾' * (len(bin_number) * 4 + 1))
    else:
        printDD("Число в памяти записывается так\n", bin_number)

    print('Готовое число будет в такой формуле:')
    print(f'(-1)^S * 1.M * 2^(E-{EXPONENT_BIAS})/2^MB')
    printDD(f'S - sign\t\t\t\t[{source.sign}]\t\t\t\t\t\t\t- {int(source.sign, 2)}\n'
            f'M - mantissa\t\t\t[{source.mantissa}]\t- {int(source.mantissa, 2)}\n'
            f'E - exponent\t\t\t[{source.exponent}]\t\t\t\t\t- {int(source.exponent, 2)}\n'
            f'MB - mantissa bits\t\t\t\t\t\t\t\t\t- {MANTISSA_BITS}')

    printDD(f'S - sign\t\t[{source.sign}]\t\t\t\t\t\t\t- {int(source.sign, 2)}\n'
            f'M - 1+mantissa\t[1{source.mantissa}]\t- {int("1" + source.mantissa, 2)}\n'
            f'E - exponent\t[{source.exponent}] - {EXPONENT_BIAS}\t\t\t- {int(source.exponent, 2) - EXPONENT_BIAS}')

    print(f"(-1)^S == (-1)^{source.sign} = {(-1) ** int(source.sign)}")
    print(f'1.M == 1{source.mantissa} = {int("1" + source.mantissa, 2)}')
    print(f'2^(E-{EXPONENT_BIAS}) == 2^({int(source.exponent, 2)} - {EXPONENT_BIAS}) = '
          f'2^{int(source.exponent, 2) - EXPONENT_BIAS} = {2 ** (int(source.exponent, 2) - EXPONENT_BIAS)}')
    printDD(f'2^MB == 2^{MANTISSA_BITS} = {2 ** MANTISSA_BITS}')

    print(f'(-1)^{int(source.sign, 2)} * {int("1" + source.mantissa, 2)} * 2^{int(source.exponent, 2) - EXPONENT_BIAS}'
          f'/2^{MANTISSA_BITS} | =>')
    print(f'(-1)^{int(source.sign, 2)} * {int("1" + source.mantissa, 2)} * '
          f'2^{int(source.exponent, 2) - EXPONENT_BIAS - MANTISSA_BITS} | =>')
    print(f'{(-1) ** int(source.sign)} * {int("1" + source.mantissa, 2)} * '
          f'{2 ** (int(source.exponent, 2) - EXPONENT_BIAS - MANTISSA_BITS)} ==\n')

    result_number = (-1) ** int(source.sign) * int("1" + source.mantissa, 2) * 2 ** (
        int(source.exponent, 2) - EXPONENT_BIAS - MANTISSA_BITS)
    print(f'>>> {result_number:.53f} - program\n>>> {number:.53f} - user input\n'
          f'>>> {bin_to_float32("1" + source.mantissa, int(source.exponent, 2) - EXPONENT_BIAS):.53f} - my program')


if __name__ == '__main__':
    printDD = partial(print, end='\n\n')
    try:
        main()
    except Exception as exc:
        print(exc.__class__.__name__, exc)
        raise exc from None
