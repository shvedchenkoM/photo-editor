'''
Class toggle. Created because the standard library didn't have the toggle I needed.
'''

import pygame
from pygame_gui.elements.ui_button import UIButton
from pygame_gui.core.interfaces import IUIManagerInterface
from pygame_gui.core.ui_element import UIElement


class Toggle(UIButton, UIElement):
    def __init__(self, relative_rect: pygame.Rect, text: (str, str), manager: IUIManagerInterface,
                 font: pygame.font.Font):
        self.first_text, self.second_text = text
        UIButton.__init__(self, relative_rect=relative_rect, text=self.first_text, manager=manager)
        self.showed_text = self.first_text
        self._click_count = 0
    # overridden function
    def update(self, time_delta: float):
        UIElement.update(self, time_delta)
        if self.alive():
            # 0,1 -> +(text.first) ; 2,3 -> -(text.second)
            # clear pressed state, we only want it to last one update cycle
            self.pressed = False

            if self.pressed_event:
                # if a pressed event has occurred set the button to the pressed state for one cycle.
                self.pressed_event = False
                self.pressed = True
                self._click_count += 1
                print(self._click_count)

            if self._click_count % 2 < 1:
                self.set_text(self.first_text)
            else:
                self.set_text(self.second_text)

        # print(self.font.size("+"))
