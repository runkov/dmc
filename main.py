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
        self.camera = Camera()
        self.size = self.width, self.height = 800, 400
        self.screen = pygame.display.set_mode(self.size)  # главная поверхность
        self.screen.blit(self.map.background, (0, 0))

    def run(self):
        while self._running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self._running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self._running = False
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

            self.clock.tick(self.fps)
            pygame.display.update()


if __name__ == '__main__':
    DMC().run()
    pygame.quit()
