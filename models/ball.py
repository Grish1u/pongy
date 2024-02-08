import pygame as pg
import settings as sts


class Ball():

    MAX_VEL = 11

    def __init__(self) -> None:
        self._x = self.original_x = sts.WINDOW_WIDTH // 2
        self._y = self.original_y = sts.WINDOW_HEIGHT // 2
        self._radius = 12
        self._xvel = self.MAX_VEL - 2
        self._yvel = self.MAX_VEL - 3

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, value):
        self._x = value

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value):
        self._y = value

    @property
    def xvel(self):
        return self._xvel

    @xvel.setter
    def xvel(self, value: int):
        self._xvel = value

    @property
    def yvel(self):
        return self._yvel

    @yvel.setter
    def yvel(self, value: int):
        self._yvel = value

    @property
    def radius(self):
        return self._radius

    def draw(self):
        pg.draw.circle(pg.display.get_surface(), sts.COLOR_BALL,
                       (self.x, self.y), self.radius)

    def move(self):
        self._x += self.xvel
        self._y += self.yvel

    def reset(self):
        self.x = self.original_x
        self.y = self.original_y
