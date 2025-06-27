from settings import *

class AllSprites(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display = pygame.display.get_surface()
        self.offset = pygame.Vector2()

    def draw(self, center, surface=None, zoom=1.0):
        surface = surface or pygame.display.get_surface()

        display_center = pygame.Vector2(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)
        offset = pygame.Vector2(center) - display_center / zoom

        for sprite in sorted(self.sprites(), key=lambda spr: spr.rect.centery):
            rel_pos = (sprite.rect.topleft - offset) * zoom

            scaled_size = (int(sprite.rect.width * zoom), int(sprite.rect.height * zoom))
            scaled_image = pygame.transform.scale(sprite.image, scaled_size)

            surface.blit(scaled_image, rel_pos)
