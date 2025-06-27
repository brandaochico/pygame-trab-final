""" Funções de uso geral """

from settings import *

def import_image(*path, format = 'png', alpha = True):
    full_path = join('..', 'assets', *path) + f'.{format}'
    return pygame.image.load(full_path).convert_alpha() if alpha else pygame.image.load(full_path).convert()

def import_folder(*path):
    frames = []
    for folder_path, _, file_names in walk(join('..', 'assets', *path)):
        for file_name in sorted(file_names, key = lambda name: int(name.split('.')[0])):
            full_path = join(folder_path, file_name)
            frames.append(pygame.image.load(full_path).convert_alpha())

    return frames

def audio_importer(*path):
    audios = {}
    for folder_path, _, file_names in walk(join('..', *path)):
        for file_name in file_names:
            full_path = join(folder_path, file_name)
            audios[file_name.split('.')[0]] = pygame.mixer.Sound(full_path)

    return audios
