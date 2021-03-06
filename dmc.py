import os

import pygame
from constants import *
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


class Map:
    def __init__(self, width, height):
        def color_tile(color):
            result = pygame.Surface((MAP_TILE_WIDTH, MAP_TILE_HEIGHT))
            result.fill(color)
            return result

        self.tiles = {
            EMPTY_MAP_TILE: color_tile((0, 0, 0)),
            GRASS_MAP_TILE: load_image('grass00.png')
        }

        self._background = pygame.Surface((width, height))
        for x in range(width // MAP_TILE_WIDTH):
            for y in range(height // MAP_TILE_HEIGHT):
                if x == 0 or y == 0:
                    self.background.blit(self.tiles[EMPTY_MAP_TILE], (x * MAP_TILE_WIDTH, y * MAP_TILE_HEIGHT))
                else:
                    self.background.blit(self.tiles[GRASS_MAP_TILE], (x * MAP_TILE_WIDTH, y * MAP_TILE_HEIGHT))

    @property
    def background(self):
        return self._background


class GameEntity:
    def __init__(self, x, y, speed=(0, 0), fps=DEFAULT_FPS):
        self.fps = fps
        self.speed = speed
        self.bounds = Rect(x, y, 50, 50)
        self.bounds.center = (x, y)
        self.direction = TO_THE_RIGHT
        self.image = load_image('monster01.png', -1)
        self.image_dx = (self.bounds.w - self.image.get_width()) // 2
        self.image_dy = (self.bounds.h // 2 - self.image.get_height())

    def draw(self, surface, camera):
        surface.blit(self.image,
                     (self.bounds.x + self.image_dx - camera.x,
                      self.bounds.y + self.image_dy - camera.y))

    def get_rect_image(self):
        return self.image.get_rect().move((self.bounds.x + self.image_dx,
                                           self.bounds.y + self.image_dy))

    def update(self, target):
        # dx = 0
        # dy = 0
        line_speed = PLAYER_SPEED // 4 // self.fps
        if self.bounds.centerx - target.x > 0:
            dx = -line_speed
        else:
            dx = line_speed
        if self.bounds.centery - target.y > 0:
            dy = -line_speed
        else:
            dy = line_speed
        self.speed = (dx, dy)
        self.move(*self.speed)

    def move(self, dx, dy):
        self.bounds = self.bounds.move(int(dx), int(dy))
        # self.image.rect = self.image.get_rect().move(int(dx), int(dy))


class Player:
    def __init__(self, x, y, speed=(0, 0), fps=DEFAULT_FPS):
        self.fps = fps
        self.bounds = Rect(x, y, 50, 50)
        self.bounds.center = (x, y)
        self.speed = speed  # (dx, dy)
        self._last_speed = speed
        self.direction = TO_THE_RIGHT
        self.image = load_image('hero01.jpeg', -1)
        self.frames = {
            TO_THE_RIGHT: load_frames('sprite-sheet-walking-girl.png', 6, 5),
            TO_THE_LEFT: load_frames('sprite-sheet-walking-girl.png', 6, 5, reverse=True)
        }
        self.animation_speed = 8
        self.animation_tick = 0
        self.animation_current_frame = 0
        self.image_dx = (self.bounds.w - self.frames[TO_THE_LEFT][0].get_width()) // 2
        self.image_dy = (self.bounds.h // 2 - self.frames[TO_THE_LEFT][0].get_height())

    @property
    def x(self):
        return self.bounds.centerx

    @property
    def y(self):
        return self.bounds.centery

    @property
    def is_run(self):
        if self.speed == (0, 0):
            return False
        else:
            return True

    def set_fps(self, new_fps):
        self.fps = new_fps

    def handle_events(self, keys):
        dx = 0
        dy = 0
        if keys[pygame.K_a]:
            dx = -PLAYER_SPEED / self.fps
        if keys[pygame.K_d]:
            dx = PLAYER_SPEED / self.fps
        if keys[pygame.K_w]:
            dy = -PLAYER_SPEED / self.fps
        if keys[pygame.K_s]:
            dy = PLAYER_SPEED / self.fps
        self._last_speed = self.speed
        self.speed = (dx, dy)
        if self.speed[0] > 0:
            self.direction = TO_THE_RIGHT
        elif self.speed[0] < 0:
            self.direction = TO_THE_LEFT

    def move(self, dx, dy):
        self.bounds = self.bounds.move(int(dx), int(dy))

    def update(self):
        if self.speed != (0, 0):
            self.move(*self.speed)
        #  определяем спрайт для анимации персонажа
        if self.animation_tick == 0:
            self.animation_current_frame = (self.animation_current_frame + 1) % 5
            if self.is_run:
                self.image = self.frames[self.direction][self.animation_current_frame]
            else:
                self.image = self.frames[self.direction][12]
        self.animation_tick = (self.animation_tick + 1) % (60 // self.animation_speed)

    def draw(self, surface, camera):
        surface.blit(self.image, (self.bounds.x + self.image_dx - camera.x,
                                  self.bounds.y + self.image_dy - camera.y))


class Camera:
    # зададим начальный сдвиг камеры
    def __init__(self, surface):
        self.x = 0
        self.y = 0
        #  todo добавить прямоугольник в центр камеры, по пересечению с которым определять необходимость сдвига камеры

    def convert_bounds_to_camera(self, bounds):
        return Rect(bounds.x - self.x, bounds.y - self.y, bounds.width, bounds.height)

    def update(self, target):
        if target.x < self.x + 100:
            self.x += target.x - (self.x + 100)
        elif target.x > self.x + 500:
            self.x += target.x - (self.x + 500)
        if target.y < self.y + 200:
            self.y += target.y - (self.y + 200)
        elif target.y > self.y + 300:
            self.y += target.y - (self.y + 300)
