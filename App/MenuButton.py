from tkinter import *


class MenuButton(Label):

    def __init__(self, focused_image=None, **kwargs):
        super().__init__(**kwargs)
        self.default_image = kwargs.get("image")
        self.focused_image = focused_image
