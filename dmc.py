import pygame
from pygame.rect import Rect


class Player:
    def __init__(self, x, y, speed=(0, 0)):
        self.x = x
        self.y = y
        self.bounds = Rect(x, y, 50, 50)
        self.speed = speed  # (dx, dy)

    def move(self, dx, dy):
        self.bounds = self.bounds.move(int(dx), int(dy))

    def update(self):
        if self.speed != (0, 0):
            self.move(*self.speed)

    def draw(self, surface):
        pygame.draw.rect(surface, (255, 0, 0), self.bounds)
