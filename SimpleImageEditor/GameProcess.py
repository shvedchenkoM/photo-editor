'''
Implementing logic of game processing here.
'''

import os
import pygame
import pygame_gui
from scenes import second_menu, work_scene, brightness_scene, color_scene, sharp_scene, contrast_scene
import Scene
import easygui
import shutil
import settings
from utils import Utils
from controller import Controller


class GameProcess:

    def __init__(self, clock: pygame.time.Clock, is_running: bool, image_path: str, original_image_path: str,
                 scene: Scene, controller_for_image: Controller, window_surface, background):
        self.clock = clock

        self.is_running = is_running
        self.image_path = image_path
        self.original_image_path = original_image_path
        self.scene = scene
        self.controller_for_image = controller_for_image
        self.window_surface = window_surface
        self.background = background

    # deal with state, when exit button is clicked
    def _on_exit(self):
        self.is_running = False
        self.original_image_path = ""
        if os.path.exists(self.image_path):
            os.remove(self.image_path)

        if os.path.exists("brightness." + self.image_path.split(".")[-1]):
            os.remove("brightness." + self.image_path.split(".")[-1])
        if os.path.exists("color." + self.image_path.split(".")[-1]):
            os.remove("color." + self.image_path.split(".")[-1])
        if os.path.exists("sharp." + self.image_path.split(".")[-1]):
            os.remove("sharp." + self.image_path.split(".")[-1])
        if os.path.exists("contrast." + self.image_path.split(".")[-1]):
            os.remove("contrast." + self.image_path.split(".")[-1])
        self.image_path = ""

