#!/bin/env python3.11

# Тип аннотации ClassVar модуля typing представляет собой конструкцию специального типа для обозначения переменных
# класса.

# Аннотация переменной, заключенной в ClassVar, указывает, что данный атрибут предназначен для использования в качестве
# переменной класса и не должен устанавливаться в экземплярах этого класса.

from dataclasses import dataclass, field
from typing import ClassVar


class Robot:
    stats: ClassVar[dict[str, int]] = {}  # атрибут класса
    damage: int = 0  # атрибут экзепляра


# Более целесобразный пример использования ClassVar
@dataclass
class StarShip:
    stats: ClassVar[dict[int, float]] = field(default={0: 0.0, 1: 0.0, 2: 0.0})
    damage: int = 0


print(f'{Robot() = !r}')
print(f'{Robot().__dict__ = !r}\n')

print(f'{StarShip() = !r}')
print(f'{StarShip().__dict__ = !r}')
