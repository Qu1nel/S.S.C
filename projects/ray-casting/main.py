import sys

import pygame as pg  # type: ignore
from drawing import Drawing
from player import Player
from settings import *


class App:
    __slots__ = ('width', 'height', 'screen', 'clock', 'player', 'drawing')

    def __init__(self):
        self.width, self.height = (WIDTH, HEIGHT)
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        self.clock = pg.time.Clock()

        self.player = Player()
        self.drawing = Drawing(self.screen)

    def draw(self) -> None:
        self.screen.fill(BLACK)
        self.drawing.world(self.player.pos, self.player.angle)
        self.drawing.fps(self.clock)
        pg.display.update()

    def run(self) -> None:
        while True:
            self.player.movement()

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()

            self.draw()
            self.clock.tick(FPS)


if __name__ == '__main__':
    pg.init()
    App().run()
