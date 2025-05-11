import pygame


class Explosion:
    def __init__(self, x, y, radius=80, duration=30):
        self.x = x
        self.y = y
        self.radius = radius
        self.duration = duration
        self.frame = 0

    def draw(self, screen):
        if self.frame < self.duration:
            alpha = max(0, 255 - int((self.frame / self.duration) * 255))
            surface = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA)
            pygame.draw.circle(surface, (255, 0, 0, alpha), (self.radius, self.radius), self.radius)
            screen.blit(surface, (self.x - self.radius, self.y - self.radius))
            self.frame += 1
