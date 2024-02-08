import pygame as pg
import sys
from core.menu import Menu
import settings as sts


class GameWindow():

    def __init__(self) -> None:
        pg.init()
        self._win = sts.WINDOW
        self._clock = pg.time.Clock()
        pg.display.set_caption(f'Pongy')
        self.menu = None  # remove this and add menu

    @ property
    def win(self):
        return self._win

    @ property
    def clock(self):
        return self._clock

    def run(self):
        self.menu = Menu()
        run = True
        while run == True:
            # print(
            #     f'gametable is {self.menu.game_table} ')
            # print(
            #     f'game_paused: {self.menu.game_paused}, menu_state: {self.menu.current_menu_state}')
            # START MENU
            self._check_window_events()
            if self.menu.game_paused:
                # or self.menu.check_win():
                if self.menu.current_menu_state == Menu.MENU_STATES[0]:
                    #print('startmenu is now')
                    pg.display.set_caption(
                        f'Pongy - Main Menu - {self.clock.get_fps() :.1f} FPS')
                    if self.menu.display_and_run_startmenu():
                        run = False
                elif self.menu.current_menu_state == Menu.MENU_STATES[1]:
                    #print('pause menu is now')
                    pg.display.set_caption(
                        f'Pongy - Game Paused - {self.clock.get_fps() :.1f} FPS')
                    self.menu.display_and_run_pausedmenu()
            else:
                #print('match is running now is now')
                pg.display.set_caption(
                    f'Pongy - {self.clock.get_fps() :.1f} FPS')
                self.clock.tick(sts.FPS)
                print(self.menu.check_win())
                self.menu.run_match()

            pg.display.update()
        pg.quit()
        sys.exit()

    def _check_window_events(self):
        for event in pg.event.get():
            # print(event)
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    self.menu.switch_paused_state()
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
