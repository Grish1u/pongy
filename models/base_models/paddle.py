import settings as sts
import pygame as pg


class Paddle:

    num_paddles = 0

    def __init__(self, side) -> None:
        self._side = side
        self._width = 18
        self._height = 70
        self._x = self.original_x = self._x_assign()
        self._y = self.original_y = sts.WINDOW_HEIGHT // 2 - self.height//2
        self._vel = 8
        self._hitbox = (self.x, self.y, self.width, self.height)
        self._can_move_up = True
        self._can_move_down = True
        self._color = self._colorasign()
        self._score = 0
        Paddle.num_paddles += 1

    @property
    def mid_y(self):
        return self.y + self.height // 2

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

    @y.setter
    def y(self, value: int):
        self._y = value
        self._update_hitbox()

    @property
    def vel(self):
        return self._vel

    @property
    def width(self):
        return self._width

    @property
    def height(self):
        return self._height

    @property
    def hitbox(self):
        return self._hitbox

    @property
    def can_move_up(self):
        return self._can_move_up

    @can_move_up.setter
    def can_move_up(self, value: bool):
        self._can_move_up = value

    @property
    def can_move_down(self):
        return self._can_move_down

    @can_move_down.setter
    def can_move_down(self, value: bool):
        self._can_move_down = value
    # direction can be either positive or negative so 1 or -1

    @property
    def side(self):
        return self._side

    @property
    def color(self):
        return self._color

    @property
    def score(self):
        return self._score

    @score.setter
    def score(self, value: int):
        self._score = value

    def _colorasign(self):
        if self.side:
            return (0, 28, 255)
        else:
            return (204, 28, 0)

    def _x_assign(self):
        if self.side:
            return 45
        else:
            return 955 - self.width

    def _update_hitbox(self):
        self._hitbox = (self.x, self.y, self.width, self.height)

    def move(self, direction: int):
        self.y += direction

    def draw(self):
        pg.draw.rect(pg.display.get_surface(), self.color, self.hitbox)
        pg.draw.rect(pg.display.get_surface(),
                     sts.COLOR_OUTLINES, self.hitbox, 3)

    def _validate_side(self, value: bool):
        if value not in (True, False):
            raise ValueError('Side can either be True or False')

    def reset(self):
        self.x = self.original_x
        self.y = self.original_y
