'''
Start of the application
'''

import pygame
import pygame_gui
import easygui
import shutil
import os

import settings
from controller import Controller
from ScreenSize import get_window
from utils import Utils

# -------initialize-------

controller_for_image = Controller()
pygame.init()

# --get display size--
wd, hd = get_window()
settings.coficient = (wd / settings.DisplayWidth, hd / settings.DisplayHeight)
# --end get display size--

# --import all scenes--
from scenes import start_menu

# --end import all scenes--

# --initialize window--
pygame.display.set_caption('Small Photo Editor')
window_surface = pygame.display.set_mode(settings.update((settings.Width, settings.Height)))
background = pygame.Surface(settings.update((settings.Width, settings.Height)))
background.fill(pygame.Color('#AA00FF'))
# --end initialize window--
scene = None
# --initialize main scene,clock,game process,and paths--
scene = start_menu
clock = pygame.time.Clock()
is_running = True
image_path = ""
original_image_path = ""
# --end initialize main scene,clock,game process,and paths--

# -------end initialize-------
from GameProcess import GameProcess

game_process = GameProcess(clock, is_running, image_path, original_image_path, scene, controller_for_image,
                           window_surface,
                           background)
game_process.Run()
