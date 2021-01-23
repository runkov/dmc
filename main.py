import pygame

from dmc import Player


class DMC:
    def __init__(self):
        self.running = True
        self.fps = 60
        self.clock = pygame.time.Clock()
        self.player = Player(100, 100)
        self.size = self.width, self.height = 800, 400
        self.surface = pygame.display.set_mode(self.size)

    def run(self):
        pygame.init()
        pygame.display.set_caption('Движущийся круг 2')
        while self.running:
            dx = 0
            dy = 0
            # регистрируем зажатые кнопки
            keys = pygame.key.get_pressed()
            if keys[pygame.K_a]:
                dx = -250 / self.fps
            if keys[pygame.K_d]:
                dx = 250 / self.fps
            if keys[pygame.K_w]:
                dy = -250 / self.fps
            if keys[pygame.K_s]:
                dy = 250 / self.fps
            self.player.speed = (dx, dy)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False
            self.surface.fill((0, 0, 0))
            self.player.update()
            self.player.draw(self.surface)
            self.clock.tick(self.fps)
            pygame.display.flip()


if __name__ == '__main__':
    DMC().run()
    pygame.quit()
