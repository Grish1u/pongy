from core.game_table import GameTable
from button import Button
import pygame as pg
import settings as sts
import time as tm
from core.utils.utility_funcs import render_text_with_outline


class Menu:
    MENU_STATES = ('start_menu', 'paused_menu')

    def __init__(self) -> None:
        self._game_paused = True
        self._current_menu_state = Menu.MENU_STATES[0]
        self._resume_img = pg.image.load(
            "resources/buttons/resume.png").convert_alpha()
        self._quit_img = pg.image.load(
            "resources/buttons/quit.png").convert_alpha()
        self._singleplayer_image = pg.image.load(
            "resources/buttons/single_player.png").convert_alpha()
        self._multiplayer_image = pg.image.load(
            "resources/buttons/multi_player.png").convert_alpha()
        self._gametable = None

    @ property
    def game_table(self):
        return self._gametable

    @ game_table.setter
    def game_table(self, value: GameTable):
        self._gametable = value

    @ property
    def game_paused(self):
        return self._game_paused

    @ game_paused.setter
    def game_paused(self, value: bool):
        self._game_paused = value

    @ property
    def current_menu_state(self):
        return self._current_menu_state

    @current_menu_state.setter
    def current_menu_state(self, value: str):
        if value in Menu.MENU_STATES:
            self._current_menu_state = value
        else:
            raise ValueError

    def display_and_run_startmenu(self):
        self.current_menu_state = Menu.MENU_STATES[0]
        singleplayer_button = Button(
            sts.WINDOW_WIDTH // 2 - 105, 125, self._singleplayer_image, 1)
        multiplayer_button = Button(
            sts.WINDOW_WIDTH // 2 - 105, 375, self._multiplayer_image, 1)
        exit_button = Button(sts.WINDOW_WIDTH // 2 -
                             105, 625, self._quit_img, 1)
        sts.WINDOW.fill(sts.COLOR_BACKGROUND)
        self.display_info()
        if singleplayer_button.draw(sts.WINDOW):
            self.current_menu_state = Menu.MENU_STATES[1]
            self.game_table = GameTable(1)
            self.game_paused = False
        if multiplayer_button.draw(sts.WINDOW):
            self.current_menu_state = Menu.MENU_STATES[1]
            self.game_table = GameTable(2)
            self.game_paused = False
            print('you picked multiplayer')
        if exit_button.draw(sts.WINDOW):
            return True

    def display_and_run_pausedmenu(self):
        #self.game_paused = True
        resume_button = Button(sts.WINDOW_WIDTH // 2 -
                               105, 125, self._resume_img, 1)
        quit_button = Button(sts.WINDOW_WIDTH // 2 -
                             105, 375, self._quit_img, 1)
        sts.WINDOW.fill(sts.COLOR_BACKGROUND)
        if resume_button.draw(sts.WINDOW):
            self.game_paused = False
            tm.sleep(0.3)
        if quit_button.draw(sts.WINDOW):
            self.current_menu_state = Menu.MENU_STATES[0]
            GameTable.cleanup()
            self.game_table = None
            self.game_paused = True
            tm.sleep(0.3)

    def display_info(self):
        fnt = pg.font.SysFont('Arial', 20, True)
        how_to_play = render_text_with_outline(
            fnt, 'First player to score 3 wins', sts.COLOR_TEXT, sts.COLOR_OUTLINES, 2)
        press_space_to_pause = render_text_with_outline(
            fnt, 'Press space to Pause', sts.COLOR_TEXT, sts.COLOR_OUTLINES, 2)
        sts.WINDOW.blit(how_to_play, (sts.WINDOW_WIDTH //
                        4 - 180, sts.WINDOW_HEIGHT // 2 - 20))
        sts.WINDOW.blit(press_space_to_pause,
                        (sts.WINDOW_WIDTH // 4 - 180, sts.WINDOW_HEIGHT // 2 + 40))

    def run_match(self):
        if self.game_table != None:
            self.game_table.run()

    def switch_paused_state(self):
        if self.game_paused:
            self.game_paused = False
        else:
            self.game_paused = True

    def check_win(self):
        if self.game_table != None:
            if self.game_table.check_win():
                self.game_table = None
                self.game_paused = True
                self.current_menu_state = Menu.MENU_STATES[0]
                return True
            else:
                return False
