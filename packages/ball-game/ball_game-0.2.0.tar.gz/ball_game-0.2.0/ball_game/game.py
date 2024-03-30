from random import randrange

from pygame.font import Font, match_font
from pygame import init, display, Color, time, event, \
    K_SPACE, K_ESCAPE, K_DOWN, K_UP, K_RIGHT, K_LEFT, QUIT, KEYDOWN, MOUSEBUTTONDOWN

from ball_game.assets import Score, MenuButton, Ball


class Game:
    def __init__(self,
                 height: int = 800,
                 width: int = 800,
                 clock_tick: int = 50):

        init()
        display.set_caption('ROLL THE BALL')

        self.GAME_DURATION = 60
        self.MAX_BALL_COUNT = 5

        self.QUIT_TEXT = 'QUIT'
        self.RESTART_TEXT = 'RESTART'

        self.GAME_FONT = match_font('monospace')
        self.FONT_LARGE = Font(self.GAME_FONT, 32)
        self.FONT_MEDIUM = Font(self.GAME_FONT, 18)
        self.FONT_SMALL = Font(self.GAME_FONT, 14)

        self.BLACK = Color('black')
        self.WHITE = Color('white')
        self.BLUE = Color('blue')
        self.GREEN = Color('green')
        self.RED = Color('red')

        self.game_is_over = False
        self.game_is_paused = False
        self.height = height
        self.width = width
        self.screen = display.set_mode((self.width, self.height))
        self.event = None
        self.start_ticks = 0
        self.played_seconds = 0
        self.pause_time = 0
        self.pause_start_ticks = 0
        self.total_pause_time = 0
        self.clock = time.Clock()
        self.clock_tick = clock_tick
        self.balls = []
        self.game_score = Score()
        self.menu_buttons = (MenuButton(self.WHITE, self.RESTART_TEXT,
                                        self.width / 3, self.height / 3, 200, 32, self.__restart_game),
                             MenuButton(self.WHITE, self.QUIT_TEXT, self.width / 3,
                                        self.height / 2, 200, 32, exit))

    def __process_mouse(self):
        if self.event.button == 1 and (self.game_is_over or self.game_is_paused):
            for button in self.menu_buttons:
                if button.rectangle.collidepoint(self.event.pos):
                    button.action()

    def __process_keys(self):

        if self.event.key == K_LEFT:
            for b in self.balls:
                b.move_x(-10)
        elif self.event.key == K_RIGHT:
            for b in self.balls:
                b.move_x(10)
        elif self.event.key == K_UP:
            for b in self.balls:
                b.move_y(-10)
        elif self.event.key == K_DOWN:
            for b in self.balls:
                b.move_y(10)
        elif self.event.key == K_ESCAPE:
            if self.game_is_over:
                exit()
            else:
                self.game_is_paused = not self.game_is_paused
                if self.game_is_paused:
                    self.pause_start_ticks = time.get_ticks()
                else:
                    self.total_pause_time += self.pause_time

        elif self.event.key == K_SPACE:
            for b in self.balls:
                b.velocity.update(0, 0)
        else:
            pass

    def __add_balls(self):
        if len(self.balls) > 0:
            self.balls.clear()
        for i in range(self.MAX_BALL_COUNT):
            self.balls.append(Ball(x=(randrange(self.width - self.MAX_BALL_COUNT) + i),
                                   y=(randrange(self.height - self.MAX_BALL_COUNT) + i),
                                   vx=(50 * (i + 1)), vy=(50 * (i + 1)),
                                   color=Color((randrange(250 + i),
                                                randrange(250 + i),
                                                randrange(250 + i),
                                                randrange(250 + i)))))

    def __draw_balls(self):
        self.screen.fill(self.BLACK)
        for ball in self.balls:
            dt = self.clock.tick(self.clock_tick) / 1000
            ball.check_borders(self.width, self.height)
            ball.ball_hit(self.balls, self.screen, self.FONT_MEDIUM, self.game_score, dt)
            ball.ball_move(dt)
            ball.draw_ball(self.screen)

        score_surface = self.FONT_SMALL.render(f'Score: {self.game_score.score}', True, self.WHITE)
        self.screen.blit(score_surface, dest=(0, 0))
        timer_surface = self.FONT_SMALL.render(f'Timer: {self.played_seconds}', True, self.WHITE)
        self.screen.blit(timer_surface, dest=(self.width - 100, 0))

    def __game_over(self):
        resolve_text = self.FONT_LARGE.render(f'GAME OVER! YOUR SCORE IS {self.game_score.score}',
                                              False, self.WHITE)
        self.screen.blit(resolve_text, dest=(self.width / 5, self.height / 4))
        for button in self.menu_buttons:
            button.draw_button(self.screen, self.FONT_MEDIUM, self.RED)

    def __restart_game(self):
        self.start_ticks = time.get_ticks()
        self.__add_balls()
        self.game_score = Score()
        self.game_is_over = False
        self.game_is_paused = False
        self.pause_time = 0
        self.total_pause_time = 0
        self.played_seconds = 0

    def __pause_game(self):
        self.pause_time = (time.get_ticks() - self.pause_start_ticks) // 1000

        resolve_text = self.FONT_LARGE.render(f'PAUSE. YOUR SCORE IS {self.game_score.score}',
                                              False, self.WHITE)
        self.screen.blit(resolve_text, dest=(self.width / 5, self.height / 4))
        for button in self.menu_buttons:
            button.draw_button(self.screen, self.FONT_MEDIUM, self.RED)

    def play(self):
        try:
            events = {
                QUIT: exit,
                KEYDOWN: self.__process_keys,
                MOUSEBUTTONDOWN: self.__process_mouse
            }

            self.start_ticks = time.get_ticks()
            self.__add_balls()

            while True:
                for evt in event.get():
                    if evt.type in events.keys():
                        self.event = evt
                        events[evt.type]()

                if self.game_is_over:
                    self.__game_over()
                elif self.game_is_paused:
                    self.__pause_game()
                else:
                    self.game_is_over = (self.played_seconds >= self.GAME_DURATION)
                    self.played_seconds = (time.get_ticks() - self.start_ticks) // 1000 - self.total_pause_time
                    self.__draw_balls()
                display.update()
        except KeyboardInterrupt:
            exit()
