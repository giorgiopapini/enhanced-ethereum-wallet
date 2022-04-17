from tkinter import *


class ContactTile(Frame):

    def __init__(self, parent=None, name=None, address=None, **kwargs):
        super().__init__(**kwargs)
        self.parent = parent
        self.name = name
        self.address = address


