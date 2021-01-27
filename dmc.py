import os

import pygame
from pygame.rect import Rect


def load_image(name, color_key=None):
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error as message:
        print('Не удаётся загрузить:', name)
        raise SystemExit(message)
    # image = image.convert_alpha()
    if color_key is not None:
        # image = image.convert()
        if color_key == -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    return image


#  список нарезаных спрайтов
def load_frames(name, columns, rows):
    im = load_image(name)
    result = []
    for j in range(rows):
        for i in range(columns):
            frame_location = (108 * i, 149 * j)
            result.append(im.surface(Rect(frame_location, (108, 149))))
    return result


class Player:
    def __init__(self, x, y, speed=(0, 0)):
        self.x = x
        self.y = y
        self.bounds = Rect(x, y, 50, 50)
        self.speed = speed  # (dx, dy)
        self.image = load_image('hero01.jpeg', -1)
        self.frames = load_frames('sprite-sheet-walking-girl.png', 6, 5)

    def handle_events(self, keys, fps):
        dx = 0
        dy = 0
        if keys[pygame.K_a]:
            dx = -250 / fps
        if keys[pygame.K_d]:
            dx = 250 / fps
        if keys[pygame.K_w]:
            dy = -250 / fps
        if keys[pygame.K_s]:
            dy = 250 / fps
        self.speed = (dx, dy)

    def move(self, dx, dy):
        self.bounds = self.bounds.move(int(dx), int(dy))

    def update(self):
        if self.speed != (0, 0):
            self.move(*self.speed)

    def draw(self, surface):
        surface.blit(self.image, (self.bounds.x, self.bounds.y))
        # pygame.draw.rect(surface, (255, 0, 0), self.bounds)
