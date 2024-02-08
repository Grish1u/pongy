from models.base_models.paddle import Paddle
from models.ball import Ball


class Ai(Paddle):
    def __init__(self, ball: Ball) -> None:
        super().__init__(side=False)
        self._ball = ball

    @property
    def ball(self):
        return self._ball

    def update_movement(self):
        # UP
        if self.can_move_up and self.ball.y < self.mid_y:
            self.move(self.vel*-1)
        if self.can_move_down and self.ball.y > self.mid_y:
            self.move(self.vel)
