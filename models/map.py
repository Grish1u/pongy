import settings as sts
import pygame as pg
from core.peh import Peh
import core.utils.utility_funcs as uf
from core.utils.utility_funcs import render_text_with_outline
from models.ball import Ball
from models.base_models.paddle import Paddle
from models.ai import Ai


class Map():
    def __init__(self, *args) -> None:
        pg.font.init()
        pg.mixer.init()
        self._pehs: list[Peh] = [*args, ]
        self._ball = Ball()
        if len([*args]) == 1:
            self._paddles = (
                self._pehs[0].player, Ai(self.ball))
            self._ai = True
        else:
            self._paddles = (
                self._pehs[0].player, self._pehs[1].player)
            self._ai = False
        self._outlines = (5, 5, sts.WINDOW_WIDTH - 10, sts.WINDOW_HEIGHT - 10)
        self.scorelines_y = (225, 575)
        self.scorerects = [(self.outlines[0] + (1.5 * self.outlines_width),
                            self.scorelines_y[0], self.outlines_width, self.scorelines_y[1] - self.scorelines_y[0]), (self.outlines[2] - self.outlines_width - 2, self.scorelines_y[0], self.outlines_width, self.scorelines_y[1] - self.scorelines_y[0])]

        self.fnt = pg.font.SysFont('Arial', 30, True)
        self.win_fnt = pg.font.SysFont('Arial', 40, True)
        self._sounds = (pg.mixer.Sound('resources/sounds/ball_start_cut.mp3'), pg.mixer.Sound('resources/sounds/bounce1_normal_speed_cut.mp3'), pg.mixer.Sound(
            'resources/sounds/bounce2_high_speed_cut.mp3'), pg.mixer.Sound('resources/sounds/bounce3_outlines_cut.mp3'), pg.mixer.Sound('resources/sounds/bounce4_score_cut.mp3'))
        self._WIN_SCORE = 3

    @property
    def WIN_SCORE(self):
        return self._WIN_SCORE

    @property
    def ai(self):
        return self._ai

    @property
    def paddles(self):
        return self._paddles

    @property
    def sounds(self):
        return self._sounds

    @property
    def ball(self):
        return self._ball

    @property
    def outlines(self):
        return self._outlines

    @property
    def player_count(self):
        if len(self._pehs) < 1 or len(self._pehs) > 2:
            raise ValueError
        return 1 if len(self._pehs) == 1 else 2

    # Makes sure that collision considers the width of outlines
    @property
    def outlines_width(self):
        return 5

    def check_win(self):
        won = False
        if self.paddles[0].score >= self.WIN_SCORE:
            won = True
            txt_win = 'Blue wins!'
            txt = render_text_with_outline(
                self.win_fnt, txt_win, (0, 28, 255), sts.COLOR_OUTLINES, 2)
        if self.paddles[1].score >= self.WIN_SCORE:
            won = True
            txt_win = 'Red wins!'
            txt = render_text_with_outline(
                self.win_fnt, txt_win, (204, 28, 0), sts.COLOR_OUTLINES, 2)

        if won:
            sts.WINDOW.blit(txt, (sts.WINDOW_WIDTH // 2 - txt.get_width() //
                            2, sts.WINDOW_HEIGHT // 2 - txt.get_height() // 2))
            pg.display.update()
            pg.time.delay(2250)
            # #self.ball.reset()
            # for paddle in self.paddles:
            #     paddle.reset()
        print(won)
        return True if won else False

    def run_map_process(self):
        for peh in self._pehs:
            peh.listen()
        if self.ai:
            self.paddles[1].update_movement()
        self.ball.move()
        self._hanndle_outlines__ball_collision()
        self._handle_paddle__ball_collisions()
        self._handle_outlines__paddle_collisions()
        self._handle_scoring()

    def draw(self):
        self._draw_background()
        self._draw_scores()
        self._draw_outlines()
        self._draw_objects()
        self._draw_scorelines()

    # Private methods

    # LOGIC

    def _handle_scoring(self):
        # ball towardsleft
        if self.ball.xvel < 0:
            if self.ball.y > self.scorelines_y[0] and self.ball.y < self.scorelines_y[1]:
                if self.ball.x - self.ball.radius <= self.scorerects[0][0] + self.scorerects[0][2]:
                    self.sounds[4].play()
                    self._paddles[1].score += 1
                    self.ball._xvel *= -1
                    print('Right scored')
        # ball towards right

        # only works if x is at least 1 more pixel to the left from the collision_with_outlines.
        else:
            if self.ball.y > self.scorelines_y[0] and self.ball.y < self.scorelines_y[1]:
                if self.ball.x + self.ball.radius >= self.scorerects[1][0] - 3:
                    self.sounds[4].play()
                    self._paddles[0].score += 1
                    self.ball._xvel *= -1
                    print('Left scored')

    def _handle_outlines__paddle_collisions(self):
        # up for left
        if self._paddles[0].y - self.outlines_width <= self.outlines[1] + self.outlines_width:
            self._paddles[0].can_move_up = False
        else:
            self._paddles[0].can_move_up = True
        # down for left
        if self._paddles[0].y + self._paddles[0].height + self.outlines_width >= self.outlines[3] - self.outlines_width:
            self._paddles[0].can_move_down = False
        else:
            self._paddles[0].can_move_down = True

        # up for right
        if self._paddles[1].y - self.outlines_width <= self.outlines[1] + self.outlines_width:
            self._paddles[1].can_move_up = False
        else:
            self._paddles[1].can_move_up = True
        # down for right
        if self._paddles[1].y + self._paddles[1].height + self.outlines_width >= self.outlines[3] - self.outlines_width:
            self._paddles[1].can_move_down = False
        else:
            self._paddles[1].can_move_down = True

    def _hanndle_outlines__ball_collision(self):
        # y axis
        if self.ball.y + self.ball.radius >= self.outlines[3] - self.outlines_width:
            self.sounds[3].play()
            self.ball._yvel *= -1
        elif self.ball.y - self.ball.radius <= self.outlines[1] + self.outlines_width:
            self.sounds[3].play()
            self.ball._yvel *= -1
        # x axis
        if self.ball.x + self.ball.radius >= self.outlines[2] - self.outlines_width:
            self.sounds[3].play()
            self.ball._xvel *= -1
        elif self.ball.x - self.ball.radius <= self.outlines[0] + self.outlines_width:
            self.sounds[3].play()
            self.ball._xvel *= -1

    def _handle_paddle__ball_collisions(self):
        # Left
        if self.ball.xvel < 0:
            if self.ball.y >= self._paddles[0].y and self.ball.y <= self._paddles[0].y + self._paddles[0].height:
                if self.ball.x <= self._paddles[0].x + self._paddles[0].width + self.outlines_width:
                    self.ball.xvel *= -1
                    self._calc_paddle_collision_angle(self._paddles[0])
        # Right
        else:
            if self.ball.y >= self._paddles[1].y and self.ball.y <= self._paddles[1].y + self._paddles[1].height:
                if self.ball.x >= self._paddles[1].x - self.outlines_width:
                    self.ball.xvel *= -1
                    self._calc_paddle_collision_angle(self._paddles[1])

    def _calc_paddle_collision_angle(self, paddle: Paddle):
        mid_y = paddle.y + paddle.height // 2
        diference_in_y = mid_y - self.ball.y
        reduction_factor = (paddle.height/2) // Ball.MAX_VEL
        yvel = diference_in_y / reduction_factor
        self.ball.yvel = -1 * yvel
        # Calculate the threshold for separating high and low speed
        speed_threshold = Ball.MAX_VEL / 2

        # Play different sounds based on yvel magnitude
        if abs(yvel) >= speed_threshold:
            self.sounds[2].play()
        else:
            self.sounds[1].play()

# DRAWING

    def _draw_scorelines(self):
        pg.draw.rect(pg.display.get_surface(),
                     sts.COLOR_SCORELINES, self.scorerects[0])
        pg.draw.rect(pg.display.get_surface(),
                     sts.COLOR_SCORELINES, self.scorerects[1])
        pg.draw.rect(pg.display.get_surface(),
                     sts.COLOR_OUTLINES, self.scorerects[0], 1)
        pg.draw.rect(pg.display.get_surface(),
                     sts.COLOR_OUTLINES, self.scorerects[1], 1)

    def _draw_objects(self):
        for paddle in self._paddles:
            paddle.draw()
        self.ball.draw()

    def _draw_background(self):
        # Draw Full Background Color
        pg.draw.rect(pg.display.get_surface(), sts.COLOR_BACKGROUND,
                     (0, 0, sts.WINDOW_WIDTH, sts.WINDOW_HEIGHT))
        # Draw field lines
        uf.draw_dashed_line()

    def _draw_outlines(self):
        pg.draw.rect(pg.display.get_surface(),
                     sts.COLOR_OUTLINES, self.outlines, self.outlines_width)

    def _draw_scores(self):
        # Left Score
        text1_with_outline = render_text_with_outline(
            self.fnt, f"Left: {str(self._paddles[0].score)}",
            sts.COLOR_TEXT, sts.COLOR_OUTLINES, 2)
        sts.WINDOW.blit(text1_with_outline, (sts.WINDOW_WIDTH // 4 - 150, 20))

        # Right Score
        text2_with_outline = render_text_with_outline(
            self.fnt, f"Right: {str(self._paddles[1].score)}",
            sts.COLOR_TEXT, sts.COLOR_OUTLINES, 2)
        sts.WINDOW.blit(
            text2_with_outline, (sts.WINDOW_WIDTH - sts.WINDOW_WIDTH // 4, 20))

    # def get_paddle_score(self, paddle: bool):
    #     return self.paddles[0].score if paddle else self.paddles[1].score
