""" main.py """

from settings import *
from sprites import *
from groups import AllSprites
from utils import *

class Game():
    def __init__(self):
        pygame.init()
        self.display = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('Platformer')
        self.clock = pygame.Clock()
        self.running = True

        # Grupos
        self.all_sprites = AllSprites()
        self.collision_sprites = pygame.sprite.Group()

        # Camera position
        self.camera_pos = pygame.Vector2()

        # Load game
        self.load_assets()
        self.setup()

    def load_assets(self):
        self.player_frames_1 = import_folder('Tiles', 'Player_1')
        print(self.player_frames_1)

    def setup(self):
        tmx_map = load_pygame(join('..', 'assets', 'Tilemap', 'world-1.tmx'))

        for x, y, image in tmx_map.get_layer_by_name('World').tiles():
            Sprite((x * TILE_SIZE, y * TILE_SIZE), image, (self.all_sprites, self.collision_sprites))

        for x, y, image in tmx_map.get_layer_by_name('Decoration').tiles():
            Sprite((x * TILE_SIZE, y * TILE_SIZE), image, (self.all_sprites))

        for obj in tmx_map.get_layer_by_name('Entities'):
            if obj.name == 'Player':
                self.player = Player((obj.x, obj.y), self.all_sprites, self.collision_sprites, self.player_frames_1)

    def run(self):
        while self.running:
            # Delta Time
            dt = self.clock.tick(FRAMERATE) / 1000

            # Event loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            # Update
            self.all_sprites.update(dt)

            # Camera lerp
            target_pos = self.player.rect.center
            self.camera_pos += (pygame.Vector2(target_pos) - self.camera_pos) * min(10 * dt, 1)

            self.display.fill(BG_COLOR)
            self.all_sprites.draw(self.camera_pos, zoom=2.0)
            pygame.display.update()

        pygame.quit()

if __name__ == '__main__':
    game = Game()
    game.run()