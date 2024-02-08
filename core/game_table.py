from models.map import Map
from models.base_models.paddle import Paddle
from core.peh import Peh
from models.player import Player
# AKA APP_DATA, GAME, GAME_DATA, PLAYFIELD etc.

# HERE PLAYER SHOULD BE ABLE TO PICK EITHER vs AI or vs another player


class GameTable():
    def __init__(self, choice: int) -> None:
        if choice == 1:
            self._map = Map(Peh(Player(True)))
        else:
            self._map = Map(Peh(Player(True)), Peh(Player(False)))

    @property
    def map(self):
        return self._map

    def run(self):
        self.map.run_map_process()
        self.map.draw()

    def check_win(self):
        return True if self.map.check_win() else False

    @classmethod
    def cleanup(cls):
        Player.cleanup()
