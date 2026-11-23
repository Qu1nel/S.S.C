import contextlib
import os
import random
import time
from collections import namedtuple
from dataclasses import dataclass
from typing import Literal, TypeAlias, cast

import colorama as c  # type: ignore

c.init()

MineCoord = namedtuple("MineCoord", ["x", "y"])
FlagCoord = namedtuple("FlagCoord", ["x", "y"])
MineCoordVector: TypeAlias = list[MineCoord]
FlagCoordVector: TypeAlias = list[FlagCoord]


@dataclass(slots=True)
class Cell:
    value: int = 0
    visible: bool = False
    with_flag: bool = False
    with_q: bool = False
    repr: str = ""  # noqa


CellVector: TypeAlias = list[Cell]
CellMatrix: TypeAlias = list[CellVector]

LOGO = """
\t ██████╗ █████╗ ███████╗███████╗██████╗
\t██╔════╝██╔══██╗██╔══██║██╔════╝██╔══██╗   Поле:  10x10
\t██║     ███████║██║  ██║█████╗  ██████╔╝   Мин:    10
\t██║     ██╔══██║██║  ██║██═══╝  ██╔═══╝    Флагов: {count_flags}
\t╚██████╗██║  ██║██║  ██║███████╗██║
\t ╚═════╝╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝╚═╝
"""


def get_color(count: int) -> str:
    match count:
        case 1:
            result_color = c.Fore.BLUE
        case 2:
            result_color = c.Fore.GREEN
        case _:
            result_color = c.Fore.RED
    return cast(str, result_color)


def print_cell(cell: Cell) -> None:
    printable_cell = f"[{c.Fore.RED} {c.Fore.RESET}]" if not cell.visible else cell.repr
    print(f"{printable_cell:^15}", end="")


def print_game_grid(field: CellMatrix, flags: int) -> None:
    os.system("clear || cls")  # noqa
    print(LOGO.format(count_flags=flags))

    print(f"\n.{'_' * 60}.", f"|{' ' * 60}|\n" * 2, end="|\t", sep="\n")

    for i in range(len(field)):
        print(f"{i + 1:^5}", end="")
    print("   |", end="\t\t")
    print("[Инструкция]", f"|{' ' * 60}|", sep="\n")

    for idx, row in enumerate(field, 1):
        print(f"|{idx:3}", end="\t")
        for col in range(len(field)):
            print_cell(cell=row[col])

        if idx == 1:
            print("   |\t   Baлидныe ввод хода:")
        elif idx == 3:  # noqa
            print("   |\t\tX Y <Action>")
        elif idx == 4:  # noqa
            print("   |\t\tX,Y,<Action>")
        elif idx == 5:  # noqa
            print("   |\t\tX Y,<Action>")
        elif idx == 6:  # noqa
            print("   |\t\tX,Y <Action>")
        elif idx == 8:  # noqa
            print(
                f"   |\t   Где {c.Fore.GREEN}X{c.Fore.RESET} и {c.Fore.GREEN}Y{c.Fore.RESET} - "
                f"координаты точки [{c.Fore.BLUE}1{c.Fore.RESET};{c.Fore.BLUE}10{c.Fore.RESET}]",
            )
        elif idx == 9:  # noqa
            print(
                f"   |\t   {c.Fore.YELLOW}<Actioin>{c.Fore.RESET} одно из действий "
                f"[{c.Fore.RED}Open{c.Fore.RESET} (o, O), {c.Fore.RED}Flag{c.Fore.RESET} (f, F), "
                f"{c.Fore.RED}?{c.Fore.RESET} (предположение)]",
            )
        else:
            print("   |")

    print(f"|{' ' * 60}|\t   Чтобы выйти: {c.Fore.RED}CTRL+C{c.Fore.RESET}")
    print(f"|{'_' * 60}|")


