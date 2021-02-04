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
        map_dx = 0
        dxm = 0
        map_dy = 0
        while self._running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self._running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self._running = False
            self.screen.fill((0, 0, 0))
            if self.player.x - map_dx < 100:
                map_dx = 100 - self.player.x
                dxm += map_dx
            elif self.player.x - map_dx > 400:
                map_dx = 100 - self.player.x
                dxm += map_dx
            self.screen.blit(self.map.background, (0 - self.camera.x, 0))

            #  регистрируем зажатые кнопки
            keys = pygame.key.get_pressed()

            #  управляем игроком
            self.player.handle_events(keys)
            self.player.update()
            self.camera.update(self.player)
            self.monster.update(self.player)
            self.player.draw(self.screen, self.camera.x, self.camera.y)

            self.monster.draw(self.screen, self.camera)

            # self.camera.update(self.player)
            # self.camera.apply(self.map)
            # self.camera.apply(self.player)

            self.clock.tick(self.fps)
            pygame.display.update()  # flip()


if __name__ == '__main__':
    DMC().run()
    pygame.quit()
