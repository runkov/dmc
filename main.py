import pygame

from dmc import Player


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
        self.size = self.width, self.height = 800, 400
        self.surface = pygame.display.set_mode(self.size)

    def run(self):
        while self._running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self._running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self._running = False
            self.surface.fill((0, 0, 0))

            #  регистрируем зажатые кнопки
            keys = pygame.key.get_pressed()

            #  управляем игроком
            self.player.handle_events(keys, self.fps)
            self.player.update()
            self.player.draw(self.surface)

            self.clock.tick(self.fps)
            pygame.display.flip()


if __name__ == '__main__':
    DMC().run()
    pygame.quit()
