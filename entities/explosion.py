import pygame


class Explosion:
    """
    Visual effect representing an expanding and fading explosion.
    Typically used when an ExplodingEnemy is triggered.
    """

    def __init__(self, x, y, radius=80, duration=30):
        self.x = x
        self.y = y
        self.radius = radius
        self.duration = duration
        self.frame = 0

    def draw(self, screen):
        """
        Render the explosion effect onto the screen.

        - The explosion is drawn as a red circle that fades over time.
        - The circle's transparency is based on how many frames have passed.

        Args:
            screen (pygame.Surface): The screen to draw the explosion on.
        """
        if self.frame < self.duration:
            # Calculate transparency (alpha): from 255 → 0 over duration
            alpha = max(0, 255 - int((self.frame / self.duration) * 255))

            # Create a transparent surface for the fading circle
            surface = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA)

            # Draw red circle with current alpha
            pygame.draw.circle(surface, (255, 0, 0, alpha), (self.radius, self.radius), self.radius)

            # Blit the explosion centered at (x, y)
            screen.blit(surface, (self.x - self.radius, self.y - self.radius))

            # Advance to the next frame
            self.frame += 1
