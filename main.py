import pygame

if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('Движущийся круг 2')
    size = width, height = 800, 400
    screen = pygame.display.set_mode(size)

    running = True
    x_pos = 100
    y_pos = 100
    v = 250  # пикселей в секунду
    fps = 60
    clock = pygame.time.Clock()
    while running:
        # регистрируем зажатые кнопки
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            x_pos -= v / fps
        if keys[pygame.K_d]:
            x_pos += v / fps
        if keys[pygame.K_w]:
            y_pos -= v / fps
        if keys[pygame.K_s]:
            y_pos += v / fps
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
        screen.fill((0, 0, 0))
        pygame.draw.circle(screen, (255, 0, 0), (int(x_pos), int(y_pos)), 20)
        clock.tick(fps)
        pygame.display.flip()
    pygame.quit()