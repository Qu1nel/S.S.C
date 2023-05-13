import pygame as pg  # type: ignore
from ray_casting import ray_casting
from settings import *

pg.init()


class Drawing:
    def __init__(self, sc):
        self.sc = sc
        self.font = pg.font.SysFont('Arial', 35, bold=True)

    def world(self, player_position, player_angle):
        ray_casting(self.sc, player_position, player_angle)

    def fps(self, clock):
        display_fps = str(int(clock.get_fps()))
        render = self.font.render(display_fps, False, GREEN)
        self.sc.blit(render, FPS_POS)
