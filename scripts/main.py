""" main.py """
import pygame

from settings import *
from sprites import *
from groups import AllSprites
from utils import *
from timer import Timer

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
        self.stairs_sprites = pygame.sprite.Group()
        self.collectable_sprites = pygame.sprite.Group()
        self.enemy_sprites = pygame.sprite.Group()

        # Camera position
        self.camera_pos = pygame.Vector2()

        # Load game
        self.load_assets()
        self.setup()

        # Timers
        self.bat_timer = Timer(1000, self.spawn_bat, True, True)

    def spawn_bat(self):
        Bat(
            frames=self.bat_frames,
            pos=((self.level_width + WINDOW_WIDTH), randint(0, self.level_height / 2)),
            groups=(self.all_sprites, self.enemy_sprites),
            speed=randint(100, 250)
        )

    def load_assets(self):
        self.player_frames_1 = import_folder('Tiles', 'Player_1')
        self.player_frames_2 = import_folder('Tiles', 'Player_2')
        self.player_frames_3 = import_folder('Tiles', 'Player_3')

        self.bat_frames = import_folder('Tiles', 'Bat')

        self.audio = audio_importer('audio')
        pygame.Sound.set_volume(self.audio['music'], 0.05)
        self.audio['music'].play()

    def setup(self):
        tmx_map = load_pygame(join('..', 'assets', 'Tilemap', 'world-1.tmx'))
        self.level_width = tmx_map.width * TILE_SIZE
        self.level_height = tmx_map.height * TILE_SIZE

        for x, y, image in tmx_map.get_layer_by_name('World').tiles():
            Sprite((x * TILE_SIZE, y * TILE_SIZE), image, (self.all_sprites, self.collision_sprites))

        for x, y, image in tmx_map.get_layer_by_name('Decoration').tiles():
            Sprite((x * TILE_SIZE, y * TILE_SIZE), image, (self.all_sprites))

        for obj in tmx_map.get_layer_by_name('Entities'):
            if obj.name == 'Player':
                self.player = Player(
                    (obj.x, obj.y),
                    self.all_sprites,
                    self.collision_sprites,
                    self.stairs_sprites,
                    self.collectable_sprites,
                    self.player_frames_1
                )
            if not hasattr(self, 'player_start_pos'):
                self.player_start_pos = (obj.x, obj.y)

        for obj in tmx_map.get_layer_by_name('Stairs'):
            stair_rect = pygame.FRect(obj.x, obj.y, obj.width, obj.height)
            Sprite((obj.x, obj.y), pygame.Surface((obj.width, obj.height)), (self.stairs_sprites,))

        for x, y, image in tmx_map.get_layer_by_name('Collectables').tiles():
            Sprite((x * TILE_SIZE, y * TILE_SIZE), image, (self.all_sprites, self.collectable_sprites))

    def show_game_over_screen(self):
        button_width, button_height = 300, 80
        button_rect = pygame.Rect(
            (WINDOW_WIDTH - button_width) // 2,
            (WINDOW_HEIGHT // 2) + 50,
            button_width,
            button_height
        )

        font = pygame.font.Font(None, 80)
        small_font = pygame.font.Font(None, 50)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if button_rect.collidepoint(event.pos):
                        self.reset_game()
                        return

            self.display.fill((0, 0, 0))  # tela preta

            text_surface = font.render("Você perdeu!", True, (255, 0, 0))
            text_rect = text_surface.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 100))
            self.display.blit(text_surface, text_rect)

            pygame.draw.rect(self.display, (50, 50, 50), button_rect)
            button_text = small_font.render("Reiniciar", True, (255, 255, 255))
            button_text_rect = button_text.get_rect(center=button_rect.center)
            self.display.blit(button_text, button_text_rect)

            pygame.display.update()

    def reset_game(self):
        self.all_sprites.empty()
        self.collision_sprites.empty()
        self.stairs_sprites.empty()
        self.collectable_sprites.empty()
        self.enemy_sprites.empty()

        self.camera_pos = pygame.Vector2()

        self.load_assets()

        tmx_map = load_pygame(join('..', 'assets', 'Tilemap', 'world-1.tmx'))
        self.level_width = tmx_map.width * TILE_SIZE
        self.level_height = tmx_map.height * TILE_SIZE

        for x, y, image in tmx_map.get_layer_by_name('World').tiles():
            Sprite((x * TILE_SIZE, y * TILE_SIZE), image, (self.all_sprites, self.collision_sprites))

        for x, y, image in tmx_map.get_layer_by_name('Decoration').tiles():
            Sprite((x * TILE_SIZE, y * TILE_SIZE), image, (self.all_sprites))

        for obj in tmx_map.get_layer_by_name('Stairs'):
            stair_rect = pygame.FRect(obj.x, obj.y, obj.width, obj.height)
            Sprite((obj.x, obj.y), pygame.Surface((obj.width, obj.height)), (self.stairs_sprites, self.all_sprites))

        for x, y, image in tmx_map.get_layer_by_name('Collectables').tiles():
            Sprite((x * TILE_SIZE, y * TILE_SIZE), image, (self.all_sprites, self.collectable_sprites))

        self.player = Player(
            self.player_start_pos,
            self.all_sprites,
            self.collision_sprites,
            self.stairs_sprites,
            self.collectable_sprites,
            self.player_frames_1
        )

        self.bat_timer = Timer(1000, self.spawn_bat, True, True)

    def run(self):
        while self.running:
            # Delta Time
            dt = self.clock.tick(FRAMERATE) / 1000

            # Event loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            # Update
            self.bat_timer.update()
            self.all_sprites.update(dt)

            # Enemy collision
            if pygame.sprite.spritecollideany(self.player, self.enemy_sprites):
                self.show_game_over_screen()
                continue

            # End game
            if self.player.won:
                self.display.fill((0, 0, 0))  # tela preta
                font = pygame.font.Font(None, 80)
                text_surface = font.render("Você ganhou!", True, (255, 255, 255))
                text_rect = text_surface.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
                self.display.blit(text_surface, text_rect)
                pygame.display.update()

                # Espera 2 segundos e fecha o jogo
                pygame.time.delay(2000)
                self.running = False
                continue  # evita continuar o loop

            # Camera lerp
            target_pos = self.player.rect.center
            self.camera_pos += (pygame.Vector2(target_pos) - self.camera_pos) * min(10 * dt, 1)

            self.display.fill(BG_COLOR)
            self.all_sprites.draw(self.camera_pos, zoom=3.0)
            pygame.display.update()

        pygame.quit()

if __name__ == '__main__':
    game = Game()
    game.run()