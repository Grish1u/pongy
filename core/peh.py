# Player Event Handler
from models.base_models.paddle import Paddle
from models.player import Player
import pygame as pg

# 1 player per peh


class Peh():
    # SPEED_INCREASE = False
    # CHEAT_RESET = False
  #  pause_key = [pg.K_p]

    def __init__(self, player: Player) -> None:
        self._player = player

    @property
    def player(self):
        return self._player

    def listen(self):
        keys = pg.key.get_pressed()
        if self.player.can_move_up:
            if keys[self.player.keyset[0]]:
                #print(f"Key {pg.key.name(self.player.keyset[0])} is pressed")
                self.player.move(self.player.vel*-1)

        if self.player.can_move_down:
            if keys[self.player.keyset[1]]:
                #print(f"Key {pg.key.name(self.player.keyset[1])} is pressed")
                self.player.move(self.player.vel)
        # if not (self.pause) and keys[Peh.pause_key]:
        #     self.pause = True
        # elif self.pause and keys[Peh.pause_key]:
        #     self.pause = False
        # if keys[Player.INCREASE_BALL_SPEED_CHEAT_KEY]:
        #     self.CHEATERS = True
        # else:
        #     self.CHEATERS = False

        # if keys[Player.RESET_CHEAT_KEYS_KEY]:
        #     self.CHEAT_RESET == True
