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


#  вернет список нарезаных спрайтов
def load_frames(name, columns, rows, reverse=False):
    sheet = load_image(name)
    result = []
    for j in range(rows):
        for i in range(columns):
            frame_location = (108 * i, 149 * j)
            if reverse:
                result.append(pygame.transform.flip(sheet.subsurface(Rect(frame_location, (108, 149))), True, False))
            else:
                result.append(sheet.subsurface(Rect(frame_location, (108, 149))))
    return result


class Player:
    def __init__(self, x, y, speed=(0, 0)):
        self.bounds = Rect(x, y, 50, 50)
        self.speed = speed  # (dx, dy)
        self._last_speed = speed
        self.image = load_image('hero01.jpeg', -1)
        self._frames_right = load_frames('sprite-sheet-walking-girl.png', 6, 5)
        self._frames_left = load_frames('sprite-sheet-walking-girl.png', 6, 5, reverse=True)
        self.animation_speed = 8
        self.animation_tick = 0
        self.animation_current_frame = 0

    @property
    def x(self):
        return self.bounds.x

    @property
    def y(self):
        return self.bounds.y

    @property
    def is_run(self):
        if self.speed == (0, 0):
            return False
        else:
            return True

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
        self._last_speed = (dx, dy)

    def update(self):
        if self.speed != (0, 0):
            self.move(*self.speed)
        if self.animation_tick == 0:
            self.animation_current_frame = (self.animation_current_frame + 1) % 5
            if self.is_run:
                if self.speed[0] < 0:
                    self.image = self._frames_left[self.animation_current_frame]
                elif self.speed[0] > 0:
                    self.image = self._frames_right[self.animation_current_frame]
            else:
                self.image = self._frames_right[12]
        self.animation_tick = (self.animation_tick + 1) % (60 // self.animation_speed)

    def draw(self, surface):
        surface.blit(self.image, (self.bounds.x, self.bounds.y))
        # pygame.draw.rect(surface, (255, 0, 0), self.bounds)