# update after using all (any) effects on all scenes
    def _update_image(self):
        work_scene.add_image(self.image_path, settings.Image_position, settings.Image_scale,
                             "image")
        brightness_scene.add_image(self.image_path, settings.Image_position, settings.Image_scale,
                                   "image")
        color_scene.add_image(self.image_path, settings.Image_position, settings.Image_scale,
                              "image")
        sharp_scene.add_image(self.image_path, settings.Image_position, settings.Image_scale,
                              "image")
        contrast_scene.add_image(self.image_path, settings.Image_position, settings.Image_scale,
                                 "image")

    def check_second_scene(self, event):
        if event.ui_element == self.scene.buttons["choose photo"]:
            # Open file:
            self.original_image_path = (easygui.fileopenbox())
            if not Utils.check_file(self.original_image_path):
                return
            type_of_image = self.original_image_path.split(".")[-1]
            f = open(".image." + type_of_image, "w+")
            f.close()
            shutil.copy(self.original_image_path, ".image." + type_of_image)
            self.image_path = ".image." + type_of_image
            print(self.image_path)
            self._update_image()
            self.scene = work_scene

        if event.ui_element == self.scene.buttons["exit"]:
            self._on_exit()
            brightness_scene.sliders["slider"].set_current_value(100)
            color_scene.sliders["slider"].set_current_value(100)
            sharp_scene.sliders["slider"].set_current_value(100)
            contrast_scene.sliders["slider"].set_current_value(100)
            self.image_path = ""

    def check_work_scene(self, event):
        if event.ui_element == self.scene.buttons["exit"]:
            work_scene.toggles["toggle"]._click_count = 0
            self.scene = second_menu
            self.original_image_path = ""
            if os.path.exists(self.image_path):
                os.remove(self.image_path)
            return

        if event.ui_element == self.scene.buttons["save"]:
            shutil.copy(self.image_path, self.original_image_path)
        if event.ui_element == self.scene.buttons["Brightness"]:
            self.scene = brightness_scene
            return
        if event.ui_element == self.scene.buttons["Set Color"]:
            self.scene = color_scene
            return
        if event.ui_element == self.scene.buttons["Sharp"]:
            self.scene = sharp_scene
            return
        if event.ui_element == self.scene.buttons["Contrast"]:
            self.scene = contrast_scene
            return
        if event.ui_element == self.scene.toggles["toggle"]:
            if self.scene.toggles["toggle"].text == "-":
                self.scene.image_to_max_size(self.image_path, settings.Image_position, settings.Image_scale, "image")
                brightness_scene.image_to_max_size(self.image_path, settings.Image_position, settings.Image_scale,
                                                   "image")
                color_scene.image_to_max_size(self.image_path, settings.Image_position, settings.Image_scale,
                                              "image")
                contrast_scene.image_to_max_size(self.image_path, settings.Image_position, settings.Image_scale,
                                                 "image")
                sharp_scene.image_to_max_size(self.image_path, settings.Image_position, settings.Image_scale,
                                              "image")
            if self.scene.toggles["toggle"].text == "+":
                self.scene.image_to_min_size(self.image_path, settings.Image_position, settings.Image_scale, "image")
                brightness_scene.image_to_min_size(self.image_path, settings.Image_position, settings.Image_scale,
                                                   "image")
                color_scene.image_to_min_size(self.image_path, settings.Image_position, settings.Image_scale,
                                              "image")
                contrast_scene.image_to_min_size(self.image_path, settings.Image_position, settings.Image_scale,
                                                 "image")
                sharp_scene.image_to_min_size(self.image_path, settings.Image_position, settings.Image_scale,
                                              "image")

    def check_brightness_scene(self, event):
        if event.ui_element == self.scene.buttons["exit"]:
            if os.path.exists("brightness." + self.image_path.split(".")[-1]):
                shutil.copy("brightness." + self.image_path.split(".")[-1],
                            ".image." + self.image_path.split(".")[-1])

            work_scene.add_image(self.image_path, settings.Image_position, settings.Image_scale,
                                 "image")
            color_scene.add_image(self.image_path, settings.Image_position, settings.Image_scale,
                                  "image")
            sharp_scene.add_image(self.image_path, settings.Image_position, settings.Image_scale,
                                  "image")
            contrast_scene.add_image(self.image_path, settings.Image_position, settings.Image_scale,
                                     "image")
            self.scene = work_scene

            if work_scene.toggles["toggle"].text == '-':
                self.scene.image_to_max_size("brightness." + self.image_path.split(".")[-1],
                                             settings.Image_position,
                                             settings.Image_scale, "image")
                brightness_scene.image_to_max_size("brightness." + self.image_path.split(".")[-1],
                                                   settings.Image_position, settings.Image_scale,
                                                   "image")
                color_scene.image_to_max_size("brightness." + self.image_path.split(".")[-1],
                                              settings.Image_position, settings.Image_scale,
                                              "image")
                contrast_scene.image_to_max_size("brightness." + self.image_path.split(".")[-1],
                                                 settings.Image_position, settings.Image_scale,
                                                 "image")
                sharp_scene.image_to_max_size("brightness." + self.image_path.split(".")[-1],
                                              settings.Image_position, settings.Image_scale,
                                              "image")
            else:
                self.scene.image_to_min_size("brightness." + self.image_path.split(".")[-1],
                                             settings.Image_position,
                                             settings.Image_scale, "image")
                brightness_scene.image_to_min_size("brightness." + self.image_path.split(".")[-1],
                                                   settings.Image_position, settings.Image_scale,
                                                   "image")
                color_scene.image_to_min_size("brightness." + self.image_path.split(".")[-1],
                                              settings.Image_position, settings.Image_scale,
                                              "image")
                contrast_scene.image_to_min_size("brightness." + self.image_path.split(".")[-1],
                                                 settings.Image_position, settings.Image_scale,
                                                 "image")
                sharp_scene.image_to_min_size("brightness." + self.image_path.split(".")[-1],
                                              settings.Image_position, settings.Image_scale,
                                              "image")
            return
        if event.ui_element == self.scene.sliders["slider"]:
            self.controller_for_image.apply_brighten(self.image_path,
                                                     self.scene.sliders["slider"].current_value)
            self.scene.add_image("brightness." + self.image_path.split(".")[-1],
                                 settings.Image_position,
                                 settings.Image_scale, "image")
            if work_scene.toggles["toggle"].text == '-':
                self.scene.image_to_max_size("brightness." + self.image_path.split(".")[-1],
                                             settings.Image_position,
                                             settings.Image_scale, "image")
            else:
                self.scene.image_to_min_size("brightness." + self.image_path.split(".")[-1],
                                             settings.Image_position,
                                             settings.Image_scale, "image")



    def check_color_scene(self, event):
        if event.ui_element == self.scene.buttons["exit"]:
            if os.path.exists("color." + self.image_path.split(".")[-1]):
                shutil.copy("color." + self.image_path.split(".")[-1],
                            ".image." + self.image_path.split(".")[-1])
            self._update_image()
            self.scene = work_scene
            if work_scene.toggles["toggle"].text == '-':
                self.scene.image_to_max_size("color." + self.image_path.split(".")[-1],
                                             settings.Image_position,
                                             settings.Image_scale, "image")
                brightness_scene.image_to_max_size("color." + self.image_path.split(".")[-1],
                                                   settings.Image_position, settings.Image_scale,
                                                   "image")
                color_scene.image_to_max_size("color." + self.image_path.split(".")[-1],
                                              settings.Image_position,
                                              settings.Image_scale,
                                              "image")
                contrast_scene.image_to_max_size("color." + self.image_path.split(".")[-1],
                                                 settings.Image_position,
                                                 settings.Image_scale,
                                                 "image")
                sharp_scene.image_to_max_size("color." + self.image_path.split(".")[-1],
                                              settings.Image_position,
                                              settings.Image_scale,
                                              "image")
            else:
                self.scene.image_to_min_size("color." + self.image_path.split(".")[-1],
                                             settings.Image_position,
                                             settings.Image_scale, "image")
                brightness_scene.image_to_min_size("color." + self.image_path.split(".")[-1],
                                                   settings.Image_position, settings.Image_scale,
                                                   "image")
                color_scene.image_to_min_size("color." + self.image_path.split(".")[-1],
                                              settings.Image_position,
                                              settings.Image_scale,
                                              "image")
                contrast_scene.image_to_min_size("color." + self.image_path.split(".")[-1],
                                                 settings.Image_position,
                                                 settings.Image_scale,
                                                 "image")
                sharp_scene.image_to_min_size("color." + self.image_path.split(".")[-1],
                                              settings.Image_position,
                                              settings.Image_scale,
                                              "image")
            return
        if event.ui_element == self.scene.sliders["slider"]:
            self.controller_for_image.apply_color(self.image_path,
                                                  self.scene.sliders["slider"].current_value)
            self.scene.add_image("color." + self.image_path.split(".")[-1], settings.Image_position,
                                 settings.Image_scale, "image")
            if work_scene.toggles["toggle"].text == '-':
                self.scene.image_to_max_size("color." + self.image_path.split(".")[-1],
                                             settings.Image_position,
                                             settings.Image_scale, "image")
            else:
                self.scene.image_to_min_size("color." + self.image_path.split(".")[-1],
                                             settings.Image_position,
                                             settings.Image_scale, "image")

    def check_contrast_scene(self, event):
        if event.ui_element == self.scene.buttons["exit"]:
            if os.path.exists("contrast." + self.image_path.split(".")[-1]):
                shutil.copy("contrast." + self.image_path.split(".")[-1],
                            ".image." + self.image_path.split(".")[-1])
            work_scene.add_image(self.image_path, settings.Image_position, settings.Image_scale,
                                 "image")
            brightness_scene.add_image(self.image_path, settings.Image_position, settings.Image_scale,
                                       "image")
            color_scene.add_image(self.image_path, settings.Image_position, settings.Image_scale,
                                  "image")
            sharp_scene.add_image(self.image_path, settings.Image_position, settings.Image_scale,
                                  "image")
            self.scene = work_scene
            if work_scene.toggles["toggle"].text == '-':
                self.scene.image_to_max_size("contrast." + self.image_path.split(".")[-1],
                                             settings.Image_position,
                                             settings.Image_scale, "image")
                brightness_scene.image_to_max_size("contrast." + self.image_path.split(".")[-1],
                                                   settings.Image_position, settings.Image_scale,
                                                   "image")
                color_scene.image_to_max_size("contrast." + self.image_path.split(".")[-1],
                                              settings.Image_position,
                                              settings.Image_scale,
                                              "image")
                contrast_scene.image_to_max_size("contrast." + self.image_path.split(".")[-1],
                                                 settings.Image_position,
                                                 settings.Image_scale,
                                                 "image")
                sharp_scene.image_to_max_size("contrast." + self.image_path.split(".")[-1],
                                              settings.Image_position,
                                              settings.Image_scale,
                                              "image")
            else:
                self.scene.image_to_min_size("contrast." + self.image_path.split(".")[-1],
                                             settings.Image_position,
                                             settings.Image_scale, "image")
                brightness_scene.image_to_min_size("contrast." + self.image_path.split(".")[-1],
                                                   settings.Image_position, settings.Image_scale,
                                                   "image")
                color_scene.image_to_min_size("contrast." + self.image_path.split(".")[-1],
                                              settings.Image_position,
                                              settings.Image_scale,
                                              "image")
                contrast_scene.image_to_min_size("contrast." + self.image_path.split(".")[-1],
                                                 settings.Image_position,
                                                 settings.Image_scale,
                                                 "image")
                sharp_scene.image_to_min_size("contrast." + self.image_path.split(".")[-1],
                                              settings.Image_position,
                                              settings.Image_scale,
                                              "image")
            return
        if event.ui_element == self.scene.sliders["slider"]:
            self.controller_for_image.apply_contrast(self.image_path,
                                                     self.scene.sliders["slider"].current_value)
            self.scene.add_image("contrast." + self.image_path.split(".")[-1], settings.Image_position,
                                 settings.Image_scale, "image")
            if work_scene.toggles["toggle"].text == '-':
                self.scene.image_to_max_size("contrast." + self.image_path.split(".")[-1],
                                             settings.Image_position,
                                             settings.Image_scale, "image")
            else:
                self.scene.image_to_min_size("contrast." + self.image_path.split(".")[-1],
                                             settings.Image_position,
                                             settings.Image_scale, "image")

    def check_sharp_scene(self, event):
        if event.ui_element == self.scene.buttons["exit"]:
            if os.path.exists("sharp." + self.image_path.split(".")[-1]):
                shutil.copy("sharp." + self.image_path.split(".")[-1],
                            ".image." + self.image_path.split(".")[-1])
            work_scene.add_image(self.image_path, settings.Image_position, settings.Image_scale,
                                 "image")
            brightness_scene.add_image(self.image_path, settings.Image_position, settings.Image_scale,
                                       "image")
            color_scene.add_image(self.image_path, settings.Image_position, settings.Image_scale,
                                  "image")
            contrast_scene.add_image(self.image_path, settings.Image_position, settings.Image_scale,
                                     "image")
            self.scene = work_scene
            if work_scene.toggles["toggle"].text == '-':
                self.scene.image_to_max_size("sharp." + self.image_path.split(".")[-1],
                                             settings.Image_position,
                                             settings.Image_scale, "image")
                brightness_scene.image_to_max_size("sharp." + self.image_path.split(".")[-1],
                                                   settings.Image_position, settings.Image_scale,
                                                   "image")
                color_scene.image_to_max_size("sharp." + self.image_path.split(".")[-1],
                                              settings.Image_position,
                                              settings.Image_scale,
                                              "image")
                contrast_scene.image_to_max_size("sharp." + self.image_path.split(".")[-1],
                                                 settings.Image_position,
                                                 settings.Image_scale,
                                                 "image")
                sharp_scene.image_to_max_size("sharp." + self.image_path.split(".")[-1],
                                              settings.Image_position,
                                              settings.Image_scale,
                                              "image")
            else:
                self.scene.image_to_min_size("sharp." + self.image_path.split(".")[-1],
                                             settings.Image_position,
                                             settings.Image_scale, "image")
                brightness_scene.image_to_min_size("sharp." + self.image_path.split(".")[-1],
                                                   settings.Image_position, settings.Image_scale,
                                                   "image")
                color_scene.image_to_min_size("sharp." + self.image_path.split(".")[-1],
                                              settings.Image_position,
                                              settings.Image_scale,
                                              "image")
                contrast_scene.image_to_min_size("sharp." + self.image_path.split(".")[-1],
                                                 settings.Image_position,
                                                 settings.Image_scale,
                                                 "image")
                sharp_scene.image_to_min_size("sharp." + self.image_path.split(".")[-1],
                                              settings.Image_position,
                                              settings.Image_scale,
                                              "image")
            return
        if event.ui_element == self.scene.sliders["slider"]:
            self.controller_for_image.apply_sharpness(self.image_path,
                                                      self.scene.sliders["slider"].current_value)
            self.scene.add_image("sharp." + self.image_path.split(".")[-1], settings.Image_position,
                                 settings.Image_scale, "image")
            if work_scene.toggles["toggle"].text == '-':
                self.scene.image_to_max_size("sharp." + self.image_path.split(".")[-1],
                                             settings.Image_position,
                                             settings.Image_scale, "image")
            else:
                self.scene.image_to_min_size("sharp." + self.image_path.split(".")[-1],
                                             settings.Image_position,
                                             settings.Image_scale, "image")

    def check_edit_scene(self, event):
        if self.scene.name == "brightness scene":
            self.check_brightness_scene(event)
        if self.scene.name == "color scene":
            self.check_color_scene(event)
        if self.scene.name == "contrast scene":
            self.check_contrast_scene(event)
        if self.scene.name == "sharp scene":
            self.check_sharp_scene(event)

    def Run(self):
        while self.is_running:
            time_delta = self.clock.tick(60) / 1000.0
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self._on_exit()
                if event.type == pygame.USEREVENT:
                    if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                        if self.scene.name == "start menu" and event.ui_element == self.scene.buttons["get started"]:
                            self.scene = second_menu
                        if self.scene.name == "second menu":
                            self.check_second_scene(event)
                        if self.scene.name == "work scene":
                            self.check_work_scene(event)
                        self.check_edit_scene(event)
                    if event.user_type == pygame_gui.UI_HORIZONTAL_SLIDER_MOVED:
                        self.check_edit_scene(event)

                self.scene.manager.process_events(event)

            self.scene.manager.update(time_delta)
            # -------draw-------

            self.window_surface.blit(self.background, (0, 0))
            self.scene.draw(self.window_surface)

            # -------draw-------

            pygame.display.update()
