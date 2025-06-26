""" Configurações gerais do projeto: importações de bibliotecas e definições de tamanhos. """

import pygame
from os import walk
from os.path import join
from pytmx.util_pygame import load_pygame

WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 720
TILE_SIZE = 18
FRAMERATE = 60
BG_COLOR = '#9fcef5'