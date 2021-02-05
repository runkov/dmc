import pygame

from dmc import Player, Map, Camera, GameEntity


class DMC:
    def __init__(self):
        #  инициализация pygame нужна некоторым методам работающими с изображениями,
        #  поэтому делаем в самом начале до создания всех спрайтов
        pygame.init()
        pygame.display.set_caption('DMC')
        self._running = True
        self.fps = 60
        self.clock = pygame.time.Clock()
        self.player = Player(100, 100)
        self.monster = GameEntity(300, 150)
        self.map = Map(1000, 600)
        self.size = self.width, self.height = 800, 600
        self.screen = pygame.display.set_mode(self.size)  # главная поверхность
        self.camera = Camera(self.screen)
        self.screen.blit(self.map.background, (0, 0))

    def run(self):
        debug_mode = True
        while self._running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self._running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self._running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 3:  # правая кнопка мыши
                        debug_mode = not debug_mode
            self.screen.fill((0, 0, 0))
            self.screen.blit(self.map.background, (0 - self.camera.x, 0 - self.camera.y))

            #  регистрируем зажатые кнопки
            keys = pygame.key.get_pressed()

            #  обрабатываем события
            self.player.handle_events(keys)

            #  делаем расчеты относительно произошедших событий
            self.player.update()
            self.camera.update(self.player)
            self.monster.update(self.player)

            #  рисуем на экран в область камеры все что туда помещается
            self.player.draw(self.screen, self.camera)
            self.monster.draw(self.screen, self.camera)

            #  todo предусмотреть как опцию для отладки
            if debug_mode:
                pygame.draw.rect(self.screen,
                                 pygame.Color('red'),
                                 self.camera.convert_bounds_to_camera(self.monster.bounds),
                                 2)  # Толщина линии
                pygame.draw.rect(self.screen,
                                 pygame.Color('blue'),
                                 self.camera.convert_bounds_to_camera(self.monster.image.get_rect(bottom=self.monster.bounds.centery, centerx=self.monster.bounds.centerx)),
                                 2)  # Толщина линии
                pygame.draw.rect(self.screen,
                                 pygame.Color('red'),
                                 self.camera.convert_bounds_to_camera(self.player.bounds),
                                 2)  # Толщина линии
                pygame.draw.rect(self.screen,
                                 pygame.Color('blue'),
                                 self.camera.convert_bounds_to_camera(self.player.image.get_rect(bottom=self.player.bounds.centery, centerx=self.player.bounds.centerx)),
                                 2)  # Толщина линии
            self.clock.tick(self.fps)
            pygame.display.update()


if __name__ == '__main__':
    DMC().run()
    pygame.quit()
