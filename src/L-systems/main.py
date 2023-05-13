import turtle
from typing import Any, Dict, List, Optional, Union

import config
import drawings as draw


class Rules:
    """Semi-dictionary, Semi-list"""

    __slots__ = ('__list', '__dict')

    __dict: Dict
    __list: List

    def __init__(self, **kwargs):
        for key in kwargs:
            if isinstance(key, (int, float)):
                raise ValueError("The keys can't be 'int' or 'float'")

        self.__dict = kwargs
        self.__list = list(kwargs)

    def __getitem__(self, item: Union[int, Any]) -> Any:
        if isinstance(item, int):
            return self.__list[item]

        return self.__dict[item]

    def __repr__(self) -> str:
        parts = []
        for idx, key in enumerate(self.__dict.keys()):
            parts.append('{' f'{key}' '}' + f'[{idx}]: {self.__dict[key]}')
        res = ', '.join(parts)

        return 'Rules([{}])'.format(res)


class LSystem:
    def __init__(self, axiom: str = 'A', rules: Optional[Union[dict, Rules]] = None, gens: int = 10):
        if isinstance(rules, (dict)):
            self.rules = Rules(**rules)
        elif isinstance(rules, Rules):
            self.rules = rules
        elif rules is None:
            self.rules = Rules(A='AB', B='A')
        else:
            raise TypeError(
                f"{self.__class__.__name__}: Take argument rules only 'dict' or 'Rules', not '{type(rules)}'"
            )

        self.axiom = axiom
        self.gens = gens

    def get_result(self):
        for gen in range(self.gens):
            self.axiom = self.apply_rules()

    def apply_rules(self):
        return ''.join([self.rules[char] if char in self.rules else char for char in self.axiom])


class App(object):
    def __init__(self, rule: Rules = Rules(**config.rules['Honeycombs'][0])):
        self.width, self.height = (config.WIDTH, config.HEIGHT)
        self.mode = 'honeycombs'
        self.__rules = rule

        self.l_system = LSystem(
            axiom=config.rules['Honeycombs'][1],
            rules=rule,
            gens=config.gens
        )

        self.screen = turtle.Screen()
        self._setting_screen()

        self.__kevin = turtle.Turtle()
        self._setting_turtle()

    def _setting_turtle(self) -> None:
        self.__kevin.pensize(2)
        self.__kevin.speed(0)
        self.__kevin.setpos(0, -self.height // 2)
        self.__kevin.color('PURPLE')

    def _setting_screen(self) -> None:
        self.screen.setup(self.width, self.height)
        self.screen.screensize(3 * self.width, 3 * self.height)
        self.screen.bgcolor('black')
        self.screen.delay(0)
        self.screen.title(f'generation: {config.gens}')

    @property
    def rules(self) -> Rules:
        return self.__rules

    @rules.setter
    def rules(self, rule: str) -> None:
        self.__rules = Rules(**config.rules[rule][0])
        self.l_system = LSystem(config.rules[rule][1], self.__rules, config.gens)
        self.mode = rule

    @property
    def turtle(self):
        return self.__kevin

    def draw(self) -> None:
        self.l_system.get_result()

        if self.mode.lower() == 'honeycombs':
            draw._honeycombs(self)
        elif self.mode.lower() == 'sierpinski triangle':
            draw._sierpinski_triangle(self)
        elif self.mode.lower() == 'dragon curve':
            draw._dragon_curve(self)
        elif self.mode.lower() == 'koch snowflake':
            draw._koch_snowflake(self)
        elif self.mode.lower() == 'tree':
            draw._tree(self)
        elif self.mode.lower() == 'realistic tree':
            draw._realtree(self)
        elif self.mode.lower() == 'gosper curve':
            draw._gosper_curve(self)
        elif self.mode.lower() == 'flower':
            draw._flower(self)
        elif self.mode.lower() == 'bush':
            draw._bush(self)

    def run(self) -> None:
        self.draw()
        self.screen.exitonclick()


if __name__ == '__main__':
    app = App()
    app.rules = 'Dragon curve'  # all rules in the config (module) in the rules (dict) + change gens
    app.run()
