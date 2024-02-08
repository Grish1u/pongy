from models.base_models.paddle import Paddle
import pygame as pg


class Player(Paddle):
    # lookig to add a class variable that can be changed with a class method // something like the barcode examples from telerik. That way
    # i can ensure there are min 1 but max 2 players and determine everything else based on that.

    ALLOWED_KEYS = [pg.K_w, pg.K_s, pg.K_UP, pg.K_DOWN]
    # INCREASE_BALL_SPEED_CHEAT_KEY = [pg.K_i]
    # RESET_CHEAT_KEYS_KEY = [pg.K_r]
    MAX_PLAYERS = 2

    num_players = 0

    def __init__(self, side) -> None:
        self._validation_num_players()
        super().__init__(side)
        self._set_keyset()
        Player.num_players += 1
        print('player created')

    @property
    def keyset(self):
        return self._keyset

    def _set_keyset(self):
        if self.side:
            self._keyset = self.ALLOWED_KEYS[:2]
        else:
            self._keyset = self.ALLOWED_KEYS[2:]

    def _validation_num_players(self):
        print(f'Player instances is: {Player.num_players}')
        # if Player.num_players >= Player.MAX_PLAYERS:
        #     raise ValueError("Maximum number of players reached")

    def printkeyset(self):
        print(self.keyset)

    @classmethod
    def cleanup(cls):
        cls.num_players = 0
