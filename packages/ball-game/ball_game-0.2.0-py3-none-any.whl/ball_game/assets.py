from typing import Union

from pygame import Color, draw, Rect
from pygame.font import Font
from pygame.math import Vector2
from pygame.surface import SurfaceType, Surface


class Score:
    def __init__(self):
        self.score = 0

    def add(self):
        self.score += 1

    def __str__(self):
        return f'Current score is {self.score}'


class Ball:
    COUNT = 0

    def __init__(self, x: int = 10, y: int = 10,
                 vx: int = 0, vy: int = 0, size: int = 3, color: Color = Color('white')):
        Ball.COUNT += 1
        self.id = self.COUNT
        self.position = Vector2(x, y)
        self.velocity = Vector2(vx, vy)
        self.color = color

        if size < 0:
            self.size = -size
        elif size == 0:
            self.size = 1
        else:
            self.size = size

    def ball_move(self, dt: int):
        self.position += self.velocity * dt

    def move_x(self, to_add: int):
        self.velocity.x += to_add

    def move_y(self, to_add: int):
        self.velocity.y += to_add

    def check_borders(self, width: int, height: int):

        if self.position.x + self.size >= width or self.position.x <= self.size:
            self.velocity.x *= -1

        if self.position.x >= width - self.size:
            self.position.x = width - self.size
        if self.position.x <= self.size:
            self.position.x = self.size

        if self.position.y + self.size >= height or self.position.y <= self.size:
            self.velocity.y *= -1

        if self.position.y >= height - self.size:
            self.position.y = height - self.size
        if self.position.y <= self.size:
            self.position.y = self.size

    def ball_hit(self, other_balls: list, screen: Union[Surface, SurfaceType], font: Font,
                 score: Score, dt: float = 50, font_color: Color = Color('white')):
        for b in other_balls:
            if self is not b and self.position.distance_to(b.position) <= self.size + b.size:
                self.velocity.reflect_ip(b.position)
                b.velocity.reflect_ip(self.position)
                b.ball_move(dt)
                text_surface = font.render('HIT', True, font_color)
                screen.blit(text_surface, dest=self.position)
                score.add()

    def draw_ball(self, screen: Union[Surface, SurfaceType]):
        draw.circle(screen, self.color, self.position, self.size)

    def __str__(self) -> str:
        return f'ID {self.id}: {self.position}; Velocity {self.velocity}'


class MenuButton:
    def __init__(self, color: Color,
                 text: str, x_pos: float,
                 y_pos: float, length: int,
                 height: int, action: callable):
        self.color = color
        self.text = text
        self.rectangle = Rect(x_pos, y_pos, length, height)
        self.action = action

    def draw_button(self, screen: Union[Surface, SurfaceType], font: Font, font_color: Color):
        txt_surface = font.render(self.text, True, font_color)
        draw.rect(screen, self.color, self.rectangle, 1)
        screen.blit(txt_surface, (self.rectangle.x + self.rectangle.x / 4, self.rectangle.y + 5))
