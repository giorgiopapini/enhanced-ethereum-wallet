from tkinter import *


class ListElement:

    def __init__(self, widget=None, **kwargs):
        if widget is None:
            raise TypeError("widget kwarg in ListElement should not be None")
        self.widget = widget
        self.widget_attributes = kwargs