class Game:
    mines_cords: MineCoordVector
    flags_cords: FlagCoordVector
    field: CellMatrix

    def __init__(self, size: int, mines: int) -> None:
        self.mines = mines
        self.size = size

        self.mines_cords = self.__generate_mines_pos()
        self.field = self.__generate_field()

        self.flags_cords = []
        self.first_move = True

        self.count_flags = mines

        self.is_lose = False
        self.is_win = False

    def __generate_mines_pos(self) -> MineCoordVector:
        mines_pos = []
        for _ in range(self.mines):
            mine_cords = MineCoord(x=random.randint(0, self.size - 1), y=random.randint(0, self.size - 1))
            while mine_cords in mines_pos:
                mine_cords = MineCoord(x=random.randint(0, self.size - 1), y=random.randint(0, self.size - 1))

            mines_pos.append(mine_cords)

        return mines_pos

    def __count_mines(self, row: int, col: int) -> int:
        if (row, col) in [(mine.x, mine.y) for mine in self.mines_cords]:
            return -1

        neighbours = [
            (row - 1, col - 1),
            (row - 1, col),
            (row - 1, col + 1),
            (row, col - 1),
            (row, col + 1),
            (row + 1, col - 1),
            (row + 1, col),
            (row + 1, col + 1),
        ]

        counter = sum(el in neighbours for el in [(mine.x, mine.y) for mine in self.mines_cords])
        return counter

    def __generate_field(self) -> CellMatrix:
        field: CellMatrix = [[Cell() for _ in range(self.size)] for _ in range(self.size)]

        for row in range(self.size):
            for col in range(self.size):
                count_mines = self.__count_mines(row, col)
                if count_mines == -1:
                    representation = f"[{c.Fore.RED}*{c.Fore.RESET}]"
                elif count_mines == 0:
                    representation = f" {c.Fore.BLUE} {c.Fore.RESET} "
                else:
                    representation = f" {get_color(count_mines)}{count_mines}{c.Fore.RESET} "

                field[row][col] = Cell(
                    value=count_mines,
                    visible=False,
                    with_flag=False,
                    repr=representation,
                )

        return field

    def __lose_game(self) -> None:
        for row in range(self.size):
            for col in range(self.size):
                if self.field[row][col].with_flag and self.field[row][col].value != -1:
                    self.field[row][col].repr = f"[{c.Fore.RED}*{c.Fore.RESET}]"

                self.field[row][col].visible = True
        self.is_lose = True
        print_game_grid(field=self.field, flags=self.count_flags)

    def __win_game(self, field: CellMatrix) -> None:
        for row in field:
            for cell in row:
                cell.visible = True
        self.is_win = True
        print_game_grid(field=field, flags=self.count_flags)

    def __player_turn(self, input_x: int, input_y: int, action: Literal["Open", "Flag", "?"]) -> None:
        if action == "Flag":
            if (
                not self.field[input_x][input_y].with_flag
                and self.count_flags > 0
                and not self.field[input_x][input_y].visible
            ):
                self.field[input_x][input_y].repr = f"[{c.Fore.YELLOW}F{c.Fore.RESET}]"
                self.field[input_x][input_y].visible = True
                self.field[input_x][input_y].with_flag = True
                self.count_flags -= 1
                self.flags_cords.append(FlagCoord(x=input_x, y=input_y))

            elif self.field[input_x][input_y].with_flag:
                self.field[input_x][input_y].repr = self.field[input_x][input_y].repr
                self.field[input_x][input_y].visible = False
                self.field[input_x][input_y].with_flag = False
                self.count_flags += 1
                self.flags_cords.remove(FlagCoord(x=input_x, y=input_y))

        elif action == "?":
            if not self.field[input_x][input_y].with_q and not self.field[input_x][input_y].visible:
                self.field[input_x][input_y].repr = f"[{c.Fore.YELLOW}?{c.Fore.RESET}]"
                self.field[input_x][input_y].visible = True
                self.field[input_x][input_y].with_q = True

            elif self.field[input_x][input_y].with_q:
                self.field[input_x][input_y].repr = self.field[input_x][input_y].repr
                self.field[input_x][input_y].visible = False
                self.field[input_x][input_y].with_q = False

        elif action == "Open" and not self.field[input_x][input_y].visible:
            if self.field[input_x][input_y].value == -1:
                if self.first_move is not True:
                    self.__lose_game()
                else:
                    self.first_move = False  # TODO: Bug
                    self.field = self.__generate_field()
                    self.__player_turn(input_x, input_y, action)
            elif self.field[input_x][input_y].value > 0:
                if not self.field[input_x][input_y].with_flag:
                    self.field[input_x][input_y].visible = True
            elif self.field[input_x][input_y].value == 0:
                vis_cells: list = []
                self.__open_neighbours(input_x, input_y, vis_cells)

        if self.__compare(self.flags_cords, self.mines_cords):
            self.__win_game(self.field)

    def __compare(self, flags: FlagCoordVector, mines: MineCoordVector) -> bool:
        if len(flags) == len(mines):
            counter1 = 0
            counter2 = 0
            for flag in flags:
                if flag in mines:
                    counter1 += 1
                else:
                    return False

            for mine in mines:
                if mine in flags:
                    counter2 += 1
                else:
                    return False

            if counter1 == counter2 and counter1 == len(flags):
                return True
        return False

    def __open_neighbours(self, row: int, col: int, visited_cells: list) -> None:
        if [row, col] not in visited_cells:
            visited_cells.append([row, col])
            if self.field[row][col].value == 0:
                self.field[row][col].repr = f" {c.Fore.BLUE} {c.Fore.RESET} "
                if self.field[row][col].with_flag:
                    self.count_flags += 1
                    self.field[row][col].with_flag = False
                self.field[row][col].visible = True

                if row > 0:
                    self.__open_neighbours(row - 1, col, visited_cells)
                if row < self.size - 1:
                    self.__open_neighbours(row + 1, col, visited_cells)
                if col > 0:
                    self.__open_neighbours(row, col - 1, visited_cells)
                if col < self.size - 1:
                    self.__open_neighbours(row, col + 1, visited_cells)
                if row > 0 and col > 0:
                    self.__open_neighbours(row - 1, col - 1, visited_cells)
                if row > 0 and col < self.size - 1:
                    self.__open_neighbours(row - 1, col + 1, visited_cells)
                if row < self.size - 1 and col > 0:
                    self.__open_neighbours(row + 1, col - 1, visited_cells)
                if row < self.size - 1 and col < self.size - 1:
                    self.__open_neighbours(row + 1, col + 1, visited_cells)

            if self.field[row][col].value != 0:
                if self.field[row][col].with_flag:
                    self.count_flags += 1
                self.field[row][col].visible = True

    def __get_input(self) -> tuple[int, int, Literal["Flag", "Open", "?"]]:
        while True:
            try:
                x, y, mode = input("\n  [Ваш ход]: ").strip().replace("\t", " ").replace(",", " ").split()
            except ValueError:
                print(
                    c.Fore.RED,
                    "\n  [Ошибка ввода]: вы не корректно ввели данные.",
                    c.Fore.RESET,
                )
                time.sleep(3)
                print_game_grid(self.field, flags=self.count_flags)
                continue
            try:
                x, y = int(x), int(y)  # type: ignore
            except ValueError:
                print(
                    c.Fore.RED,
                    "\n  [Ошибка ввода]: вы ввели координаты не корректного типа.",
                    c.Fore.RESET,
                )
                time.sleep(3)
                print_game_grid(self.field, flags=self.count_flags)
                continue
            try:
                assert 1 <= int(x) <= 10  # noqa
                assert 1 <= int(y) <= 10  # noqa
                assert mode.lower() in ("open", "o", "flag", "f", "?")
            except AssertionError:
                print(
                    c.Fore.RED,
                    "\n  [Ошибка ввода]: введённые данные не допустимы по значению.",
                    c.Fore.RESET,
                )
                time.sleep(3)
                print_game_grid(self.field, flags=self.count_flags)
                continue
            mode = "Open" if mode.lower() in ("open", "o") else "Flag" if mode.lower() in ("flag", "f") else "?"
            return cast(int, y), cast(int, x), cast(Literal["Open", "Flag", "?"], mode)

    def run(self) -> None:
        while not self.is_lose and not self.is_win:
            print_game_grid(field=self.field, flags=self.count_flags)
            x, y, move = self.__get_input()
            self.__player_turn(int(x) - 1, int(y) - 1, move)

        if self.is_win:
            print(c.Fore.GREEN, "\n  You WIN!", c.Fore.RESET)
        else:
            print(c.Fore.RED, "\n  Game OVER!", c.Fore.RESET)


def main() -> None:
    game = Game(size=10, mines=10)
    with contextlib.suppress(KeyboardInterrupt):
        game.run()


if __name__ == "__main__":
    main()
